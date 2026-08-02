# Header bug fix — blog-green-canyon-guide (SR + DE)

## Sta je bilo pogresno
U ova dva fajla, header (logo + "nazad" link) je greskom ostao
kopiran iz EN verzije umesto lokalizovan:
  - logo je vodio na "/" umesto na "/sr/" odn. "/de/"
  - "nazad" dugme je pisalo "Tours" umesto "Ture" (sr) / "Touren" (de)

Svi OSTALI blogovi u ta dva jezika su vec bili ispravni — ovo je bio
izolovan copy-paste propust u jednom fajlu po jeziku.

## Sta je ispravljeno (2 fajla, po 2 linije svaki)
- sr/blog-green-canyon-guide.html: href="/sr/", tekst "← Ture"
- de/blog-green-canyon-guide.html: href="/de/", tekst "← Touren"

Nista drugo u fajlovima nije dirano.

## Kako
Raspakuj u koren repoa (Merge), prebrisuje ta 2 fajla.
git add -A && git commit -m "Fix header locale bug in green-canyon blog (SR, DE)" && git push
