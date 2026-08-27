# Die Chronik von Mordheim / The Chronicle of Mordheim

A standalone, **bilingual (DE/EN)** Jekyll site for our Mordheim campaign
chronicle, hosted on GitHub Pages as a project site — separate from the
roster-builder repo, so the tool's code and history stay clean.

- German: `https://hmvbfv.github.io/mordheim-chronicle/`
- English: `https://hmvbfv.github.io/mordheim-chronicle/en/`

No plugins are used, so GitHub Pages builds it automatically ("Deploy from a
branch"). The DE/EN switch in the header always jumps to the matching
translation of the page you are on.

---

## What is in here

The chronicle runs in three kinds of post, distinguished by the `kind` field
in the front matter:

| `kind` | Shown in the index as | Image | `victor` |
|---|---|---|---|
| *(none)* — a battle chapter | Roman numeral, I onward | yes, one each | yes |
| `prologue` | an ornament | no | no |
| `interlude` | a small mark, indented and italic | no | no |

Current contents, alternating chapter and interlude:

```
prolog            Auf Flügeln aus Feuer        On Wings of Fire
battle-1     I    Das Urteil im Nebel          The Verdict in the Fog
interlude-1       Der Nebel hebt sich          The Fog Lifts
battle-2     II   Die verbrannten Seiten       The Burned Pages
interlude-2       Die Wochen ohne Zeichen      The Weeks Without a Sign
battle-3     III  Was der Juwelier bezahlte    What the Jeweller Paid
pits-interlude    Was drei Käufer bieten       What Three Buyers Bid
battle-4     IV   Was dreimal aufstand         What Rose Three Times
```

**Chapters** cover one battle. **Interludes** cover the weeks between two
battles — the post-battle sequence told as prose: wounds, recruiting,
purchases, exploration, and why each warband went where it went next. They sit
only *between* battles, never before the first one. Aftermath stays inside the
chapter (the morning after); the interlude carries the weeks after.

---

## How the two languages fit together

```
_posts/
  de/  2026-06-14-das-urteil-im-nebel.md
  en/  2026-06-14-the-verdict-in-the-fog.md
index.html        -> German home  (/)
en/index.html     -> English home (/en/)
assets/img/       -> one 3:2 JPEG per battle chapter
notes/            -> working notes, excluded from the build
```

- A file's **language, layout and URL prefix come from its folder**
  (`_posts/de` vs `_posts/en`) via `_config.yml` — not set per post.
- Both language versions of one post share the same **`ref`**. That is how the
  DE/EN switch finds the counterpart. If a translation is missing the switch
  falls back to the other home page — so always add both.
- `date` must match the date in the filename. It is only a sort key and is
  never displayed; `ic_date` is the in-fiction date and is what readers see.
- Previous/next navigation stays within one language and runs through chapters
  and interludes alike.

---

## Adding a new chapter

Two files with the same `ref`, one per folder:

`_posts/de/2026-09-05-<deutscher-titel>.md`
```yaml
---
ref: "battle-5"
title: "Titel der Schlacht"
chapter: "Fünfte Schlacht"
ic_date: "Herbst 2000 IC"
place: "Ort, Mordheim"
victor: >-
  Ein ganzer Satz darüber, was jede Seite gewonnen oder verloren hat.
image: "dateiname.jpg"
image_alt: "Was auf dem Bild zu sehen ist"
image_caption: "Bildunterschrift"
date: 2026-09-05
---
Fließtext …
```

The English file is identical apart from `title`, `chapter`, `ic_date`,
`place`, `victor` and the two image text fields — `image` points at the same
file, so both languages show the same artwork.

Use `### Szenenüberschrift` to break a battle into scenes. Never use `#` or
`##` in the body; the title comes from the front matter.

## Adding an interlude

As above, plus `kind: "interlude"`, and without `victor` and the image fields.
Give it a `date` a few days before the chapter it leads into, so it sorts into
the right gap.

## Images

One image per battle chapter, none for prologue or interludes. Put the file in
`assets/img/` and name it after the location.

- **3:2, 1600 × 1067, JPEG, under 400 KB.** The same ratio everywhere, or the
  chronicle jumps as you page through it.
- The image sits between the title block and the first paragraph and breaks out
  of the reading column on desktop (52rem against the text's 38rem).
- It shows the **setting and mood only, never the action**. The chapter text
  should agree with what is visible: if the image has a crane on the quay, the
  crane belongs in the prose.

---

## Writing conventions

These are settled and should not drift:

- **"Out of Action" in battle prose means leaving the fight, nothing more.**
  Deaths and lasting injuries appear only in the Aftermath section.
- **Every mechanical advance needs a narrative cause** anchored in that battle,
  that opponent, that character. Go long rather than brief on these.
- **No game terminology in the prose** — no Roster, Henchman, Charge,
  Toughness, skill names. Translate it into narrative language or drop it.
- **Chapter titles are evocative, not descriptive**, and watch for repetition:
  four consecutive titles beginning "Was …" / "What …" read as laziness.
- **The `victor` line is a full sentence** about what each side gained or lost,
  not a bare warband name.
- **The English layer is written, not translated.** No German sentence
  patterns, no calques.
- **Player input is raw outline only** and never lands verbatim in the prose.
- **Nameless dead still get a death.** The lizardmen have no names a human
  could speak, so they are given weight through what they did and how they
  fell, not through biography.

## Naming across the two languages

Personal names keep their form, including the Empire's Germanic "von"
(*Sir Honnung von Hoiser*). Epithets are translated: *Ulfrik der Pfähler* →
*Ulfrik the Impaler*, *Brutvater Qotl* → *Broodfather Qotl*. Two warband names
differ by language on purpose — *Die Silberne Karavane* / *The Ardent Caravan*,
and *Kinder des Sotek* / *Children of Sotek*. *Rangvald's Reavers* keeps the
apostrophe in both languages, since the whole name is English.

In the German text keep **Wyrdstone** (masculine: *der* Wyrdstone),
**Warband** and **Marauder** in English, but vary Warband with *Trupp*,
*Banden* or a description (*Bande von Chaoskriegern*, *Horde Echsenmenschen*)
where the referent is clear. Anything with a German Warhammer equivalent is
translated: *Oger*, *Stammesfürst* / *Anführer* (never *Häuptling*). Skink,
Saurus and Skaven stay as they are. Never write bare *die Kinder* in German —
it reads as human children; use the full name or *Echsenmenschen*.

The Chaos seer's god is Tchar, the Great Eagle — the northern-tribe name for
Tzeentch.

---

## Working notes (not published)

`notes/campaign-notes.md` is the consolidated record behind the chronicle:
roster data, supplied rules text, canon spellings, regional origins and a
per-battle log with post-battle results, keyed to the same `ref` values the
posts use. The folder is in `exclude:` in `_config.yml`, so it never reaches
GitHub Pages.

**Write down who was hired after every session.** Anything not recorded there
cannot be reconstructed later, and the chronicle then has to leave those
sell-swords nameless.

## Update workflow with Claude

Hand over the session notes as a raw outline. Claude writes the chapter as
German literary prose, then rewrites it as native English prose, then the
interlude covering the weeks that lead into it. Drop the files into
`_posts/de` and `_posts/en`, commit, push.

## Local preview

```bash
bundle install
bundle exec jekyll serve
# German: http://localhost:4000/mordheim-chronicle/
# English: http://localhost:4000/mordheim-chronicle/en/
```

## Theme

`assets/css/style.css` holds the whole look; all colours are CSS variables at
the top of the file. Cinzel for display, EB Garamond for text, on a
bone/charcoal palette with wyrdstone green as the single accent.
