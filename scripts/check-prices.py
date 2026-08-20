#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/check-prices.py

Usage:
    python scripts/check-prices.py

Purpose:
    Safety net for the Cappadocia tour price bug found & fixed on 2026-08-20
    (stale "Budget €35 / Premium €90" left behind on the excursion hub pages
    across all 6 languages, while the Cappadocia page itself already showed
    the correct "Budget €50 / Premium €100"). Run this before every deploy
    to catch the same class of regression automatically.

Canonical Cappadocia prices (as of 2026-08-20):
    Budget adult:            EUR 50
    Premium adult:           EUR 100
    Budget child (4-10):     EUR 25
    Premium child (4-10):    EUR 50
    Infant (0-3):            free, no separate seat

Explicitly NOT flagged (legitimate, unrelated prices that happen to share
a number with an old stale Cappadocia value):
    - EUR 35 "Balloon Panorama" optional add-on (NOT included in tour price)
    - EUR 15 single-room supplement (Cappadocia FAQ / Not Included list)
    - Any other tour's own price (Pamukkale, Demre-Myra-Kekova, Green Canyon)

Scope:
    Scans the Cappadocia-price-bearing pages only (the ones that actually
    quote a Cappadocia tour price): the Cappadocia page itself and the two
    excursion hub pages, in the English root and all 5 translated folders.
    Other tour pages (pamukkale.html, demre-myra-kekova.html,
    green-canyon.html, blog posts, etc.) are intentionally out of scope for
    THIS script, since they do not carry Cappadocia's own price figures.

Exit status:
    0  -> no stale prices found
    1  -> at least one stale price found (prints a report)
"""

import os
import sys

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANG_DIRS = ["", "ru/", "de/", "tr/", "uk/", "sr/"]
PAGES = ["index.html", "excursions-from-alanya.html", "excursions-from-side.html"]

# ---------------------------------------------------------------------------
# 1) FORBIDDEN: substrings that must NEVER appear anywhere in the scanned
#    files. These are the exact stale strings found & fixed on 2026-08-20.
#    If any of these come back (e.g. from an old branch, a bad merge, or a
#    careless manual edit), the script fails loudly.
# ---------------------------------------------------------------------------
FORBIDDEN_PATTERNS = [
    # --- stale Budget €35 (should be €50) ---
    "Cappadocia from €35",
    "Cappadocia €35.",
    "The 2-day Cappadocia tour starts at €35 per adult in the budget package.",
    "Каппадокия от €35",
    "Каппадокия €35.",
    "Двухдневный тур в Каппадокию — от €35 за взрослого в бюджетном пакете.",
    "Двухдневный тур в Каппадокию — от €35 со взрослого в бюджетном пакете.",
    "Kappadokien ab 35 €",
    "Kappadokien 35 €.",
    "Die 2-Tages-Tour nach Kappadokien beginnt bei 35 € pro Erwachsenem im Budget-Paket.",
    "Kapadokya €35'ten",
    "Kapadokya 35 €.",
    "2 günlük Kapadokya turu bütçe paketinde yetişkin başına €35'ten başlar.",
    "2 günlük Kapadokya turu ekonomik pakette yetişkin başına 35 €'dan başlar.",
    "Каппадокія від €35",
    "Каппадокія €35.",
    "Дводенний тур до Каппадокії — від €35 за дорослого в бюджетному пакеті.",
    "Дводенний тур у Каппадокію — від €35 з дорослого в бюджетному пакеті.",
    "Kapadokija od €35",
    "Kapadokija €35.",
    "Dvodnevna tura u Kapadokiju počinje od €35 po odrasloj osobi u budžet paketu.",
    '<td class="price">€35<small>From</small></td>',
    '<td class="price">€35<small>От</small></td>',
    '<td class="price">€35<small>Ab</small></td>',
    '<td class="price">35 €<small>Ab</small></td>',
    '<td class="price">€35<small>Başlangıç</small></td>',
    '<td class="price">35 €<small>Başlangıç</small></td>',
    '<td class="price">€35<small>Від</small></td>',
    '<td class="price">€35<small>Od</small></td>',

    # --- stale Premium €90 (should be €100) ---
    '<td class="prem">€90</td>',
    '<td class="prem">90 €</td>',

    # --- stale pricing.js object / product schema (if ever regressed) ---
    "budget: { adult: 35",
    "premium: { adult: 90",
    '"price": "35"',
]

# ---------------------------------------------------------------------------
# 2) REQUIRED: golden-value assertions. Each entry says "this exact
#    substring MUST be present in this exact file" -- proves the correct
#    price is actually there, not just that the stale one is absent.
#    Keyed by relative file path.
# ---------------------------------------------------------------------------
REQUIRED_PATTERNS = {
    "index.html": [
        "premium: { adult: 100, child: 50 }",
        "budget: { adult: 50, child: 25 }",
        # Balloon Panorama add-on must stay at its own, unrelated €35 --
        # if this goes missing it means someone "fixed" it by mistake.
        "Balloon panorama – €35",
    ],
    "ru/index.html": [
        "premium: { adult: 100, child: 50 }",
        "budget: { adult: 50, child: 25 }",
        "Панорама шаров – €35",
    ],
    "de/index.html": [
        "premium: { adult: 100, child: 50 }",
        "budget: { adult: 50, child: 25 }",
        "Ballonpanorama – €35",
    ],
    "tr/index.html": [
        "premium: { adult: 100, child: 50 }",
        "budget: { adult: 50, child: 25 }",
        "Balon panoraması – €35",
    ],
    "uk/index.html": [
        "premium: { adult: 100, child: 50 }",
        "budget: { adult: 50, child: 25 }",
        "Панорама куль – €35",
    ],
    "sr/index.html": [
        "premium: { adult: 100, child: 50 }",
        "budget: { adult: 50, child: 25 }",
        "Panorama balona – €35",
    ],

    "excursions-from-alanya.html": [
        "Cappadocia from €50",
        "The 2-day Cappadocia tour starts at €50 per adult in the budget package.",
        '<td class="price">€50<small>From</small></td>',
        '<td class="prem">€100</td>',
    ],
    "excursions-from-side.html": [
        "Cappadocia €50.",
        "The 2-day Cappadocia tour starts at €50 per adult in the budget package.",
        '<td class="price">€50<small>From</small></td>',
        '<td class="prem">€100</td>',
    ],
    "ru/excursions-from-alanya.html": [
        "Каппадокия от €50",
        "Двухдневный тур в Каппадокию — от €50 за взрослого в бюджетном пакете.",
        '<td class="price">€50<small>От</small></td>',
        '<td class="prem">€100</td>',
    ],
    "ru/excursions-from-side.html": [
        "Каппадокия €50.",
        "Двухдневный тур в Каппадокию — от €50 со взрослого в бюджетном пакете.",
        '<td class="price">€50<small>От</small></td>',
        '<td class="prem">€100</td>',
    ],
    "de/excursions-from-alanya.html": [
        "Kappadokien ab 50 €",
        "Die 2-Tages-Tour nach Kappadokien beginnt bei 50 € pro Erwachsenem im Budget-Paket.",
        '<td class="price">€50<small>Ab</small></td>',
        '<td class="prem">€100</td>',
    ],
    "de/excursions-from-side.html": [
        "Kappadokien 50 €.",
        "Die 2-Tages-Tour nach Kappadokien beginnt bei 50 € pro Erwachsenem im Budget-Paket.",
        '<td class="price">50 €<small>Ab</small></td>',
        '<td class="prem">100 €</td>',
    ],
    "tr/excursions-from-alanya.html": [
        "Kapadokya €50'den",
        "2 günlük Kapadokya turu bütçe paketinde yetişkin başına €50'den başlar.",
        '<td class="price">€50<small>Başlangıç</small></td>',
        '<td class="prem">€100</td>',
    ],
    "tr/excursions-from-side.html": [
        "Kapadokya 50 €.",
        "2 günlük Kapadokya turu ekonomik pakette yetişkin başına 50 €'dan başlar.",
        '<td class="price">50 €<small>Başlangıç</small></td>',
        '<td class="prem">100 €</td>',
    ],
    "uk/excursions-from-alanya.html": [
        "Каппадокія від €50",
        "Дводенний тур до Каппадокії — від €50 за дорослого в бюджетному пакеті.",
        '<td class="price">€50<small>Від</small></td>',
        '<td class="prem">€100</td>',
    ],
    "uk/excursions-from-side.html": [
        "Каппадокія €50.",
        "Дводенний тур у Каппадокію — від €50 з дорослого в бюджетному пакеті.",
        '<td class="price">€50<small>Від</small></td>',
        '<td class="prem">€100</td>',
    ],
    "sr/excursions-from-alanya.html": [
        "Kapadokija od €50",
        "Dvodnevna tura u Kapadokiju počinje od €50 po odrasloj osobi u budžet paketu.",
        '<td class="price">€50<small>Od</small></td>',
        '<td class="prem">€100</td>',
    ],
    "sr/excursions-from-side.html": [
        "Kapadokija €50.",
        "Dvodnevna tura u Kapadokiju počinje od €50 po odrasloj osobi u budžet paketu.",
        '<td class="price">€50<small>Od</small></td>',
        '<td class="prem">€100</td>',
    ],
}


def scanned_files():
    files = []
    for lang in LANG_DIRS:
        for page in PAGES:
            rel = lang + page
            abs_path = os.path.join(SITE_ROOT, rel)
            if os.path.isfile(abs_path):
                files.append(rel)
    return files


def main():
    files = scanned_files()
    if not files:
        print("ERROR: no files found to scan under", SITE_ROOT)
        return 1

    problems = []

    for rel in files:
        abs_path = os.path.join(SITE_ROOT, rel)
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()

        for pattern in FORBIDDEN_PATTERNS:
            if pattern in content:
                problems.append(f"[STALE PRICE FOUND]  {rel}\n    contains forbidden text: {pattern!r}")

        for pattern in REQUIRED_PATTERNS.get(rel, []):
            if pattern not in content:
                problems.append(f"[MISSING GOLDEN VALUE]  {rel}\n    expected but not found: {pattern!r}")

    print(f"Scanned {len(files)} file(s):")
    for rel in files:
        print(f"  - {rel}")
    print()

    if problems:
        print(f"FAILED — {len(problems)} problem(s) found:\n")
        for p in problems:
            print(p)
            print()
        print("Canonical Cappadocia prices: Budget adult €50 / Premium adult €100 / "
              "Budget child €25 / Premium child €50 / Infant free.")
        print("€35 (Balloon Panorama) and €15 (single-room supplement) are legitimate "
              "and are not flagged.")
        return 1

    print("OK — no stale Cappadocia prices found. All golden values present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
