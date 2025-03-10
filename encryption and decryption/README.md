# Exercises proposed for solution
![Image](https://github.com/user-attachments/assets/ea332992-493f-4c8a-b1b4-9a8ea127bdeb)

# SIMPLE
https://github.com/user-attachments/assets/7c354ee2-f41c-483c-83b4-51328cd0571e

# EXTENDED
https://github.com/user-attachments/assets/af67c759-1187-48cd-9146-ef049a58c746


# Descriere pentru fiecare aplicație

1: Cifrarea folosind Cifrul lui Cezar
Aceasta este o metodă clasică de criptare în care fiecare literă din textul original este înlocuită cu o literă aflată la o distanță fixă în alfabet. În acest caz, cheia de cifrare este k=5, ceea ce înseamnă că fiecare literă este înlocuită cu a 5-a literă care o urmează în alfabet. De exemplu, A devine F, B devine G, etc. Mesajul "CRIPTOGRAFIE" este astfel transformat într-un text cifrat prin această deplasare.

2: Decriptarea Cifrului lui Cezar
Aplicația realizează operația inversă celei din Aplicația 1. Avem un text cifrat "JAJSN SHJWDU YTQTL DXNQJ SHJNX LTQJJ SXXXX" și trebuie să determinăm cheia de cifrare (valoarea k) pentru a recupera mesajul original. Algoritmul încearcă toate cheile posibile (1-25) și determină care dintre rezultate are cea mai mare probabilitate de a fi textul original, bazându-se pe frecvența literelor.

3: Criptosistemul Afin
Criptosistemul afin este o generalizare a cifrului lui Cezar. În loc să folosească doar o deplasare fixă, folosește o funcție matematică de forma E(x) = (ax + b) mod 26, unde 'a' și 'b' sunt cheia de cifrare. În acest caz, cheia este (5,2), ceea ce înseamnă că a=5 și b=2. Textul "CRIPTARE" este cifrat prin aplicarea acestei formule pentru fiecare literă.

4: Rezolvarea unui Sistem de Congruențe
Această aplicație rezolvă un sistem de ecuații modulare (congruențe) de forma:

ax + by ≡ c (mod m)
dx + ey ≡ f (mod m)
Algoritmul calculează determinantul Δ = ad - bc, verifică dacă este inversabil modulo m, și apoi calculează soluțiile x și y. Aceste sisteme sunt fundamentale în multe operații criptografice mai avansate.

5: Cifrul Hill Modificat cu Vector de Deplasare
Cifrul Hill utilizează algebra liniară pentru criptare, folosind o matrice ca și cheie. În această variantă modificată, se folosește o matrice A = [[3, 5], [1, 2]] și un vector de deplasare b = [[2], [2]]. Textul "ATTACK" este împărțit în perechi de litere, care sunt transformate în vectori, înmulțite cu matricea A, adunate cu vectorul b, și apoi se aplică modulul 26 pentru a obține textul cifrat.

6: Cifrul Hill Standard
Similar cu Aplicația 5, dar fără vectorul de deplasare. Se folosește doar înmulțirea cu matricea A = [[2, 5], [1, 3]] pentru a cifra mesajul "CRIPTOGRAFIE". Fiecare pereche de litere este tratată ca un vector, înmulțită cu matricea A, și apoi convertită înapoi în litere pentru a forma textul cifrat.
Aceste aplicații ilustrează diverse metode criptografice, de la cele clasice și simple (Cifrul lui Cezar) la cele mai avansate care utilizează algebra liniară (Cifrul Hill) și operații matematice modulare. Toate sunt fundamentale pentru înțelegerea principiilor criptografiei.

# Description for each application

1: Encryption using Caesar Cipher
This is a classic encryption method in which each letter in the original text is replaced by a letter at a fixed distance in the alphabet. In this case, the encryption key is k=5, which means that each letter is replaced by the 5th letter that follows it in the alphabet. For example, A becomes F, B becomes G, etc. The message "CRYPTOGRAPHY" is thus transformed into a ciphertext by this shift.

2: Decryption of Caesar Cipher
The application performs the reverse operation of that in Application 1. We have a ciphertext "JAJSN SHJWDU YTQTL DXNQJ SHJNX LTQJJ SXXXX" and we need to determine the encryption key (the value of k) to recover the original message. The algorithm tries all possible keys (1-25) and determines which of the results has the highest probability of being the original text, based on the frequency of the letters.

3: Affine Cryptosystem
The affine cryptosystem is a generalization of the Caesar cipher. Instead of using only a fixed shift, it uses a mathematical function of the form E(x) = (ax + b) mod 26, where 'a' and 'b' are the encryption key. In this case, the key is (5,2), which means that a=5 and b=2. The text "ENCRYPTION" is encrypted by applying this formula to each letter.

4: Solving a System of Congruences
This application solves a system of modular equations (congruences) of the form:

ax + by ≡ c (mod m)
dx + ey ≡ f (mod m)
The algorithm computes the determinant Δ = ad - bc, checks if it is invertible modulo m, and then computes the solutions x and y. These systems are fundamental to many more advanced cryptographic operations.

5: Modified Hill Cipher with Displacement Vector
The Hill cipher uses linear algebra for encryption, using a matrix as the key. In this modified variant, a matrix A = [[3, 5], [1, 2]] and a displacement vector b = [[2], [2]] are used. The text "ATTACK" is divided into pairs of letters, which are converted into vectors, multiplied by the matrix A, added by the vector b, and then modulo 26 is applied to obtain the ciphertext.

6: Standard Hill Cipher
Similar to Application 5, but without the shift vector. Only multiplication by the matrix A = [[2, 5], [1, 3]] is used to encrypt the message "CRYPTOGRAPHY". Each pair of letters is treated as a vector, multiplied by the matrix A, and then converted back to letters to form the ciphertext.
These applications illustrate various cryptographic methods, from the classical and simple ones (Caesar Cipher) to the more advanced ones that use linear algebra (Hill Cipher) and modular mathematical operations. All are fundamental to understanding the principles of cryptography.
