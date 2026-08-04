# BreadcrumbList prevod — 15 fajlova

Poslednja stavka sa prijateljeve liste ("velikih"). BreadcrumbList
(mrvice/navigacija u Google rezultatima) je imao engleska imena i
EN URL-ove na svih 5 ne-EN jezika. Sada:

- "Home" -> Главная / Startseite / Ana Sayfa / Головна / Početna
- "Pamukkale Tour" -> Тур в Памуккале / Pamukkale-Tour / Pamukkale Turu / ...
- "Demre · Myra · Kekova Tour" -> lokalizovano
- "Green Canyon Tour" -> lokalizovano
- Svi item URL-ovi sada imaju jezicki prefiks (/ru/, /de/, itd.)

Provereno programski (JSON parsiranje) da su sva imena i URL-ovi
tacno onakvi kakvi treba da budu.

## Kako
Raspakuj u koren repoa (Merge). Prebrisuje 15 fajlova.
git add -A && git commit -m "Translate BreadcrumbList names and localize URLs" && git push

## Sta ostaje sa prijateljeve liste
Samo nova generate-languages.py skripta (najveci, najrizicniji zadatak) —
namerno ostavljen za kasnije, treba pazljivo testiranje da ne pokvari
postojece rucno popravljeno stanje.
