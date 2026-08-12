# Nove cene Kapadokije — Budget 50€, Premium 100€ (6 fajlova)

## Nove cene
- Budget: odrasli 35 -> 50 EUR, dete NEPROMENJENO (25 EUR)
- Premium: odrasli 90 -> 100 EUR, dete 45 -> 50 EUR
- Infant (0-3): i dalje besplatno (0 EUR)

## Sta je azurirano, 12 mesta po fajlu:
1. JS "pricing" objekat — IZVOR ISTINE za kalkulator, email i WhatsApp poruku
2. WhatsApp/email poruka template (PREMIUM/BUDGET oznaka sa cenom)
3. Tab dugmad (Premium/Budget) x2 svaka
4. "Starting from" price-big prikaz (oba paketa)
5. "Children"/"Adults" cene u oba paket bloka
6. Default prikaz cene pre klika (adult-price-display)
7. "Estimated Total" placeholder
8. JSON-LD Product schema price (za Google rich snippets)
9. Meta description + og:description + twitter:description (sve 3 taga)

## Sta NIJE dirano (namerno):
- "Balloon panorama – €35" — OPCIONA aktivnost, slucajno ista cifra kao
  stara Budget cena. Ovo je zaseban trosak (let balonom + panorama tacka),
  ne cena ture. Proveril sam da je ostalo netaknuto na svih 6 jezika.
- "Jeep safari – €50" — isto, opciona aktivnost, slucajno ista cifra kao
  nova Budget cena. Netaknuto.
- Ostale opcione aktivnosti (Red Valley €15, Turkish Night €40) — netaknute.
- Cena za decu na Budget paketu (25 EUR) — po tvom uputstvu, nepromenjena.

## Provera
- Simulacija stvarnog JS kalkulatora potvrdila tacne iznose:
  Budget 2 odrasla = €100, Budget 2 odrasla+1 dete = €125,
  Premium 2 odrasla = €200, Premium 2 odrasla+2 dece = €300
- Svih 6 fajlova: tagovi/JSON-LD validni, prevodi parsiraju
- Vizuelno provereno oba taba (Budget/Premium) u browseru

## Kako
Raspakuj u koren repoa (Replace za index.html fajlove).
git add -A && git commit -m "Update Cappadocia prices: Budget 50 EUR, Premium 100 EUR" && git push
