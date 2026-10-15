#!/usr/bin/env python3
"""Fill in `source.text_pointed` for every entry from Sefaria's vocalised text.

The pointed text is aligned word-for-word with the consonantal `source.text`
(same number of tokens, "..." preserved), so the viewer can swap between the
two and keep the word glosses attached. Cantillation is stripped; vowels,
dagesh, shin/sin dots and maqaf are kept.

Usage:  python scripts/pointed.py
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify import DATA, heb_consonants, sefaria, to_sefaria_ref  # noqa: E402

CANTILLATION = re.compile(r"[֑-ֽֿ֯׀ׅׄ׆͏​-‏⁠﻿]")
PUNCT = re.compile(r"[{}\[\]()׀|״׳\"'“”:;,.!?—–׃]")


def clean_pointed(s: str) -> str:
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = CANTILLATION.sub("", s)
    s = PUNCT.sub(" ", s)
    s = re.sub(r"[  ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def pointed_units(s: str) -> list[tuple[str, str]]:
    """Split pointed text into (consonantal, pointed) units; maqaf splits a unit
    and stays attached to the first half."""
    out = []
    for word in clean_pointed(s).split():
        if word in ("פ", "ס"):
            continue
        parts = word.split("־")
        for i, p in enumerate(parts):
            if not p:
                continue
            pointed = p + ("־" if i < len(parts) - 1 else "")
            out.append((heb_consonants(p), pointed))
    return out


def align(consonantal: str, units: list[tuple[str, str]]) -> str | None:
    """Return the pointed text aligned token-for-token with `consonantal`."""
    cons = [u[0] for u in units]
    result = []
    pos = 0
    for seg in consonantal.split("..."):
        toks = seg.split()
        if not toks:
            continue
        # find toks as a contiguous run in cons at or after pos
        found = None
        for i in range(pos, len(cons) - len(toks) + 1):
            if cons[i:i + len(toks)] == toks:
                found = i
                break
        if found is None:
            return None
        result.append(" ".join(units[j][1] for j in range(found, found + len(toks))))
        pos = found + len(toks)
    return " ... ".join(result)


def main() -> None:
    text = DATA.read_text(encoding="utf-8")
    entries = yaml.safe_load(text)
    done = 0
    for e in entries:
        src = e["source"]
        sref = to_sefaria_ref(src["ref"])
        if sref is None:
            print(f"-- {e['id']}: no Sefaria ref, skipped")
            continue
        _, raw = sefaria(sref)
        pointed = align(src["text"], pointed_units(raw))
        if pointed is None:
            print(f"XX {e['id']}: could not align")
            continue
        n_c = len(src["text"].split())
        n_p = len(pointed.split())
        assert n_c == n_p, (e["id"], n_c, n_p)
        # splice into the YAML text, after this entry's `    text:` line
        start = text.index(f"\n- id: {e['id']}\n")
        end = text.find("\n- id: ", start + 1)
        end = len(text) if end == -1 else end
        block = text[start:end]
        block = re.sub(r"\n    text_pointed: \"[^\"]*\"", "", block)  # drop old
        m = re.search(r"\n    text: \"[^\"]*\"", block)
        block = block[:m.end()] + f'\n    text_pointed: "{pointed}"' + block[m.end():]
        text = text[:start] + block + text[end:]
        done += 1
        print(f"ok {e['id']}")
    DATA.write_text(text, encoding="utf-8", newline="\n")
    yaml.safe_load(text)  # still valid
    print(f"\n{done} entries pointed")


if __name__ == "__main__":
    main()
