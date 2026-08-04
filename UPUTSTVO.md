# "Ne zaboravite" — tacnija formulacija (6 fajlova)

Stavka "Nesto dodatnog novca za rucak i pice" u "Ne zaboravite" listi
(Kapadokija, oba paketa - Premium i Budzet) je bila netacna za Premium
paket, koji vec ima "Svi obroci ukljuceni".

Promenjeno na generalniju, tacniju formulaciju za oba paketa:

SR: Nešto dodatnog novca za piće i vaše lične troškove
EN: Some extra money for drinks and personal expenses
RU: Немного дополнительных денег на напитки и личные расходы
DE: Etwas zusätzliches Geld für Getränke und persönliche Ausgaben
TR: İçecekler ve kişisel harcamalarınız için ekstra para
UK: Додаткові гроші на напої та особисті витрати

Primenjeno u svih 6 kopija index.html (root + 5 jezika), jer svaka
kopija nosi kompletan set od 6 prevoda unutar sebe (tako radi
prekidac jezika na sajtu).

## Kako
Raspakuj u koren repoa (Merge/Replace za index.html fajlove).
git add -A && git commit -m "Fix 'don't forget' note wording (accurate for Premium package)" && git push
