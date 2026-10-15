#!/usr/bin/env python3
"""Print a YAML `passage:` skeleton for a range of verses, with consonantal and
pointed Hebrew from Sefaria. English and glosses are then filled in by hand.

Usage:  python scripts/fetch_passage.py "Isaiah 52:13-53:12"
        python scripts/fetch_passage.py "Psalms 22"
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pointed import clean_pointed, pointed_units  # noqa: E402
from verify import heb_consonants, fetch  # noqa: E402
import json, urllib.parse  # noqa: E402


def verses(ref: str) -> list[tuple[str, str]]:
    url = "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref) + "?return_format=text_only"
    d = json.loads(fetch(url))
    v = d["versions"][0]
    text = v["text"]
    book = d["book"]
    # sections: for a single chapter, text is a list of verses; for ranges across
    # chapters, a list of lists.
    out = []
    start_ch = int(d["sections"][0])
    start_v = int(d["sections"][1]) if len(d["sections"]) > 1 else 1
    if text and isinstance(text[0], list):
        for ci, chapter in enumerate(text):
            ch = start_ch + ci
            v0 = start_v if ci == 0 else 1
            for vi, verse in enumerate(chapter):
                out.append((f"{book} {ch}:{v0 + vi}", verse))
    else:
        for vi, verse in enumerate(text):
            out.append((f"{book} {start_ch}:{start_v + vi}", verse))
    return out


def main() -> None:
    ref = sys.argv[1]
    print("  passage:")
    for vref, raw in verses(ref):
        units = pointed_units(raw)
        cons = " ".join(u[0] for u in units)
        pointed = " ".join(u[1] for u in units)
        print(f"    - ref: {vref}")
        print(f'      text: "{cons}"')
        print(f'      text_pointed: "{pointed}"')
        print(f'      english: ""')


if __name__ == "__main__":
    main()
