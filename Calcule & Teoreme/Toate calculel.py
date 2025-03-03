import math


def gcd(a, b):
    """Calculează cel mai mare divizor comun (cmmdc) al numerelor a și b."""
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """
    Calculează cmmdc-ul numerelor a și b, precum și coeficienții u și v din relația
    a*u + b*v = cmmdc(a, b)
    """
    if a == 0:
        return b, 0, 1
    else:
        g, v, u = extended_gcd(b % a, a)
        return g, u - (b // a) * v, v


def print_steps(steps):
    """Afișează pașii de calcul."""
    for step in steps:
        print(step)


# APLICAȚIA 1: Inversul modulo m
def invers_modulo(a, m):
    """
    Calculează inversul lui a modulo m.

    Args:
        a: Numărul pentru care se caută inversul
        m: Modulul

    Returns:
        Inversul lui a modulo m, dacă există, altfel None
    """
    steps = [f"Calculăm inversul lui {a} modulo {m}"]

    # Verificăm dacă a și m sunt prime între ele
    d, x, y = extended_gcd(a, m)
    steps.append(f"Aplicăm algoritmul lui Euclid extins:")

    if d > 1:
        steps.append(f"(a, m) = ({a}, {m}) = {d} > 1")
        steps.append(f"Inversul lui {a} modulo {m} nu există deoarece {a} și {m} nu sunt prime între ele.")
        print_steps(steps)
        return None

    # Calculăm inversul și ajustăm pentru a obține un rezultat pozitiv
    invers = x % m

    steps.append(f"Am calculat coeficienții din relația {a}u + {m}v = 1:")
    steps.append(f"{a} * {x} + {m} * {y} = {d}")
    steps.append(f"Astfel, {a} * {x} ≡ 1 (mod {m})")
    steps.append(f"Inversul lui {a} modulo {m} este {invers}")

    print_steps(steps)
    return invers


# APLICAȚIA 2: Teorema chinezească a resturilor
def chinese_remainder_theorem(moduli, remainders):
    """
    Rezolvă un sistem de congruențe folosind teorema chinezească a resturilor.

    Args:
        moduli: Lista de module (m1, m2, ..., mt)
        remainders: Lista de resturi (b1, b2, ..., bt)

    Returns:
        Soluția x a sistemului de congruențe, dacă există
    """
    steps = ["Aplicăm Teorema chinezească a resturilor pentru sistemul:"]
    for i in range(len(moduli)):
        steps.append(f"x ≡ {remainders[i]} (mod {moduli[i]})")

    # Verificăm dacă modulii sunt două câte două prime între ele
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                steps.append(f"Modulii {moduli[i]} și {moduli[j]} nu sunt primi între ei.")
                steps.append("Sistemul nu poate fi rezolvat cu acest algoritm.")
                print_steps(steps)
                return None

    # Calculăm produsul tuturor modulilor
    m = 1
    for mi in moduli:
        m *= mi
    steps.append(f"Produsul modulilor m = {m}")

    result = 0
    for i in range(len(moduli)):
        mi = moduli[i]
        bi = remainders[i]
        ni = m // mi

        steps.append(f"\nPentru congruența x ≡ {bi} (mod {mi}):")
        steps.append(f"Calculăm ni = m/mi = {m}/{mi} = {ni}")

        # Calculăm inversul lui ni modulo mi
        si = invers_modulo(ni % mi, mi)
        if si is None:
            steps.append(f"Inversul lui {ni} modulo {mi} nu există.")
            steps.append("Sistemul nu poate fi rezolvat.")
            print_steps(steps)
            return None

        steps.append(f"Inversul lui {ni} modulo {mi} este {si}")

        # Adăugăm contribuția la rezultat
        term = (bi * ni * si) % m
        result = (result + term) % m

        steps.append(f"Termen: {bi} * {ni} * {si} ≡ {term} (mod {m})")

    steps.append(f"\nSoluția sistemului este x ≡ {result} (mod {m})")
    print_steps(steps)
    return result


# APLICAȚIA 3: Ridicarea repetată la pătrat
def power_mod(b, n, m):
    """
    Calculează b^n mod m folosind metoda ridicării repetate la pătrat.

    Args:
        b: Baza
        n: Exponentul
        m: Modulul

    Returns:
        b^n mod m
    """
    steps = [f"Calculăm {b}^{n} mod {m} folosind metoda ridicării repetate la pătrat"]

    if n == 0:
        steps.append("Rezultatul este 1 (orice număr la puterea 0 este 1)")
        print_steps(steps)
        return 1

    # Convertim n în binar
    binary = bin(n)[2:]  # eliminăm prefixul '0b'
    steps.append(f"Scriem exponentul {n} în baza 2: {binary}")

    steps.append(f"\nCalculăm puterile succesive și le reducem modulo {m}:")

    # Inițializăm rezultatul
    result = 1
    a = b

    # Tabel pentru pași
    table = [["j", "bit", f"{b}^(2^j) mod {m}", "Înmulțim cu rezultatul?"]]

    for j, bit in enumerate(binary[::-1]):  # parcurgem de la dreapta la stânga
        if bit == '1':
            result = (result * a) % m
            used = "Da"
        else:
            used = "Nu"

        table.append([j, bit, a, used])

        # Pregătim pentru următoarea iterație
        a = (a * a) % m

    # Afișăm tabelul
    steps.append("\nTabel de calcul:")
    col_widths = [max(len(str(row[i])) for row in table) for i in range(len(table[0]))]

    for i, row in enumerate(table):
        formatted_row = " | ".join(str(cell).ljust(col_widths[j]) for j, cell in enumerate(row))
        steps.append(formatted_row)
        if i == 0:  # după antet
            steps.append("-" * len(formatted_row))

    steps.append(f"\nRezultatul final: {b}^{n} mod {m} = {result}")
    print_steps(steps)
    return result


# APLICAȚIA 4: Dezvoltarea în fracție continuă și rezolvarea ecuației diofantice
def continued_fraction(a, b):
    """
    Calculează dezvoltarea în fracție continuă a lui a/b și rezolvă ecuația ax + by = 1.

    Args:
        a, b: Numerele pentru care se calculează fracția continuă

    Returns:
        O tuplu conținând:
        - Lista termenilor fracției continue [a0, a1, ..., an]
        - Listele p și q pentru convergente
        - O soluție particulară (x0, y0) a ecuației ax + by = 1 (dacă gcd(a,b) = 1)
    """
    if b == 0:
        return [a], [a], [1], None

    # Asigurăm-ne că a și b sunt pozitive pentru algoritm
    sign_a, sign_b = 1, 1
    if a < 0:
        a, sign_a = -a, -1
    if b < 0:
        b, sign_b = -b, -1

    steps = [f"Calculăm dezvoltarea în fracție continuă pentru {a}/{b}"]

    orig_a, orig_b = a, b
    cf_terms = []  # termenii fracției continue

    # Calculăm termenii fracției continue
    while b:
        q, r = divmod(a, b)
        cf_terms.append(q)
        steps.append(f"{a} = {b} * {q} + {r}")
        a, b = b, r

    steps.append(f"\nDezvoltarea în fracție continuă a lui {orig_a}/{orig_b} este: [{', '.join(map(str, cf_terms))}]")

    # Calculăm convergentele
    p = [0, 1]
    q = [1, 0]

    steps.append("\nCalculăm convergențele:")
    steps.append(f"p₀ = {p[1]}, q₀ = {q[1]}")

    for i, a_i in enumerate(cf_terms):
        p.append(a_i * p[-1] + p[-2])
        q.append(a_i * q[-1] + q[-2])
        steps.append(f"p₍{i + 1}₎ = {a_i} * {p[-2]} + {p[-3]} = {p[-1]}")
        steps.append(f"q₍{i + 1}₎ = {a_i} * {q[-2]} + {q[-3]} = {q[-1]}")

    # Soluția ecuației ax + by = 1 (dacă gcd(a,b) = 1)
    solution = None
    if p[-1] == orig_a and q[-1] == orig_b and gcd(orig_a, orig_b) == 1:
        n = len(cf_terms)
        x0 = q[-2] * ((-1) ** (n + 1))
        y0 = p[-2] * ((-1) ** (n))

        steps.append(f"\nAm verificat că p_{n} = {p[-1]} = {orig_a} și q_{n} = {q[-1]} = {orig_b}")
        steps.append(f"Din relația q_{n}p_{n - 1} - p_{n}q_{n - 1} = (-1)^{n}, avem:")
        steps.append(f"{orig_b} * {p[-2]} - {orig_a} * {q[-2]} = {(-1) ** n}")
        steps.append(f"Astfel, soluția ecuației {orig_a}x + {orig_b}y = 1 este:")
        steps.append(f"x₀ = {x0}, y₀ = {y0}")
        steps.append(f"Verificare: {orig_a} * {x0} + {orig_b} * {y0} = {orig_a * x0 + orig_b * y0}")

        solution = (x0, y0)

    # Ajustăm pentru semnele originale
    p_adjusted = [sign_a * pi for pi in p[1:]]
    q_adjusted = [sign_b * qi for qi in q[1:]]

    print_steps(steps)
    return cf_terms, p_adjusted, q_adjusted, solution


def solve_diophantine(a, b, c):
    """
    Rezolvă ecuația diofantică ax + by = c.

    Args:
        a, b, c: Coeficienții ecuației

    Returns:
        O soluție particulară (x0, y0) și formula generală
    """
    steps = [f"Rezolvăm ecuația diofantică {a}x + {b}y = {c}"]

    # Calculăm cmmdc-ul
    d = gcd(abs(a), abs(b))
    steps.append(f"Calculăm cmmdc({abs(a)}, {abs(b)}) = {d}")

    # Verificăm dacă ecuația are soluții
    if c % d != 0:
        steps.append(f"{c} nu este divizibil cu {d}, deci ecuația nu are soluții întregi.")
        print_steps(steps)
        return None

    # Simplificăm ecuația
    a_prime, b_prime, c_prime = a // d, b // d, c // d
    steps.append(f"Simplificăm ecuația: {a_prime}x + {b_prime}y = {c_prime}")

    # Calculăm dezvoltarea în fracție continuă și rezolvăm ecuația a_prime*x + b_prime*y = 1
    cf_terms, p, q, base_solution = continued_fraction(abs(a_prime), abs(b_prime))

    if base_solution is None:
        steps.append("Nu s-a putut găsi o soluție.")
        print_steps(steps)
        return None

    # Ajustăm pentru semnele originale ale a și b
    if a_prime < 0:
        base_solution = (-base_solution[0], base_solution[1])
    if b_prime < 0:
        base_solution = (base_solution[0], -base_solution[1])

    # Scalăm soluția pentru a rezolva ecuația originală
    x0, y0 = c_prime * base_solution[0], c_prime * base_solution[1]

    steps.append(f"\nO soluție particulară a ecuației {a}x + {b}y = {c} este:")
    steps.append(f"x₀ = {x0}, y₀ = {y0}")
    steps.append(f"Verificare: {a} * {x0} + {b} * {y0} = {a * x0 + b * y0}")

    steps.append(f"\nFormula generală a soluțiilor este:")
    steps.append(f"x = {x0} + {b_prime}*t")
    steps.append(f"y = {y0} - {a_prime}*t")
    steps.append("unde t este un număr întreg arbitrar.")

    print_steps(steps)
    return (x0, y0), (b_prime, -a_prime)


def main_menu():
    """Afișează meniul principal și procesează alegerea utilizatorului."""
    while True:
        print("\n==== APLICAȚII MATEMATICE ====")
        print("1. Calculul inversului modulo m")
        print("2. Teorema chinezească a resturilor")
        print("3. Ridicarea repetată la pătrat (mod m)")
        print("4. Dezvoltarea în fracție continuă")
        print("5. Rezolvarea ecuației diofantice ax + by = c")
        print("0. Ieșire")

        choice = input("\nAlegeți o opțiune (0-5): ")

        if choice == '0':
            print("La revedere!")
            break

        elif choice == '1':
            try:
                a = int(input("Introduceți numărul a: "))
                m = int(input("Introduceți modulul m: "))
                invers_modulo(a, m)
            except ValueError:
                print("Eroare: Introduceți numere întregi valide.")

        elif choice == '2':
            try:
                n = int(input("Introduceți numărul de congruențe: "))
                moduli = []
                remainders = []

                for i in range(n):
                    print(f"\nCongruența {i + 1}:")
                    moduli.append(int(input(f"Introduceți modulul m{i + 1}: ")))
                    remainders.append(int(input(f"Introduceți restul b{i + 1}: ")))

                chinese_remainder_theorem(moduli, remainders)
            except ValueError:
                print("Eroare: Introduceți numere întregi valide.")

        elif choice == '3':
            try:
                b = int(input("Introduceți baza b: "))
                n = int(input("Introduceți exponentul n: "))
                m = int(input("Introduceți modulul m: "))
                power_mod(b, n, m)
            except ValueError:
                print("Eroare: Introduceți numere întregi valide.")

        elif choice == '4':
            try:
                a = int(input("Introduceți numărătorul a: "))
                b = int(input("Introduceți numitorul b: "))
                continued_fraction(a, b)
            except ValueError:
                print("Eroare: Introduceți numere întregi valide.")

        elif choice == '5':
            try:
                a = int(input("Introduceți coeficientul a: "))
                b = int(input("Introduceți coeficientul b: "))
                c = int(input("Introduceți termenul liber c: "))
                solve_diophantine(a, b, c)
            except ValueError:
                print("Eroare: Introduceți numere întregi valide.")

        else:
            print("Opțiune invalidă. Încercați din nou.")

        input("\nApăsați Enter pentru a continua...")


if __name__ == "__main__":
    main_menu()