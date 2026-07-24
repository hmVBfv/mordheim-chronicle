# Die Chronik von Mordheim / The Chronicle of Mordheim

A standalone, **bilingual (DE/EN)** Jekyll site for our Mordheim campaign
chronicle, hosted on GitHub Pages as a project site — separate from the
roster-builder repo, so the tool's code and history stay clean.

Live once published:
- German: `https://<your-user>.github.io/mordheim-chronicle/`
- English: `https://<your-user>.github.io/mordheim-chronicle/en/`

No plugins are used, so GitHub Pages builds it automatically (the "Deploy from
a branch" setting). The DE/EN switch in the header always jumps to the matching
translation of the page you are on.

---

## One-time setup

1. Create a **new** empty repository named `mordheim-chronicle`. If you pick a
   different name, change `baseurl` in `_config.yml` to `/<that-name>`.
2. Push these files:
   ```bash
   git init
   git add .
   git commit -m "Chronicle: bilingual scaffold + prologue and first three battles"
   git branch -M main
   git remote add origin https://github.com/<your-user>/mordheim-chronicle.git
   git push -u origin main
   ```
3. GitHub → **Settings → Pages → Deploy from a branch**, branch `main`, folder
   `/ (root)`. Save.
4. Wait ~1 minute, open the live URL.

---

## How the two languages fit together

```
_posts/
  de/  2026-06-14-nebel-ueber-quayside.md      (lang: de, set automatically)
  en/  2026-06-14-fog-over-quayside.md         (lang: en, set automatically)
index.html        -> German home  (/)
en/index.html     -> English home (/en/)
```

- A file's **language, layout and URL prefix come from its folder** (`_posts/de`
  vs `_posts/en`) via `_config.yml` — you don't set them per post.
- Each chapter carries a **`ref`** in its front matter (`prolog`, `battle-1`,
  `battle-2`, `battle-3`). The two language versions of one chapter share the
  same `ref`; that is how the DE/EN switch finds the counterpart. If a
  translation is missing, the switch falls back to the other home page.
- Previous/next navigation stays within one language.

## Adding a new chapter (both languages)

Create two files with the **same `ref`**, one per folder:

`_posts/de/2026-08-01-<deutscher-titel>.md`
```yaml
---
ref: "battle-4"
title: "Titel der Schlacht"
chapter: "Vierte Schlacht"
ic_date: "Sommer 2000 IC"
place: "Ort, Mordheim"
victor: "Wer gewann"
date: 2026-08-01
---
Fließtext ...
```

`_posts/en/2026-08-01-<english-title>.md`
```yaml
---
ref: "battle-4"
title: "Title of the Battle"
chapter: "Fourth Battle"
ic_date: "Summer 2000 IC"
place: "Place, Mordheim"
victor: "Who won"
date: 2026-08-01
---
Prose ...
```

The `date` is the real date (controls order); `ic_date` is the in-fiction date.
Use `### Scene heading` to break a battle into scenes. Commit and push — both
homes, the switch and prev/next update automatically. You can publish one
language first and add the translation later; the `ref` links them once both
exist.

## Working notes (not published)

`notes/campaign-notes.md` holds the single consolidated record behind the
chronicle: roster data, unit descriptions, supplied rules text, canon spellings,
regional origins and a per-battle log with post-battle results, keyed to the same
`ref` values the chapters use (`battle-1`, `battle-2`, …). The folder is listed
in `exclude:` in `_config.yml`, so Jekyll never builds it and it does not appear
on GitHub Pages — it stays in the repo as source material in case the campaign
data is ever reused for something other than prose.

## Update workflow with Claude

Hand over the session notes; Claude writes the chapter as prose in the
chronicle's voice and produces both the German and English file with a matching
`ref`. Drop them into `_posts/de` and `_posts/en`, commit, push.

## Local preview (optional)

```bash
bundle install
bundle exec jekyll serve
# German: http://localhost:4000/mordheim-chronicle/
# English: http://localhost:4000/mordheim-chronicle/en/
```

## Theme

`assets/css/style.css` holds the whole look; all colours are CSS variables at
the top of that file.

## Naming choices across the two languages

Personal names keep their form, including the Empire's Germanic "von"
(*Sir Honnung von Hoiser*). Two warband names differ by language on purpose:
the caravan is *Die Silberne Karavane* (DE) / *The Ardent Caravan* (EN), and the
Lizardmen band is *Kinder des Sotek* (DE) / *Children of Sotek* (EN). Epithets
are translated (*Ulfrik der Pfähler* → *Ulfrik the Impaler*). The Chaos seer's
god is named Tchar, the Great Eagle — the northern-tribe name for Tzeentch.
Adjust to taste.
