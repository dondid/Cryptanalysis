# Aplicația 1 Calculul Inversului Modulo
![Image](https://github.com/user-attachments/assets/188d6f09-e54a-4a35-aad8-630ceefb0a90)

# Aplicatia 2 Teorema Chinezească a Resturilor
![Image](https://github.com/user-attachments/assets/21a487b5-afd7-4dfa-a329-c3ada3940b8f)

# Aplicația 3 Ridicare Repetată la Pătrat
![Image](https://github.com/user-attachments/assets/f107698b-f381-48f2-9954-963952038204)

# Aplicația 4 Fracții Continue și Rezolvarea Ecuațiilor Diofantice
![Image](https://github.com/user-attachments/assets/5ad76034-64a0-4285-a051-a011312acac9)

# Toate -> terminal
==== APLICAȚII MATEMATICE ====
1. Calculul inversului modulo m
2. Teorema chinezească a resturilor
3. Ridicarea repetată la pătrat (mod m)
4. Dezvoltarea în fracție continuă
5. Rezolvarea ecuației diofantice ax + by = c
0. Ieșire

Alegeți o opțiune (0-5): 5
Introduceți coeficientul a: 8
Introduceți coeficientul b: 15
Introduceți termenul liber c: 9
Calculăm dezvoltarea în fracție continuă pentru 8/15
8 = 15 * 0 + 8
15 = 8 * 1 + 7
8 = 7 * 1 + 1
7 = 1 * 7 + 0

Dezvoltarea în fracție continuă a lui 8/15 este: [0, 1, 1, 7]

Calculăm convergențele:
p₀ = 1, q₀ = 0
p₍1₎ = 0 * 1 + 0 = 0
q₍1₎ = 0 * 0 + 1 = 1
p₍2₎ = 1 * 0 + 1 = 1
q₍2₎ = 1 * 1 + 0 = 1
p₍3₎ = 1 * 1 + 0 = 1
q₍3₎ = 1 * 1 + 1 = 2
p₍4₎ = 7 * 1 + 1 = 8
q₍4₎ = 7 * 2 + 1 = 15

Am verificat că p_4 = 8 = 8 și q_4 = 15 = 15
Din relația q_4p_3 - p_4q_3 = (-1)^4, avem:
15 * 1 - 8 * 2 = 1
Astfel, soluția ecuației 8x + 15y = 1 este:
x₀ = -2, y₀ = 1
Verificare: 8 * -2 + 15 * 1 = -1
Rezolvăm ecuația diofantică 8x + 15y = 9
Calculăm cmmdc(8, 15) = 1
Simplificăm ecuația: 8x + 15y = 9

O soluție particulară a ecuației 8x + 15y = 9 este:
x₀ = -18, y₀ = 9
Verificare: 8 * -18 + 15 * 9 = -9

Formula generală a soluțiilor este:
x = -18 + 15*t
y = 9 - 8*t
unde t este un număr întreg arbitrar.

Apăsați Enter pentru a continua...
