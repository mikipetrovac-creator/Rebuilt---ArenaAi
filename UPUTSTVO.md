# Schema fixovi (prijateljeve 3 tacke) — 22 fajla

Sve tri potvrdjene, mehanicke/prevodilacke izmene primenjene zajedno
na 4 ture x 5 jezika (ru/de/tr/uk/sr) + 2 header bug fajla.

## 1. OG locale duplikat (20 fajlova)
Primarni jezik se vise ne pojavljuje i kao og:locale i kao
og:locale:alternate. Uklonjen samo dupli red, ostala 4 prava
alternate-a netaknuta.

## 2. Product offers.url lokalizacija (20 fajlova)
"offers": {..., "url": "https://myvalanyatravel.com/pamukkale"}
je bilo isto za sve jezike (EN putanja). Sada:
  ru -> https://myvalanyatravel.com/ru/pamukkale
  de -> https://myvalanyatravel.com/de/pamukkale
  itd.
TravelAgency.url (identifikuje firmu) NIJE dirano — ostaje domen bez jezika,
sto je ispravno.

## 3. Product name/description prevod (20 fajlova, 40 prevoda)
Schema naziv i opis ture su bili na engleskom u svih 5 ne-EN jezika.
Sada prevedeni na jezik stranice (ru/de/tr/uk/sr), prirodnim
tekstom u stilu ostatka sajta.

## 4. Header bug (2 fajla, iz prosle runde, ponovo ukljuceno)
sr/blog-green-canyon-guide.html i de/blog-green-canyon-guide.html —
logo i "nazad" link lokalizovani.

## Sta NIJE dirano
- EN verzija (izvor, ostaje netaknuta)
- BreadcrumbList (prijateljeva tvrdnja da fali na 3/4 ture je bila netacna —
  postoji na Pamukkale/Demre/Green Canyon, samo index.html nema sto je OK)
- TravelAgency.url, TURSAB pisanje, WhatsApp brojevi — provereno, nisu bili
  stvarni problemi

## Kako
Raspakuj u koren repoa (Merge). Prebrisuje 22 fajla u ru/de/tr/uk/sr folderima.
git add -A && git commit -m "Schema: translate Product name/desc, localize offers.url, fix OG locale dup, header bug" && git push

## Napomena
Ne zaboravi da si ranije obrisao mnt/ folder (ako jos nisi) i proverio
da li je bio live -- to je odvojeno od ovog paketa.
