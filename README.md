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
│   ├── graph.md         Mermaid graph generated from the catalogue
│   └── sources.md       texts, editions, and how we cite them
└── .gitattributes       keeps Hebrew/Greek files in UTF-8 with LF endings
```

The YAML file is the single source of truth. The graph and any future website or app are built from it.

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
| `notes` | textual or translation issues |
| `tags` | free keywords |

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
- [ ] Fill in the remaining classic passages (Psalms 2, 16, 22, 69, 110; Isaiah 11, 42, 49, 50, 61; Jeremiah 23, 31; Daniel 7, 9; Hosea 11; Zechariah 11-13; Malachi 3-4)
- [ ] Add Targum / Talmud / Midrash entries as first-class sources, not just notes
- [ ] Add vowel pointing (niqqud) and cantillation to the Hebrew
- [ ] Script to regenerate `docs/graph.md` from the YAML
- [ ] Interactive web graph (click a node, see both languages side by side)
- [ ] Timeline view (prophecy date → fulfilment date)

## Contributing

- Keep original-language text **exact**; quote the edition you copied from.
- Every entry needs the `jewish_reading` field. Disagreement is the point of the project, not a bug.
- Prefer primary sources over apologetics sites in either direction.

## Name

"Meshiach" is a working title.
