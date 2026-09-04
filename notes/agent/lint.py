#!/usr/bin/env python3
"""Prueft die maschinell pruefbaren Konventionen der Mordheim-Chronik.

Quelle der Regeln: README.md (Writing conventions, Naming across the two
languages, Adding a new chapter) und die Verbotsliste aus den Stilvorgaben.

Aufruf aus dem Repo-Wurzelverzeichnis:
    python3 notes/agent/lint.py            # prueft beide Sprachen
    python3 notes/agent/lint.py de         # nur Deutsch

Exit 0 = keine Funde, 1 = Funde, 2 = Aufrufproblem.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
POSTS = WURZEL / "_posts"
BILDER = WURZEL / "assets" / "img"
BILD_MAX = 400 * 1024

# --- Schreibweisen: Muster -> was stattdessen richtig ist --------------------

SCHREIBWEISEN = {
    r"\bMarkus\b": "Marcus",
    r"\bStyrkar\b(?!r)": "Styrkarr",
    r"\bWyrdstein\w*": "Wyrdstone",
    r"\b(?:die|das) Wyrdstone\b": "der Wyrdstone (maskulin)",
    r"\b(?:die|das) Bleiche\b": "der Bleiche (maskulin)",
    r"\bH(?:ä|ae)uptling\w*": "Stammesfuerst oder Anfuehrer",
    r"\bTzeentch\b": "Tchar (Name der Nordstaemme)",
}

# --- Begriffe, die nur in einer Sprachfassung vorkommen duerfen --------------

NUR_DEUTSCH = [
    "Silberne Karavane", "Ulfrik der Pfähler", "Brutvater Qotl",
    "Kinder des Sotek", "Stammesfürst", "Echsenmenschen",
]
NUR_ENGLISCH = [
    "Ardent Caravan", "Ulfrik the Impaler", "Broodfather Qotl",
    "Children of Sotek",
]

KUTTE_OK = re.compile(r"(?:dem|den|der|des)?\s*Mann(?:es)?\s+in\s+der\s+Kutte")
DATUM_IM_NAMEN = re.compile(r"^(\d{4}-\d{2}-\d{2})-")


# --- Front Matter -----------------------------------------------------------

def front_matter(text: str) -> tuple[dict[str, str], str]:
    """Zerlegt in Kopf und Rumpf. Bewusst simpel: die Chronik nutzt nur
    'key: wert' und gefaltete Bloecke mit '>-'."""
    if not text.startswith("---"):
        return {}, text

    teile = text.split("---", 2)
    if len(teile) < 3:
        return {}, text

    kopf: dict[str, str] = {}
    letzter = None
    for zeile in teile[1].splitlines():
        if not zeile.strip():
            continue
        if zeile.startswith((" ", "\t")) and letzter:
            kopf[letzter] += " " + zeile.strip()
            continue
        if ":" not in zeile:
            continue
        schluessel, _, wert = zeile.partition(":")
        letzter = schluessel.strip()
        kopf[letzter] = wert.strip().strip('"').lstrip(">-").strip()

    return kopf, teile[2]


def spielbegriffe() -> list[str]:
    datei = Path(__file__).resolve().parent / "spielbegriffe.txt"
    if not datei.exists():
        return []
    return [z.strip() for z in datei.read_text(encoding="utf-8").splitlines()
            if z.strip() and not z.startswith("#")]


# --- Pruefungen pro Datei ---------------------------------------------------

def pruefe_kopf(pfad: Path, kopf: dict[str, str]) -> list[str]:
    funde = []

    def melde(was: str):
        funde.append(f"{pfad.relative_to(WURZEL)}: {was}")

    if "ref" not in kopf:
        melde("kein ref — die Sprachumschaltung findet die Gegenseite nicht")

    treffer = DATUM_IM_NAMEN.match(pfad.name)
    if treffer and kopf.get("date", "")[:10] != treffer.group(1):
        melde(f"date '{kopf.get('date', '')}' passt nicht zum Dateinamen "
              f"({treffer.group(1)})")

    art = kopf.get("kind", "")

    if art == "interlude":
        for feld in ("victor", "image", "image_alt", "image_caption"):
            if feld in kopf:
                melde(f"Zwischenspiel hat '{feld}' — gehoert nur ins Schlachtkapitel")

    elif art == "":
        for feld in ("victor", "chapter", "ic_date", "place",
                     "image", "image_alt", "image_caption"):
            if feld not in kopf:
                melde(f"Schlachtkapitel ohne '{feld}'")

        victor = kopf.get("victor", "")
        if victor:
            if not victor.rstrip().endswith((".", "!", "?")):
                melde("victor ist kein ganzer Satz (kein Schlusszeichen)")
            elif len(victor.split()) < 8:
                melde(f"victor wirkt zu knapp ({len(victor.split())} Woerter) — "
                      "erwartet ist ein ganzer Satz pro Seite")

        bild = kopf.get("image", "")
        if bild:
            datei = BILDER / bild
            if not datei.exists():
                melde(f"Bild fehlt: assets/img/{bild}")
            elif datei.stat().st_size > BILD_MAX:
                melde(f"Bild zu gross: {bild} "
                      f"({datei.stat().st_size // 1024} KB, erlaubt sind 400)")

    return funde


def pruefe_rumpf(pfad: Path, rumpf: str, sprache: str,
                 begriffe: list[str]) -> list[str]:
    funde = []
    kurz = pfad.relative_to(WURZEL)

    def melde(nr: int, zeile: str, was: str, treffer: "re.Match | None" = None):
        """Zeigt einen Ausschnitt um die Fundstelle, nicht immer den
        Zeilenanfang — sonst ist bei langen Zeilen nie zu sehen, was
        eigentlich getroffen hat."""
        if treffer is not None:
            mitte = treffer.start()
            start = max(0, mitte - 40)
            ende = min(len(zeile), mitte + 70)
            ausschnitt = zeile[start:ende].strip()
            praefix = "…" if start > 0 else ""
            suffix = "…" if ende < len(zeile) else ""
            ausschnitt = f"{praefix}{ausschnitt}{suffix}"
        else:
            ausschnitt = zeile.strip()[:110]
        funde.append(f"{kurz}:{nr}: {was}\n    {ausschnitt}")

    fremd = NUR_ENGLISCH if sprache == "de" else NUR_DEUTSCH

    for nr, zeile in enumerate(rumpf.splitlines(), start=1):
        if re.match(r"^#{1,2}(?!#)", zeile):
            melde(nr, zeile, "nur '###' im Fliesstext, der Titel kommt aus dem Kopf")

        for begriff in begriffe:
            treffer = re.search(rf"\b{re.escape(begriff)}\b", zeile, re.IGNORECASE)
            if treffer:
                melde(nr, zeile, f"Spielbegriff in der Prosa: {begriff}", treffer)

        treffer = re.search(r"\?", zeile)
        if treffer:
            melde(nr, zeile, "Fragezeichen — rhetorische Frage? (pruefen)", treffer)

        treffer = re.search(r"(?<!\d)\d{1,2}(?!\d)", zeile)
        if treffer:
            melde(nr, zeile, "Ziffer — Ungefaehres statt Zahlenpraezision (pruefen)",
                  treffer)
            # 3+ stellige Zahlen (Jahre wie 1999) sind bewusst ausgenommen:
            # eine Kalenderangabe ist kein Fall fuer "ein halbes Dutzend".

        for muster, richtig in SCHREIBWEISEN.items():
            treffer = re.search(muster, zeile)
            if treffer:
                melde(nr, zeile, f"Schreibweise: erwartet {richtig}", treffer)

        treffer = re.search(r"\bdie Kinder\b(?!\s+des\s+Sotek)", zeile)
        if sprache == "de" and treffer:
            melde(nr, zeile, "bloss 'die Kinder' — liest sich als Menschenkinder",
                  treffer)

        if "Kutte" in zeile and not KUTTE_OK.search(zeile):
            treffer = re.search("Kutte", zeile)
            melde(nr, zeile, "'Kutte' ausserhalb der festgelegten Wendung", treffer)

        for begriff in fremd:
            treffer = re.search(re.escape(begriff), zeile)
            if treffer:
                melde(nr, zeile, f"Begriff der anderen Sprachfassung: {begriff}",
                      treffer)

    return funde


# --- Pruefungen ueber alle Dateien hinweg -----------------------------------

def pruefe_refs(koepfe: dict[str, dict[str, dict[str, str]]]) -> list[str]:
    """Jeder ref braucht beide Sprachfassungen."""
    funde = []
    de = {k.get("ref") for k in koepfe["de"].values() if k.get("ref")}
    en = {k.get("ref") for k in koepfe["en"].values() if k.get("ref")}
    for ref in sorted(de - en):
        funde.append(f"ref '{ref}': englische Fassung fehlt — "
                     "der Umschalter faellt auf die Startseite zurueck")
    for ref in sorted(en - de):
        funde.append(f"ref '{ref}': deutsche Fassung fehlt")
    return funde


def pruefe_titel(koepfe: dict[str, dict[str, str]], sprache: str) -> list[str]:
    """Vier aufeinanderfolgende Titel mit demselben ersten Wort lesen sich
    als Faulheit (README)."""
    funde = []
    sortiert = sorted(koepfe.items(), key=lambda p: p[0])
    titel = [(name, k.get("title", "")) for name, k in sortiert]

    for i in range(len(titel) - 2):
        fenster = titel[i:i + 3]
        erste = [t.split()[0].lower() for _, t in fenster if t.split()]
        if len(erste) == 3 and len(set(erste)) == 1:
            namen = ", ".join(n for n, _ in fenster)
            funde.append(f"[{sprache}] drei Titel in Folge beginnen mit "
                         f"'{erste[0]}': {namen}")
    return funde


# --- Hauptprogramm ----------------------------------------------------------

def main() -> int:
    sprachen = [sys.argv[1]] if len(sys.argv) > 1 else ["de", "en"]
    for s in sprachen:
        if s not in ("de", "en"):
            print("Aufruf: lint.py [de|en]")
            return 2

    begriffe = spielbegriffe()
    funde: list[str] = []
    koepfe: dict[str, dict[str, dict[str, str]]] = {"de": {}, "en": {}}

    for sprache in ("de", "en"):
        verzeichnis = POSTS / sprache
        if not verzeichnis.is_dir():
            print(f"Verzeichnis fehlt: {verzeichnis}")
            return 2
        for pfad in sorted(verzeichnis.glob("*.md")):
            kopf, rumpf = front_matter(pfad.read_text(encoding="utf-8"))
            koepfe[sprache][pfad.name] = kopf
            if sprache in sprachen:
                funde += pruefe_kopf(pfad, kopf)
                funde += pruefe_rumpf(pfad, rumpf, sprache, begriffe)

    funde += pruefe_refs(koepfe)
    for sprache in sprachen:
        funde += pruefe_titel(koepfe[sprache], sprache)

    if funde:
        print(f"{len(funde)} Fund(e):\n")
        print("\n".join(funde))
        return 1

    print("Keine Funde.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
