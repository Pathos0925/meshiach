#!/usr/bin/env python3
"""Check every original-language quotation in data/prophecies.yaml against
published editions:

  * Tanakh, Targum, Talmud  -> Sefaria API (Miqra according to the Masorah etc.)
  * New Testament Greek      -> SBLGNT (LogosBible/SBLGNT on GitHub)

Hebrew/Aramaic is compared consonantally (vowels and cantillation stripped).
Greek is compared case- and punctuation-insensitively, accents kept.
A quotation may contain "..." to mark an omission; each segment is then
checked separately.

Usage:  python scripts/verify.py [--pointed]
  --pointed   also print the pointed (vocalised) Sefaria text for each entry
"""
from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "prophecies.yaml"

SEFARIA_BOOK = {
    "Genesis": "Genesis", "Deuteronomy": "Deuteronomy", "2 Samuel": "II Samuel",
    "Psalm": "Psalms", "Isaiah": "Isaiah", "Jeremiah": "Jeremiah", "Daniel": "Daniel",
    "Hosea": "Hosea", "Micah": "Micah", "Zechariah": "Zechariah", "Malachi": "Malachi",
}
SBLGNT_BOOK = {
    "Matthew": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
    "Romans": "Rom", "1 Corinthians": "1Cor", "Galatians": "Gal", "Philippians": "Phil",
    "Hebrews": "Heb", "1 Peter": "1Pet", "Revelation": "Rev",
}
SBLGNT_URL = "https://raw.githubusercontent.com/LogosBible/SBLGNT/master/data/sblgnt/text/{}.txt"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "meshiach-verify/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


# ---------------------------------------------------------------- Hebrew ----
HEB_MARKS = re.compile(r"[֑-ׇ]")          # cantillation + vowels + dagesh etc.


def heb_consonants(s: str) -> str:
    s = html.unescape(s)                             # &thinsp; &nbsp; ...
    s = re.sub(r"<[^>]+>", " ", s)                   # strip html (Sefaria footnotes)
    s = re.sub(r"[͏​-‏⁠﻿]", "", s)  # invisible joiners
    s = re.sub(r"[  ]", " ", s)                     # nbsp, thin space
    s = s.replace("־", " ")                     # maqaf -> space
    s = s.replace("׃", " ")                     # sof pasuk
    s = HEB_MARKS.sub("", s)
    s = re.sub(r"[{}\[\]()׀|״׳\"'“”:;,.!?—–-]", " ", s)  # brackets, paseq, gershayim, punctuation
    s = re.sub(r"\s+", " ", s).strip()
    # drop petucha/setuma markers
    return " ".join(w for w in s.split() if w not in ("פ", "ס"))


@lru_cache(maxsize=None)
def sefaria(ref: str) -> tuple[str, str]:
    """Return (versionTitle, plain text joined with spaces)."""
    url = "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref) + "?return_format=text_only"
    d = json.loads(fetch(url))
    v = d["versions"][0]
    t = v["text"]

    def flat(x):
        if isinstance(x, str):
            return [x]
        return [y for z in x for y in flat(z)]
    return v["versionTitle"], " ".join(flat(t))


def to_sefaria_ref(ref: str) -> str | None:
    """'Psalm 22:17 [16]' -> 'Psalms.22.17'; '2 Samuel 7:12-13' -> 'II Samuel.7.12-13'."""
    ref = re.sub(r"\s*\[[^\]]*\]", "", ref).strip()
    if ref.startswith("Targum Jonathan on "):
        inner = to_sefaria_ref(ref[len("Targum Jonathan on "):])
        return "Targum Jonathan on " + inner if inner else None
    m = re.match(r"^(Sanhedrin|Sukkah|Pesachim|Nedarim)\s+(\d+[ab])$", ref)
    if m:
        return f"{m.group(1)}.{m.group(2)}"
    m = re.match(r"^(Pesikta Rabbati|Midrash Tehillim)\s+(\d+)$", ref)
    if m:
        return f"{m.group(1)}.{m.group(2)}"
    m = re.match(r"^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$", ref)
    if not m:
        return None
    book, ch, v1, v2 = m.groups()
    if book not in SEFARIA_BOOK:
        return None
    r = f"{SEFARIA_BOOK[book]}.{ch}.{v1}"
    if v2:
        r += f"-{v2}"
    return r


# ----------------------------------------------------------------- Greek ----
@lru_cache(maxsize=None)
def sblgnt_book(code: str) -> dict[str, str]:
    out = {}
    for line in fetch(SBLGNT_URL.format(code)).splitlines():
        if "\t" in line:
            ref, text = line.split("\t", 1)
            out[ref.strip()] = text.strip()
    return out


GRK_PUNCT = re.compile(r"[\.,;·:!?\"'’‘“”()\[\]⸀⸂⸃⸁⟦⟧—–-]")


def grk_norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = GRK_PUNCT.sub(" ", s).lower()
    s = s.replace("ς", "σ")                           # final sigma
    return re.sub(r"\s+", " ", s).strip()


def sblgnt_text(ref: str) -> str | None:
    m = re.match(r"^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$", ref)
    if not m:
        return None
    book, ch, v1, v2 = m.groups()
    if book not in SBLGNT_BOOK:
        return None
    code = SBLGNT_BOOK[book]
    verses = sblgnt_book(code)
    parts = []
    for v in range(int(v1), int(v2 or v1) + 1):
        key = f"{code} {ch}:{v}"
        if key not in verses:
            return None
        parts.append(verses[key])
    return " ".join(parts)


# ------------------------------------------------------------------ main ----
def check_segments(quoted: str, source: str, norm) -> list[str]:
    """Return list of segments of `quoted` not found in `source`."""
    src = norm(source)
    bad = []
    for seg in quoted.split("..."):
        seg = norm(seg)
        if seg and seg not in src:
            bad.append(seg)
    return bad


def main() -> None:
    pointed = "--pointed" in sys.argv
    entries = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    problems = 0
    skipped = []
    for e in entries:
        src = e["source"]
        sref = to_sefaria_ref(src["ref"])
        if sref is None:
            skipped.append(f"{e['id']}  ({src['ref']})")
        else:
            try:
                vt, text = sefaria(sref)
            except Exception as ex:  # noqa: BLE001
                print(f"!! {e['id']}: Sefaria fetch failed for {sref}: {ex}")
                problems += 1
                continue
            bad = check_segments(src["text"], text, heb_consonants)
            if bad:
                problems += 1
                print(f"XX {e['id']}  {src['ref']}  [{vt}]")
                for b in bad:
                    print(f"     ours : {b}")
                print(f"     source: {heb_consonants(text)}")
            else:
                print(f"ok {e['id']}  {src['ref']}")
            if pointed:
                print(f"     {re.sub(r'<[^>]+>', '', text)}")
        for v in e.get("passage") or []:
            vref = to_sefaria_ref(v["ref"].replace("Psalms ", "Psalm "))
            if vref is None:
                skipped.append(f"{e['id']} passage {v['ref']}")
                continue
            try:
                vt, vtext = sefaria(vref)
            except Exception as ex:  # noqa: BLE001
                print(f"!! {e['id']}: Sefaria fetch failed for {vref}: {ex}")
                problems += 1
                continue
            bad = check_segments(v["text"], vtext, heb_consonants)
            if bad:
                problems += 1
                print(f"XX {e['id']} passage {v['ref']}  [{vt}]")
                for b in bad:
                    print(f"     ours : {b}")
                print(f"     source: {heb_consonants(vtext)}")
            else:
                print(f"ok {e['id']} passage {v['ref']}")
        for f in e.get("fulfilment") or []:
            gt = sblgnt_text(f["ref"])
            if gt is None:
                skipped.append(f"{e['id']} -> {f['ref']}")
                continue
            bad = check_segments(f["text"], gt, grk_norm)
            if bad:
                problems += 1
                print(f"XX {e['id']} -> {f['ref']}  [SBLGNT]")
                for b in bad:
                    print(f"     ours : {b}")
                print(f"     source: {gt}")
            else:
                print(f"ok {e['id']} -> {f['ref']}")
    if skipped:
        print("\nNot checked automatically (verify by hand):")
        for s in skipped:
            print("  ", s)
    print(f"\n{problems} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
