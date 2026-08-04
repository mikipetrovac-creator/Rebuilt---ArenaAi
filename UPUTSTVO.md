# Balon — "samo preko vodica" napomena (6 fajlova)

Ranije je "book via guide on day 1" info postojala SAMO u FAQ.
Gost koji ne otvori FAQ nije znao KAKO da kupi let balonom, niti
da mora iskljucivo preko vodica (zastita od ulicnih prevaranata
u Kapadokiji koji nude "jeftinije" balone).

## Sta je dodato, dva mesta:

1. Price card napomena (Premium paket, odmah pored cene):
   PRE: "Hot air balloon ride sold separately"
   SAD: "Hot air balloon ride sold separately — book only through your guide on day 1"

2. Itinerar, dan 2, stavka o balonu:
   PRE: "Optional: Hot air balloon ride at sunrise"
   SAD: "Optional: Hot air balloon ride at sunrise (book only through your guide)"

Prevedeno na svih 6 jezika (EN/RU/DE/TR/UK/SR), primenjeno u svih 6
kopija index.html (root + 5 jezika), jer svaka nosi kompletan set
prevoda unutar sebe.

## Kako
Raspakuj u koren repoa (Replace za index.html fajlove).
git add -A && git commit -m "Balloon: clarify guide-only booking outside FAQ" && git push
