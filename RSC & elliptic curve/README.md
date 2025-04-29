# Exerciții propuse

![image](https://github.com/user-attachments/assets/96415a98-ffd2-4f14-9071-ca92142c5dc1)

# Interfață

https://github.com/user-attachments/assets/bd7504be-55b4-4f03-bed2-9faac081121e

# Instrucțiuni de instalare și utilizare a aplicațiilor criptografice

## Cerințe de sistem
- Python 3.6 sau mai recent
- Tkinter (de obicei vine instalat cu Python)

## Pași pentru instalare și rulare

1. **Salvați toate cele trei fișiere în același director**:
   - `main_application.py` - Aplicația principală
   - `rsa_encryption.py` - Aplicația pentru criptosistemul RSA
   - `elliptic_curve_cryptography.py` - Aplicația pentru criptografia pe curbe eliptice

2. **Rulați aplicația principală**:
   ```
   python main_application.py
   ```

3. **Din meniul principal**, alegeți una dintre cele două aplicații disponibile:
   - **Aplicația 1**: Criptosistem Exponențial (RSA)
   - **Aplicația 2**: Criptografie pe Curbe Eliptice

## Utilizarea aplicației RSA (Aplicația 1)

Această aplicație permite:
- Criptarea unui mesaj folosind criptosistemul exponențial RSA
- Stabilirea unei chei comune folosind numărul prim p

### Pentru criptarea unui mesaj:
1. Introduceți numărul prim p (implicit 101)
2. Introduceți cheia publică e (implicit 23)
3. Introduceți mesajul de criptat (implicit "CRIPTOGRAFIE")
4. Apăsați butonul "Criptează Mesaj"

### Pentru stabilirea unei chei comune:
1. Introduceți numărul prim p (implicit 101)
2. Apăsați butonul "Stabilește Cheia Comună"

## Utilizarea aplicației de Criptografie pe Curbe Eliptice (Aplicația 2)

Această aplicație permite:
- Determinarea punctelor de pe curba eliptică y² = x³ + x + 1 peste Z₇
- Cifrarea unui mesaj folosind curba eliptică
- Descifrarea unui mesaj cifrat

### Pentru a găsi punctele curbei:
1. Apăsați butonul "Determină punctele curbei"

### Pentru cifrarea unui mesaj:
1. Introduceți mesajul M în format (x,y), de exemplu (10,9)
2. Apăsați butonul "Cifrează mesajul"

### Pentru descifrarea unui mesaj:
1. Introduceți sau preluați mesajul cifrat din câmpul corespunzător
2. Apăsați butonul "Descifrează mesajul"

## Explicații matematice

Ambele aplicații afișează pașii matematici detaliați pentru fiecare operațiune efectuată, astfel încât să se poată urmări procesul de criptare și decriptare.

## În caz de erori

Dacă întâmpinați probleme la rularea aplicațiilor:
1. Verificați dacă aveți Python instalat corect
2. Verificați dacă toate cele trei fișiere se află în același director
3. Verificați dacă aveți Tkinter instalat (este necesar pentru interfața grafică)
