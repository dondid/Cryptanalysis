# Description

Înregistrare votant cu credențialele

Atribuire ID

Autentificarea alegătorului folosind ID-ul generat la înregistrare

Autentificarea cu succes a votantului validat ce poate vota

Înregistrarea votului în sistem (criptat)

Afișarea rezultatelor în timp real prin grafice de tip bară și pie chart

Verificarea individuală a voturilor (alegătorii pot confirma că votul lor a fost înregistrat)

Demonstrație interactivă despre principiile criptografice utilizate

Mecanisme de securitate implementate
Sistemul folosește mai multe mecanisme criptografice pentru a asigura securitatea și integritatea procesului electoral:

1. Criptare cu cheie publică (RSA), unde voturile sunt criptate cu cheia publică a autorității electorale. Doar autoritatea electorală poate decripta voturile folosind cheia privată corespunzătoare.
2. Semnături digitale, când fiecare alegător are o pereche de chei (publică și privată). Votul este semnat cu cheia privată a alegătorului, iar semnătura poate fi verificată folosind cheia publică a alegătorului.
3. Hash-uri criptografice sunt utilizate pentru stocarea securizată a datelor sensibile (ex: CNP-ul este stocat doar ca hash) și asigură integritatea datelor.
4. Verificabilitate end-to-end, când alegătorii pot verifica că votul lor a fost înregistrat corect, iar sistemul păstrează confidențialitatea votului.
   Fluxul de date
5. Înregistrare: Date personale → Generare ID și chei → Stocare în dicționarul voters
6. Votare:
   o Autentificare → Selecție candidat → Criptare și semnare → Stocare în lista ballots
   Pentru simulare, votul este și decriptat imediat pentru a actualiza numărătoarea.
7. Verificare: Introducere ID alegător → Căutare buletin de vot → Verificare semnătură → Confirmare
   Observații importante
   • Sistemul este demonstrativ și conține simplificări care nu ar fi adecvate într-un sistem real
   • Într-un sistem real, cheia privată a alegătorului ar rămâne doar la acesta
   • Datele nu sunt persistente între sesiuni (funcțiile save_data și load_data sunt implementate parțial)
   • Sistemul demonstrează principii criptografice fără a implementa toate măsurile de securitate necesare unui sistem real
   Acest cod servește ca un exemplu educațional despre cum ar putea funcționa un sistem de vot electronic și ce mecanisme de securitate ar putea utiliza pentru a asigura integritatea, confidențialitatea și verificabilitatea procesului electoral.
