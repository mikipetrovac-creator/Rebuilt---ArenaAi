# Tri izmene odjednom — meta opisi + meni + Viber napomena

Primenjeno na AKTUELNU verziju sajta (iz provere), pa se lepo poklapa
sa onim što je već online (recenzija Fiery Phoenix, hero slike — netaknuti).

## Šta je unutra (24 fajla: 4 ture x 6 jezika)

1. META OPISI (Pamukale, Demre, Green Canyon) — prepravljeni da odgovaraju
   na prave upite iz Search Console:
   - Pamukale: "Yes, you can swim in Cleopatra's pool (~15 EUR)"
   - Demre: Kekova / Sunken City / St Nicholas
   - Green Canyon: emerald Green Lake
   OVO je najvažnije — resava Demre 102 prikaza / 3 klika problem.

2. MENI breakpoint 1024 -> 1200
   Hamburger se sada pojavljuje ranije (ispod 1200px), meni se vise
   ne guzva na uskim laptopovima (~1280px).

3. VIBER napomena u booking modalu
   "Poruka je kopirana — samo je nalepite u aplikaciju." (6 jezika)
   Resava zbunjenost kod Vibera koji ne prima gotov tekst.

## Kako
1. Raspakuj u koren repoa (Merge, ne Replace) — prebrisuje 24 fajla
2. netlify dev -> proveri:
   - meni na 1280px = hamburger
   - booking modal ima Viber napomenu
   - (meta opisi se ne vide u browseru, ali su u kodu)
3. git add -A && git commit -m "Meta descriptions + menu breakpoint + Viber hint" && git push
4. Posle push-a: u Search Console -> URL Inspection -> zatrazi reindeksiranje
   za /pamukkale, /demre-myra-kekova, /green-canyon (da Google brze pokupi nove opise)

## Sto NIJE dirano (vec online, netaknuto)
- Recenzija Fiery Phoenix + broj 36
- Hero slike Demre i Green Canyon
- Chat meni (WhatsApp/Viber/Telegram/VK/MAX)
