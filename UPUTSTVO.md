# M.Y.V. 2.0: novi dizajn, 6 izleta, 6 jezika

## Šta je novo
- Nova početna (/, /ru/, /de/, /tr/, /uk/, /sr/): Alanja hero, statistika, traka sa izletima, O nama, recenzije, baner.
- Kapadokija se seli sa / na /cappadocia (i /ru/cappadocia itd.).
- Novi izleti: /private-boat-alanya i /pirate-ship-alanya (sa videom).
- Sve stranice izleta: pola slika / pola tekst, paketi, uključeno / nije uključeno / ponesite, plan ture, galerija, česta pitanja, forma za pitanje, animirana traka „Rezerviši".
- Rezervacija se otvara odmah, na svakoj stranici. Brod: termin + broj osoba, cena se računa sama (€350 do 6 osoba, +€20 po osobi, max 12).
- Stranice „Izleti iz Alanje" i „Izleti iz Side-a" u novom dizajnu.
- Blog ostaje u starom dizajnu; linkovi „Vidi turu" vode na /cappadocia.
- Mejl za rezervaciju sada prikazuje i termin i broj osoba (za brod).
- Novi sitemap.xml (90 adresa) i preusmerenja za .html adrese.

## Kako se menja sadržaj ubuduće
Tekstovi su u build/data/*.json. Posle izmene pokreni u folderu sajta:
    python3 build/build.py
Stari generate-languages.py se NE koristi.

## Objava (prvo pregled, pa tek onda pravi sajt)
1. U Terminalu uđi u folder sajta (isti kao do sada) i napravi novu granu:
       git checkout -b redizajn
2. Raspakuj zip sa Desktop-a preko sajta:
       unzip -o ~/Desktop/myv-2.0.zip
3. Pošalji granu na GitHub:
       git add -A
       git commit -m "M.Y.V. 2.0 redesign: new home, 6 tours, boat and pirate"
       git push -u origin redizajn
4. Na GitHub-u klikni „Compare & pull request" → „Create pull request".
   Netlify za par minuta u tom pull request-u ostavi link „Deploy Preview". Tu pregledaj sajt (i na telefonu).
5. Kad je sve u redu: na GitHub-u „Merge pull request". Netlify tada objavljuje na myvalanyatravel.com.
6. Vrati se na glavnu granu u Terminalu:
       git checkout main
       git pull
