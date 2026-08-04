# Balon "samo preko vodica" — sada i za Budzet paket (6 fajlova)

Nastavak prethodnog fixa. "tourDetails.notInc1" (stavka u "Not Included"
listi) je DELJEN kljuc izmedju Premium i Budzet paketa — pojavljuje se
2x u HTML-u (jednom po paketu) ali 1x u prevodima po jeziku.
Jedna izmena je automatski pokrila OBA paketa.

PRE: "Hot air balloon ride (optional – price varies)"
SAD: "Hot air balloon ride (optional, book only through your guide)"

Prevedeno na svih 6 jezika, primenjeno u svih 6 kopija index.html.

Sada "samo preko vodica" poruka postoji na:
1. Price card napomena (Premium)
2. Itinerar dan 2 (oba paketa, opisuje isti dan)
3. "Not Included" lista (Premium I Budzet) <- ovaj fix
4. FAQ (postojalo od ranije)

## Kako
Raspakuj u koren repoa (Replace za index.html fajlove).
git add -A && git commit -m "Balloon: guide-only note now also in Budget package's Not Included list" && git push
