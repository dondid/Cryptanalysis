import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import random
from fractions import Fraction


class DixonFactorization:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmul lui Dixon - Factorizare")
        self.root.geometry("900x700")

        # Variabile
        self.n = tk.StringVar(value="1577070841")
        self.base_primes = tk.StringVar(value="2,3,5,7,11,13")
        self.max_attempts = tk.StringVar(value="1000")

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurare input
        input_frame = ttk.LabelFrame(main_frame, text="Parametri", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(input_frame, text="Numărul de factorizat (n):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.n, width=20).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        ttk.Label(input_frame, text="Baza de primi (separați prin virgulă):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.base_primes, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E),
                                                                             pady=2)

        ttk.Label(input_frame, text="Numărul maxim de încercări:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.max_attempts, width=10).grid(row=2, column=1, sticky=tk.W, pady=2)

        # Butoane
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Rulează Algoritmul Dixon",
                   command=self.run_dixon).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Șterge Rezultate",
                   command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exemplu din Imagine",
                   command=self.load_example).pack(side=tk.LEFT, padx=5)

        # Zona de rezultate
        result_frame = ttk.LabelFrame(main_frame, text="Rezultate și Pași", padding="10")
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.result_text = scrolledtext.ScrolledText(result_frame, width=100, height=30, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurare grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)

    def load_example(self):
        """Încarcă exemplul din imagine"""
        self.n.set("1577070841")
        self.base_primes.set("2,3,5,7,11,13")
        self.max_attempts.set("1000")

    def clear_results(self):
        """Șterge rezultatele"""
        self.result_text.delete(1.0, tk.END)

    def log(self, message):
        """Adaugă mesaj în zona de rezultate"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update()

    def is_perfect_square(self, n):
        """Verifică dacă un număr este pătrat perfect"""
        sqrt_n = int(math.sqrt(n))
        return sqrt_n * sqrt_n == n

    def gcd(self, a, b):
        """Calculează cel mai mare divizor comun"""
        while b:
            a, b = b, a % b
        return a

    def legendre_symbol(self, a, p):
        """Calculează simbolul Legendre pentru a verifică dacă a este reziduu pătratic modulo p"""
        if p == 2:
            return 1 if a % 2 == 1 else 0

        a = a % p
        if a == 0:
            return 0

        result = 1
        while a != 1:
            while a % 2 == 0:
                a //= 2
                if p % 8 in [3, 5]:
                    result = -result
            a, p = p, a
            if a % 4 == 3 and p % 4 == 3:
                result = -result
            a = a % p
        return 1 if result == 1 else 0

    def factor_in_base(self, num, base):
        """Factorizează un număr în baza de primi dată"""
        factors = {}
        remaining = abs(num)

        for prime in base:
            factors[prime] = 0
            while remaining % prime == 0:
                remaining //= prime
                factors[prime] += 1

        return factors if remaining == 1 else None

    def find_smooth_numbers(self, n, base, max_attempts):
        """Găsește numere smooth (B-smooth) pentru algoritmul Dixon"""
        smooth_numbers = []
        self.log(f"\n=== CĂUTAREA NUMERELOR B-SMOOTH ===")
        self.log(f"Căutăm numere x pentru care x² ≡ y² (mod {n}) și y² se factorizează în baza B = {base}")

        # Avem nevoie de cel puțin len(base)+1 numere pentru a avea o dependență liniară
        needed = len(base) + 2  # Luăm câteva în plus pentru siguranță

        attempts = 0
        x = int(math.sqrt(n)) + 1  # Începem de la sqrt(n)

        while len(smooth_numbers) < needed and attempts < max_attempts:
            x_squared = x * x
            remainder = x_squared % n

            # Verificăm dacă remainder se factorizează în baza dată
            factorization = self.factor_in_base(remainder, base)

            if factorization is not None:
                smooth_numbers.append((x, remainder, factorization))
                self.log(f"\n✓ Găsit #{len(smooth_numbers)}: x = {x}")
                self.log(f"  x² = {x_squared}")
                self.log(f"  x² ≡ {remainder} (mod {n})")

                # Afișează factorizarea
                factor_parts = []
                for p, exp in factorization.items():
                    if exp > 0:
                        if exp == 1:
                            factor_parts.append(str(p))
                        else:
                            factor_parts.append(f"{p}^{exp}")

                if factor_parts:
                    factor_str = " × ".join(factor_parts)
                    self.log(f"  Factorizare: {remainder} = {factor_str}")
                else:
                    self.log(f"  Factorizare: {remainder} = 1")

            attempts += 1
            x += 1

            # Dacă nu găsim suficiente cu căutarea secvențială, încercăm și alte valori
            if attempts > max_attempts // 2 and len(smooth_numbers) < needed:
                # Încercăm și cu valori random în jurul sqrt(n)
                base_x = int(math.sqrt(n))
                x = base_x + random.randint(-base_x // 4, base_x // 4)
                if x <= 1:
                    x = base_x + random.randint(1, 1000)

        self.log(f"\nAm găsit {len(smooth_numbers)} numere B-smooth din {attempts} încercări.")
        self.log(f"Sunt necesare cel puțin {len(base) + 1} pentru a găsi dependențe liniare.")

        return smooth_numbers

    def find_linear_dependencies(self, matrix):
        """Găsește dependențe liniare în matricea exponenților modulo 2"""
        if not matrix:
            return []

        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        # Pentru a găsi dependențe, avem nevoie de mai multe rânduri decât coloane
        if rows <= cols:
            return []

        # Construim matricea extinsă pentru a urmări combinațiile
        extended_matrix = []
        for i in range(rows):
            # Rândul original + vectorul unitate pentru a urmări combinația
            row = matrix[i][:] + [0] * rows
            row[cols + i] = 1  # Vectorul unitate
            extended_matrix.append(row)

        # Eliminare Gaussiană modulo 2
        pivot_col = 0
        for row in range(rows):
            if pivot_col >= cols:
                break

            # Găsim pivot în coloana curentă
            pivot_row = -1
            for r in range(row, rows):
                if extended_matrix[r][pivot_col] == 1:
                    pivot_row = r
                    break

            if pivot_row == -1:
                # Nu există pivot în această coloană, trecem la următoarea
                pivot_col += 1
                row -= 1  # Rămânem pe același rând
                continue

            # Schimbăm rândurile dacă e necesar
            if pivot_row != row:
                extended_matrix[row], extended_matrix[pivot_row] = extended_matrix[pivot_row], extended_matrix[row]

            # Eliminăm în coloana pivot_col
            for r in range(rows):
                if r != row and extended_matrix[r][pivot_col] == 1:
                    for c in range(cols + rows):
                        extended_matrix[r][c] ^= extended_matrix[row][c]

            pivot_col += 1

        # Găsim rândurile care au devenit zero în partea stângă (dependențe)
        dependencies = []
        for row in range(rows):
            if all(extended_matrix[row][col] == 0 for col in range(cols)):
                # Acest rând reprezintă o dependență liniară
                combination = []
                for i in range(rows):
                    if extended_matrix[row][cols + i] == 1:
                        combination.append(i)
                if len(combination) > 1:  # Trebuie să avem cel puțin 2 elemente
                    dependencies.append(combination)

        return dependencies

    def run_dixon(self):
        """Rulează algoritmul Dixon"""
        try:
            self.clear_results()

            # Parsează input-ul
            n = int(self.n.get())
            base = [int(x.strip()) for x in self.base_primes.get().split(',')]
            max_attempts = int(self.max_attempts.get())

            self.log("=== ALGORITMUL LUI DIXON ===")
            self.log(f"Factorizăm n = {n}")
            self.log(f"Folosind baza B = {base}")
            self.log(f"Număr maxim de încercări: {max_attempts}")

            # Verificări inițiale
            if self.is_perfect_square(n):
                sqrt_n = int(math.sqrt(n))
                self.log(f"\n✓ REZULTAT: {n} = {sqrt_n}²")
                return

            # Pas 1: Găsește numere B-smooth
            smooth_numbers = self.find_smooth_numbers(n, base, max_attempts)

            if len(smooth_numbers) < len(base) + 1:
                self.log(f"\n❌ EROARE: Nu am găsit suficiente numere B-smooth!")
                self.log(f"   Necesare: {len(base) + 1}, Găsite: {len(smooth_numbers)}")
                return

            # Pas 2: Construiește matricea exponenților modulo 2
            self.log(f"\n=== CONSTRUIREA MATRICEI EXPONENȚILOR ===")
            matrix = []
            for x, remainder, factorization in smooth_numbers:
                row = []
                for prime in base:
                    exp = factorization.get(prime, 0)
                    row.append(exp % 2)
                matrix.append(row)

            # Afișează matricea
            self.log("Matricea exponenților modulo 2:")
            header = "x\t" + "\t".join(str(p) for p in base)
            self.log(header)
            self.log("-" * len(header))
            for i, (x, _, _) in enumerate(smooth_numbers):
                row_str = f"{x}\t" + "\t".join(str(matrix[i][j]) for j in range(len(base)))
                self.log(row_str)

            # Pas 3: Găsește dependențe liniare
            self.log(f"\n=== GĂSIREA DEPENDENȚELOR LINIARE ===")
            dependencies = self.find_linear_dependencies(matrix)

            if not dependencies:
                self.log("❌ Nu s-au găsit dependențe liniare!")
                self.log("Încearcă să mărești numărul maxim de încercări sau să modifici baza de primi.")
                return

            self.log(f"✓ Găsite {len(dependencies)} dependențe liniare")
            for i, dep in enumerate(dependencies):
                indices_str = ", ".join(str(idx) for idx in dep)
                self.log(f"  Dependența {i + 1}: rândurile {indices_str}")

            # Pas 4: Construiește congruențe și calculează factori
            self.log(f"\n=== CALCULAREA FACTORILOR ===")

            for dep_idx, combination in enumerate(dependencies):
                self.log(f"\n--- Folosind dependența {dep_idx + 1} ---")
                self.log(f"Combinăm rândurile: {combination}")

                # Calculează produsul x-urilor din combinație
                x_product = 1
                y_squared_factors = {p: 0 for p in base}

                x_values = []
                for i in combination:
                    x, remainder, factorization = smooth_numbers[i]
                    x_values.append(x)
                    x_product = (x_product * x) % n

                    for prime in base:
                        y_squared_factors[prime] += factorization.get(prime, 0)

                self.log(f"x-uri folosite: {x_values}")
                self.log(f"Produsul x-urilor: {' × '.join(map(str, x_values))} ≡ {x_product} (mod {n})")

                # Calculează y din exponenții înjumătățiți
                y = 1
                y_factors = []
                for prime in base:
                    total_exp = y_squared_factors[prime]
                    if total_exp > 0:
                        half_exp = total_exp // 2
                        if half_exp > 0:
                            y = (y * pow(prime, half_exp)) % n
                            if half_exp == 1:
                                y_factors.append(str(prime))
                            else:
                                y_factors.append(f"{prime}^{half_exp}")

                if y_factors:
                    self.log(f"y = {' × '.join(y_factors)} ≡ {y} (mod {n})")
                else:
                    self.log(f"y = 1")

                # Verifică congruența x² ≡ y² (mod n)
                x_sq = (x_product * x_product) % n
                y_sq = (y * y) % n

                self.log(f"\nVerificare congruență:")
                self.log(f"x² ≡ {x_product}² ≡ {x_sq} (mod {n})")
                self.log(f"y² ≡ {y}² ≡ {y_sq} (mod {n})")

                if x_sq == y_sq:
                    self.log(f"✓ Congruența este corectă: x² ≡ y² (mod {n})")

                    # Calculează gcd pentru factorizare
                    if x_product != y and x_product != (n - y):
                        diff = (x_product - y) % n
                        suma = (x_product + y) % n

                        factor1 = self.gcd(diff, n)
                        factor2 = self.gcd(suma, n)

                        self.log(f"\nCalcul factori:")
                        self.log(f"gcd({x_product} - {y}, {n}) = gcd({diff}, {n}) = {factor1}")
                        self.log(f"gcd({x_product} + {y}, {n}) = gcd({suma}, {n}) = {factor2}")

                        if 1 < factor1 < n:
                            other_factor = n // factor1
                            self.log(f"\n🎉 FACTORIZARE REUȘITĂ!")
                            self.log(f"{n} = {factor1} × {other_factor}")

                            # Verificare finală
                            if factor1 * other_factor == n:
                                self.log(f"✓ Verificare: {factor1} × {other_factor} = {n}")

                                # Verificăm dacă sunt primi
                                if self.is_likely_prime(factor1) and self.is_likely_prime(other_factor):
                                    self.log(f"✓ Ambii factori par să fie primi!")
                                else:
                                    self.log(f"ℹ️  Factorii pot fi factorizați mai departe.")
                            return

                        if 1 < factor2 < n:
                            other_factor = n // factor2
                            self.log(f"\n🎉 FACTORIZARE REUȘITĂ!")
                            self.log(f"{n} = {factor2} × {other_factor}")

                            # Verificare finală
                            if factor2 * other_factor == n:
                                self.log(f"✓ Verificare: {factor2} × {other_factor} = {n}")

                                # Verificăm dacă sunt primi
                                if self.is_likely_prime(factor2) and self.is_likely_prime(other_factor):
                                    self.log(f"✓ Ambii factori par să fie primi!")
                                else:
                                    self.log(f"ℹ️  Factorii pot fi factorizați mai departe.")
                            return

                        self.log(f"❌ Factorii găsiți sunt triviali: {factor1}, {factor2}")
                    else:
                        self.log(f"❌ x ≡ ±y (mod n), această dependență nu dă o factorizare utilă.")
                else:
                    self.log(f"❌ Congruența nu se verifică: {x_sq} ≠ {y_sq}")

            self.log(f"\n❌ Nu s-a găsit o factorizare utilizabilă cu dependențele disponibile.")
            self.log("Încearcă să mărești numărul de încercări sau să modifici baza de primi.")

        except ValueError as e:
            messagebox.showerror("Eroare", f"Valoare invalidă: {e}")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la execuție: {e}")


def main():
    root = tk.Tk()
    app = DixonFactorization(root)
    root.mainloop()


if __name__ == "__main__":
    main()