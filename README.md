# Meshiach (מָשִׁיחַ)

An open, source-first study of **Jesus of Nazareth read as the Jewish Messiah**: a catalogue of the prophecies, types, and future-oriented passages in the Hebrew Bible (Tanakh / Old Testament) and other Jewish writings that have been understood as pointing to him, with the **original-language text and an English rendering side by side**, and a **visual graph** linking each passage to its claimed fulfilment.

> *Meshiach* is the Hebrew מָשִׁיחַ, "anointed one". Greek Χριστός (Christos), English "Christ", is a translation of the same word.

## Goals

1. **Catalogue** every passage in the Tanakh, Torah, Targumim, Dead Sea Scrolls, Talmud, Midrash, and related Jewish literature that has been read messianically or applied to Jesus.
2. **Show the text in its original language** (Hebrew, Aramaic, or Greek) next to English, so a reader can check the wording rather than trust a paraphrase.
3. **Link** each passage to the New Testament text (Greek) that claims or implies its fulfilment.
4. **Record how Jewish tradition reads the same passage**, so the project is a fair comparison and not a one-sided proof text list.
5. **Visualise** the whole web of connections as a graph: themes → prophecies → fulfilments → sources.

## Layout

```
meshiach/
├── README.md            this file
├── data/
│   └── prophecies.yaml  the catalogue (one entry per passage)
├── docs/
│   ├── graph.md         Mermaid graph, generated from the catalogue
│   └── sources.md       texts, editions, and how we cite them
├── scripts/
│   ├── build.py         regenerates docs/graph.md and web/data.js from the YAML
│   └── verify.py        checks every quotation against Sefaria and SBLGNT
├── web/
│   ├── index.html       interactive graph viewer (open directly in a browser)
│   └── data.js          generated; do not edit
└── .gitattributes       keeps Hebrew/Greek files in UTF-8 with LF endings
```

The YAML file is the single source of truth. The Mermaid graph and the web viewer are built from it:

```bash
python scripts/build.py
```

To check every Hebrew, Aramaic and Greek quotation against its published edition (Sefaria for the Tanakh, Targum and Talmud; SBLGNT for the New Testament):

```bash
python scripts/verify.py
```

Then open `web/index.html` in a browser. Click a node to see the original text and English side by side; hover a word that has a gloss to see its meaning.

## Entry format

Each prophecy is one YAML record:

```yaml
- id: isa-7-14
  theme: birth
  title: Born of the almah / virgin
  source:
    ref: Isaiah 7:14
    lang: he
    text: "לכן יתן אדני הוא לכם אות הנה העלמה הרה וילדת בן וקראת שמו עמנו אל"
    english: "Therefore the Lord himself will give you a sign: behold, the almah shall conceive and bear a son, and shall call his name Immanuel."
  fulfilment:
    - ref: Matthew 1:22-23
      lang: el
      text: "Ἰδοὺ ἡ παρθένος ἐν γαστρὶ ἕξει καὶ τέξεται υἱόν, καὶ καλέσουσιν τὸ ὄνομα αὐτοῦ Ἐμμανουήλ"
      english: "Behold, the virgin shall conceive and bear a son, and they shall call his name Emmanuel."
  jewish_reading: "Rashi and most rabbinic readers take the sign as fulfilled in Isaiah's own day (a young woman, Hebrew almah, not necessarily a virgin); the LXX translators chose parthenos."
  notes: "Hebrew almah vs Greek parthenos is the crux; the LXX predates Christianity."
  tags: [immanuel, septuagint]
```

Fields:

| field | meaning |
|---|---|
| `id` | stable slug, `book-chapter-verse` |
| `theme` | one of the graph groupings: `lineage`, `birth`, `forerunner`, `ministry`, `suffering`, `death`, `resurrection`, `exaltation`, `covenant`, `kingdom`, `return` |
| `source` | the Jewish text: reference, language code (`he` Hebrew, `arc` Aramaic, `el` Greek), original text, English |
| `fulfilment` | list of New Testament passages (Greek + English) that cite or allude to it |
| `jewish_reading` | how classical Jewish interpretation (Targum, Talmud, Rashi, Radak, etc.) takes the passage |
| `christian_reading` | how Christian interpretation takes the passage and why it is applied to Jesus |
| `notes` | textual or translation issues |
| `tags` | free keywords |
| `words` | optional per-word glosses for the original text (see below) |
| `relates_to` | ids of other entries this one comments on (used by Targum/Talmud/Qumran entries) |
| `source.kind` | `tanakh` (default), `targum`, `talmud`, `midrash`, `qumran` |

### Word-level glosses

Entries may carry a `words` list, one item per word of `source.text`, in order. This drives the hover feature in the web graph: hover a Hebrew or Greek word to see its dictionary meaning and its meaning in this sentence. Where Jewish and Christian tradition read the word differently in context, both are given.

```yaml
  words:
    - w: העלמה
      lemma: עַלְמָה
      gloss: "young woman of marriageable age"
      context: "the specific young woman known to Isaiah and Ahaz"
      readings:
        jewish: "a young woman; virginity is neither asserted nor denied (that word would be בתולה)"
        christian: "a virgin, following the Septuagint's παρθένος and Matthew 1:23"
```

| field | meaning |
|---|---|
| `w` | the word exactly as it appears in `source.text` |
| `lemma` | dictionary form, pointed |
| `gloss` | plain dictionary meaning |
| `context` | what it means in this sentence, where both traditions agree |
| `readings` | `jewish` and `christian` contextual meanings, only when they differ |

Verse numbers follow the **Hebrew (Masoretic) numbering**; where Christian Bibles differ, the English number is given in brackets, e.g. `Psalm 22:17 [16]`.

## Side-by-side sample

| Ref | Original | English | NT fulfilment |
|---|---|---|---|
| Genesis 3:15 | ואיבה אשית בינך ובין האשה ובין זרעך ובין זרעה הוא ישופך ראש ואתה תשופנו עקב | I will put enmity between you and the woman, and between your seed and her seed; he shall bruise your head, and you shall bruise his heel. | Romans 16:20; Galatians 4:4 |
| Genesis 49:10 | לא יסור שבט מיהודה ומחקק מבין רגליו עד כי יבא שילה ולו יקהת עמים | The sceptre shall not depart from Judah, nor the ruler's staff from between his feet, until Shiloh comes; and to him shall be the obedience of the peoples. | Hebrews 7:14; Revelation 5:5 |
| Micah 5:1 [2] | ואתה בית לחם אפרתה צעיר להיות באלפי יהודה ממך לי יצא להיות מושל בישראל ומוצאתיו מקדם מימי עולם | But you, Bethlehem Ephrathah, small among the clans of Judah, from you shall come forth for me one who is to be ruler in Israel, whose origins are from of old, from ancient days. | Matthew 2:5-6 |
| Isaiah 53:5 | והוא מחלל מפשענו מדכא מעונתינו מוסר שלומנו עליו ובחברתו נרפא לנו | But he was pierced for our transgressions, crushed for our iniquities; the chastisement of our peace was upon him, and by his wounds we are healed. | 1 Peter 2:24 |
| Zechariah 9:9 | גילי מאד בת ציון הריעי בת ירושלם הנה מלכך יבוא לך צדיק ונושע הוא עני ורכב על חמור ועל עיר בן אתנות | Rejoice greatly, daughter of Zion; shout, daughter of Jerusalem. Behold, your king comes to you; righteous and victorious is he, humble and riding on a donkey, on a colt, the foal of a donkey. | Matthew 21:4-5; John 12:14-15 |

Full list: [data/prophecies.yaml](data/prophecies.yaml). Graph: [docs/graph.md](docs/graph.md).

## Sources we draw on

- **Tanakh**: Masoretic Text (Westminster Leningrad Codex), with the Septuagint (LXX) and Dead Sea Scrolls noted where they differ.
- **Targumim**: Targum Onkelos, Targum Jonathan (e.g. Targum Jonathan on Isaiah 52:13 explicitly names "my servant the Messiah").
- **Talmud and Midrash**: e.g. Sanhedrin 98a-b (the Messiah's coming, "Bar Nafle"), Sukkah 52a (Messiah ben Joseph, Zechariah 12:10), Pesikta Rabbati 36-37 (the suffering Messiah Ephraim).
- **Medieval commentators**: Rashi, Ibn Ezra, Radak, Ramban, for the traditional Jewish readings.
- **New Testament**: Greek (SBLGNT / NA28 wording).

See [docs/sources.md](docs/sources.md) for editions and licensing.

## Roadmap

- [x] Repo, data format, first entries, first graph
- [x] Fill in the classic passages (Psalms 2, 16, 22, 69, 110; Isaiah 7, 9, 11, 40, 42, 49, 50, 53, 61; Jeremiah 23, 31; Daniel 7, 9; Hosea 11; Micah 5; Zechariah 9, 11-13; Malachi 3)
- [x] Add Targum / Talmud / Qumran entries as first-class sources, not just notes
- [x] Script to regenerate `docs/graph.md` and the web data from the YAML
- [x] Interactive web graph (click a node, see both languages side by side)
- [ ] **Word hover**: hovering a word of the original text shows (a) the word's translation and (b) its meaning in the context of the sentence. Where Jewish and Christian tradition differ on the contextual meaning, both are shown. The `words` field and the web viewer already support this; the work is filling in glosses for every entry.
- [ ] Add vowel pointing (niqqud) and cantillation to the Hebrew
- [ ] Catalogue whole passages, not single verses (Isaiah 52:13-53:12, Psalm 22 entire, Daniel 9:24-27)
- [ ] Midrash entries (Pesikta Rabbati 36-37, Midrash Tehillim)
- [ ] Timeline view (prophecy date → fulfilment date)

## Contributing

- Keep original-language text **exact**; quote the edition you copied from, and run `scripts/verify.py` before committing.
- Every entry needs the `jewish_reading` field. Disagreement is the point of the project, not a bug.
- Prefer primary sources over apologetics sites in either direction.

## Name

"Meshiach" is a working title.
