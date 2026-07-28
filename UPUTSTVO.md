# Meni breakpoint fix — hamburger se pojavljuje ranije

## Šta je promenjeno
Glavni meni se do sada gužvao na uskim laptopovima (~1280px).
Sada se hamburger meni pojavljuje već ispod 1200px umesto ispod 1024px.
Na širim ekranima (1200px+) ostaje pun desktop meni kao pre.

Promenjeno je TAČNO dvoje po fajlu (CSS breakpoint):
- @media(max-width:1024px) -> 1200px   (kad se pojavi hamburger)
- @media(min-width:1025px) -> 1201px    (desktop scrolled stilovi)

JS i HTML menija su NETAKNUTI — hamburger radi isto kao i pre,
samo se pojavljuje na široj tački.

## Fajlovi (24)
index (Kapadokija), demre-myra-kekova, green-canyon, pamukkale — svaki x 6 jezika.
Blogovi i hub stranice imaju drugačiji header i NISU dirani.

## Kako da raspakuješ
Iz korena repoa, raspakuj tako da se folderi poklope (Merge, ne Replace).
Fajlovi prebrisuju postojeće istoimene.

## Pregled pre push-a
1. Raspakuj u repo
2. netlify dev (ili lokalni server)
3. Smanji prozor browsera na ~1280px — meni sada treba da bude hamburger
4. Proširi na 1400px — pun desktop meni
5. Klikni hamburger — otvara sve stavke kao i pre
6. Zadovoljan -> git add -A && git commit -m "Menu: hamburger breakpoint 1024->1200" && git push

## Napomena
Ovo je "Opcija A" — samo pomeranje tačke prelaska.
Padajući "Tours" meni i proređivanje stavki (Opcija B) je veći posao,
ostavljen za kasnije ako budeš hteo.
