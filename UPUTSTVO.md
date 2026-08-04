# Sitni tehnicki fixovi — 33 fajla

## 1. mainEntityOfPage .html mismatch (30 fajlova: 5 blogova x 6 jezika)
Article schema je imala "mainEntityOfPage" sa .html na kraju, dok je
canonical (tacan URL) bio bez .html. Sada se poklapaju svuda.
Provereno programski da se svaka izmena tacno slaze sa canonical URL-om.

## 2. sitemap.xml — dodat <lastmod> (72 unosa)
Svaki URL u sitemap-u sada ima datum poslednje izmene (2026-08-02).
XML potvrdjeno validan posle izmene.

## 3. robots.txt — dodat Disallow: /mnt/
Sigurnosna mera, cak i ako je mnt/ folder vec obrisan iz repoa —
spreci buduce slucajne indeksacije ako se ponovi.

## 4. _headers — dodato keširanje za /images/*
Cache-Control: public, max-age=2592000, immutable
Ubrzava ucitavanje slika za posetioce koji se vracaju.

## Kako
Raspakuj u koren repoa (Merge za jezicke foldere, Replace za
sitemap.xml/robots.txt/_headers).
git add -A && git commit -m "Fix mainEntityOfPage mismatch, add sitemap lastmod, robots/headers hardening" && git push
