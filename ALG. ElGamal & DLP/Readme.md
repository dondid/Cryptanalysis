# Vizualizator pentru Problema Logaritmului Discret (DLP)

Această aplicație oferă o interfață grafică interactivă pentru înțelegerea și vizualizarea **problemei logaritmului discret** (DLP - Discrete Logarithm Problem) și a algoritmilor principali utilizați pentru rezolvarea acesteia.

## Descrierea problemei

Problema logaritmului discret este formulată astfel:

Considerăm:
- un număr prim p,
- g un generator al grupului Z_p* (rădăcină primitivă modulo p) și
- un element b ∈ Z_p*

Se cere să se determine 1 ≤ x ≤ p − 1 pentru care b ≡ g^x (mod p).

Dacă alegem alt grup ciclic în locul Z_p*, obținem **problema generalizată a logaritmului discret** (GDLP).

## Caracteristici ale aplicației

Aplicația implementează și vizualizează următorii algoritmi pentru rezolvarea DLP:

1. **Căutare Exhaustivă (Brute Force)** - verifică fiecare posibil exponent până găsește soluția
2. **Baby-step Giant-step** - un algoritm de tip "meet-in-the-middle" cu complexitate O(√p)
3. **Pollard's Rho** - un algoritm probabilistic eficient în practică
4. **Pohlig-Hellman** - exploatează factorizarea lui p-1 pentru rezolvarea DLP

Pentru fiecare algoritm, aplicația oferă:
- Pașii matematici detaliați ai execuției algoritmului
- Vizualizare grafică a operațiilor și a valorilor intermediare
- Reprezentare ciclică pe cerc a elementelor modulare

## Utilizare

1. Introduceți parametrii:
   - Numărul prim p
   - Generatorul g
   - Elementul b căruia i se caută logaritmul

2. Selectați unul dintre algoritmi apăsând pe butonul corespunzător

3. Vizualizați:
   - Tab-ul "Pași Matematici" - pentru a înțelege pașii de calcul
   - Tab-ul "Vizualizare Grafică" - pentru reprezentare vizuală

## Dependențe

Aplicația necesită următoarele biblioteci Python:
- tkinter - pentru interfața grafică
- matplotlib - pentru vizualizare grafică
- numpy - pentru calcule
- sympy - pentru funcții matematice (test primalitate, etc.)

## Instalare dependențe

```bash
pip install numpy matplotlib sympy
```

## Rulare

```bash
python run_dlp_visualizer.py
```

## Importanța Problemei Logaritmului Discret

DLP stă la baza mai multor sisteme criptografice moderne, inclusiv:
- Protocolul de schimb de chei Diffie-Hellman
- Criptosistemul ElGamal
- Sistemul de semnătură digitală DSA

Securitatea acestor sisteme se bazează pe dificultatea calculării logaritmilor discreți în grupuri speciale.
