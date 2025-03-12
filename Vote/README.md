# Descriere - RO
![Image](https://github.com/user-attachments/assets/32765f76-9d1d-4053-9683-b8e9b08506b6)
Înregistrare votant cu credențialele

![Image](https://github.com/user-attachments/assets/7e0670f6-2f98-4003-a7f6-ce1c830aa23c)
Atribuire ID

![Image](https://github.com/user-attachments/assets/b771bd51-e482-4b7f-bede-a46f07787567)
Autentificarea alegătorului folosind ID-ul generat la înregistrare

![Image](https://github.com/user-attachments/assets/adc4421e-1a60-4d1c-8bc2-0a5f647c3f53)
Autentificarea cu succes a votantului validat ce poate vota

![Image](https://github.com/user-attachments/assets/63478242-67f4-4cb4-a81c-d9c168abf192)
Înregistrarea votului în sistem (criptat)

![Image](https://github.com/user-attachments/assets/d1cd1c25-d56c-4fca-8ae0-a6dbd69f2c94)
Afișarea rezultatelor în timp real prin grafice de tip bară și pie chart

![Image](https://github.com/user-attachments/assets/49227db0-9845-4273-a12f-6e6a2e3aa169)
Verificarea individuală a voturilor (alegătorii pot confirma că votul lor a fost înregistrat)

![Image](https://github.com/user-attachments/assets/5dd1cac6-2328-43b7-89ef-9d8f5775166c)
Demonstrație interactivă despre principiile criptografice utilizate

# Mecanisme de securitate implementate
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

# Description - ENG
![Image](https://github.com/user-attachments/assets/32765f76-9d1d-4053-9683-b8e9b08506b6)
Voter registration with credentials

![Image](https://github.com/user-attachments/assets/7e0670f6-2f98-4003-a7f6-ce1c830aa23c)
ID assignment

![Image](https://github.com/user-attachments/assets/b771bd51-e482-4b7f-bede-a46f07787567)
Voter authentication using the ID generated at registration

![Image](https://github.com/user-attachments/assets/adc4421e-1a60-4d1c-8bc2-0a5f647c3f53)
Successful authentication of the validated voter who can vote

![Image](https://github.com/user-attachments/assets/63478242-67f4-4cb4-a81c-d9c168abf192)
Registering the vote in the system (encrypted)

![Image](https://github.com/user-attachments/assets/d1cd1c25-d56c-4fca-8ae0-a6dbd69f2c94)
Displaying results in real time through bar and pie charts chart

![Image](https://github.com/user-attachments/assets/49227db0-9845-4273-a12f-6e6a2e3aa169)
Individual vote verification (voters can confirm that their vote was recorded)

![Image](https://github.com/user-attachments/assets/5dd1cac6-2328-43b7-89ef-9d8f5775166c)
Interactive demonstration of the cryptographic principles used

# Implemented security mechanisms
The system uses several cryptographic mechanisms to ensure the security and integrity of the electoral process:

1. Public key encryption (RSA), where votes are encrypted with the public key of the electoral authority. Only the electoral authority can decrypt the votes using the corresponding private key.

2. Digital signatures, when each voter has a pair of keys (public and private). The vote is signed with the voter's private key, and the signature can be verified using the voter's public key.

3. Cryptographic hashes are used to securely store sensitive data (e.g., the CNP is stored only as a hash) and ensure data integrity.

4. End-to-end verifiability, when voters can verify that their vote was recorded correctly, and the system maintains the confidentiality of the vote.
Data flow

5. Registration: Personal data → Generate ID and keys → Store in the voters dictionary

6. Voting:
o Authentication → Candidate selection → Encryption and signing → Store in the ballots list
For simulation, the vote is also decrypted immediately to update the count.

7. Verification: Enter Voter ID → Search Ballot → Verify Signature → Confirm
Important Notes
• The system is demonstrative and contains simplifications that would not be appropriate in a real system
• In a real system, the voter's private key would remain with the voter only
• Data is not persistent between sessions (the save_data and load_data functions are partially implemented)
• The system demonstrates cryptographic principles without implementing all the security measures required for a real system

This code serves as an educational example of how an electronic voting system might work and what security mechanisms it might use to ensure the integrity, confidentiality, and verifiability of the electoral process.
