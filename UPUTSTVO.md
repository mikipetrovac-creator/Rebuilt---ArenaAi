# Nove recenzije + brojac 42 (12 fajlova)

Google profil se u medjuvremenu osvezio i sada pokazuje 42 recenzije
(bilo je 36), pa je sve uskladjeno sa stvarnim stanjem.

## KAPADOKIJA (index.html x 6 jezika)
Dodate 4 nove recenzije (sve 5 zvezdica):
1. Merli Kalbus (EN, Estonija) — hvali Yelenu; balon rezervisan PREKO VODICA
   (direktna potvrda da poruka koju smo dodali na sajt radi)
2. Ирина Овчинникова (RU)
3. Dmitry (RU)
4. Elnara Zakiroglu (RU)

Ukupno 40 citljivih kartica u "Read all" modalu.

### Brojevi
- Brojac na stranici: 42 (tacan Google broj)
- Schema reviewCount: 42 (odgovara Google-u — bezbedno za rich snippets)
- Labela: "Google Reviews" (tacna, jer se broj poklapa)

Napomena: kartica ima 40 a brojac 42 jer 2 recenzije na Google-u
nemaju napisan tekst (samo zvezdice), pa se ne prikazuju kao kartice.

## PAMUKALE (pamukkale.html x 6 jezika)
Dodata recenzija Zemfire Valiyeve — ona pise BAS o Pamukkale turi,
pa pripada toj stranici. Modal recenzija na Pamukkale je do sada bio prazan.

## Provera
- Kapadokija: 40 kartica, brojac/schema 42, svih 6 jezika
- Pamukkale: Zemfira dodata, svih 6 jezika
- Tagovi balansirani, JSON-LD validan u svih 12 fajlova

## Kako
Raspakuj u koren repoa (Replace).
git add -A
git commit -m "Add new reviews, update count to 42"
git push
