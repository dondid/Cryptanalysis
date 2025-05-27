import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
from fractions import Fraction


class NumberTheoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicații Teoria Numerelor")
        self.root.geometry("800x600")

        # Notebook pentru tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab-uri
        self.create_fraction_tab()
        self.create_congruence_tab()
        self.create_factorization_tab()

    def create_fraction_tab(self):
        # Tab pentru fracții continue
        frame1 = ttk.Frame(self.notebook)
        self.notebook.add(frame1, text="Fracții Continue")

        # Input-uri
        ttk.Label(frame1, text="Exercițiul 1: Fracții Continue", font=('Arial', 12, 'bold')).pack(pady=10)

        input_frame = ttk.Frame(frame1)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="n = ").grid(row=0, column=0, padx=5)
        self.n_entry = ttk.Entry(input_frame, width=15)
        self.n_entry.insert(0, "160523347")
        self.n_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="b = ").grid(row=0, column=2, padx=5)
        self.b_entry = ttk.Entry(input_frame, width=15)
        self.b_entry.insert(0, "60728973")
        self.b_entry.grid(row=0, column=3, padx=5)

        ttk.Button(input_frame, text="Calculează", command=self.calculate_continued_fraction).grid(row=0, column=4,
                                                                                                   padx=10)

        # Rezultate
        self.result_text1 = scrolledtext.ScrolledText(frame1, width=90, height=25)
        self.result_text1.pack(pady=10, fill='both', expand=True)

    def create_congruence_tab(self):
        # Tab pentru congruențe
        frame2 = ttk.Frame(self.notebook)
        self.notebook.add(frame2, text="Sisteme de Congruențe")

        ttk.Label(frame2, text="Exercițiul 2: Sisteme de Congruențe", font=('Arial', 12, 'bold')).pack(pady=10)

        input_frame2 = ttk.Frame(frame2)
        input_frame2.pack(pady=10)

        ttk.Label(input_frame2, text="n = ").grid(row=0, column=0, padx=5)
        self.n2_entry = ttk.Entry(input_frame2, width=10)
        self.n2_entry.insert(0, "403")
        self.n2_entry.grid(row=0, column=1, padx=5)

        ttk.Button(input_frame2, text="Calculează", command=self.solve_congruence_system).grid(row=0, column=2, padx=10)

        self.result_text2 = scrolledtext.ScrolledText(frame2, width=90, height=25)
        self.result_text2.pack(pady=10, fill='both', expand=True)

    def create_factorization_tab(self):
        # Tab pentru factorizare
        frame3 = ttk.Frame(self.notebook)
        self.notebook.add(frame3, text="Factorizare cu Bază")

        ttk.Label(frame3, text="Exercițiul 3: Factorizare cu Bază", font=('Arial', 12, 'bold')).pack(pady=10)

        input_frame3 = ttk.Frame(frame3)
        input_frame3.pack(pady=10)

        ttk.Label(input_frame3, text="n = ").grid(row=0, column=0, padx=5)
        self.n3_entry = ttk.Entry(input_frame3, width=10)
        self.n3_entry.insert(0, "84823")
        self.n3_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame3, text="Baza B = ").grid(row=1, column=0, padx=5)
        self.base_entry = ttk.Entry(input_frame3, width=20)
        self.base_entry.insert(0, "2,3,5,7")
        self.base_entry.grid(row=1, column=1, padx=5)

        ttk.Label(input_frame3, text="Numere de plecare = ").grid(row=2, column=0, padx=5)
        self.start_nums_entry = ttk.Entry(input_frame3, width=20)
        self.start_nums_entry.insert(0, "513,537")
        self.start_nums_entry.grid(row=2, column=1, padx=5)

        ttk.Button(input_frame3, text="Calculează", command=self.factorize_with_base).grid(row=3, column=0,
                                                                                           columnspan=2, pady=10)

        self.result_text3 = scrolledtext.ScrolledText(frame3, width=90, height=20)
        self.result_text3.pack(pady=10, fill='both', expand=True)

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def continued_fraction(self, n, d):
        """Calculează fracția continuă pentru n/d"""
        result = []
        while d != 0:
            q = n // d
            result.append(q)
            n, d = d, n - q * d
        return result

    def convergents(self, cf):
        """Calculează convergentele unei fracții continue"""
        if not cf:
            return []

        convergents = []
        p_prev, p_curr = 1, cf[0]
        q_prev, q_curr = 0, 1

        convergents.append((p_curr, q_curr))

        for i in range(1, len(cf)):
            p_next = cf[i] * p_curr + p_prev
            q_next = cf[i] * q_curr + q_prev
            convergents.append((p_next, q_next))
            p_prev, p_curr = p_curr, p_next
            q_prev, q_curr = q_curr, q_next

        return convergents

    def calculate_continued_fraction(self):
        try:
            n = int(self.n_entry.get())
            b = int(self.b_entry.get())

            self.result_text1.delete(1.0, tk.END)

            # Calculăm fracția continuă b/n
            cf = self.continued_fraction(b, n)
            self.result_text1.insert(tk.END, f"Fracția continuă pentru {b}/{n}:\n")
            self.result_text1.insert(tk.END, f"{cf}\n\n")

            # Calculăm convergentele
            conv = self.convergents(cf)
            self.result_text1.insert(tk.END, "Convergentele p_k/q_k pentru k = 1,2,...,10:\n")
            for i, (p, q) in enumerate(conv[:10]):
                self.result_text1.insert(tk.END, f"k={i + 1}: {p}/{q}\n")

            self.result_text1.insert(tk.END, "\n" + "=" * 50 + "\n")

            # Pentru fiecare convergentă verificăm condiția pentru t/a
            self.result_text1.insert(tk.END, "Verificare pentru forma t/a și calculul lui m:\n\n")

            for i, (p, q) in enumerate(conv[:10]):
                if i == 0:
                    continue

                # Verificăm dacă |ab - 1| este format de t și a
                ab_minus_1 = abs(p * q - 1)
                t = ab_minus_1
                a = 1  # încercăm cu a = 1 inițial

                # Căutăm factorizări ale lui ab-1
                factors = self.find_factors(ab_minus_1)

                self.result_text1.insert(tk.END, f"Convergenta k={i + 1}: p={p}, q={q}\n")
                self.result_text1.insert(tk.END, f"|ab - 1| = |{p}*{q} - 1| = {ab_minus_1}\n")

                if factors:
                    self.result_text1.insert(tk.END, f"Factori posibili pentru {ab_minus_1}: {factors}\n")

                    # Pentru fiecare factorizare calculăm m și rezolvăm ecuația
                    for t, a in factors:
                        if a != 0:
                            m = (p * q - 1) // t
                            self.result_text1.insert(tk.END, f"  Pentru t={t}, a={a}: m = {m}\n")

                            # Rezolvăm ecuația x² - (n - m + 1) + n = 0
                            # x² - (n - m + 1)x + n = 0
                            A = 1
                            B = -(n - m + 1)
                            C = n

                            discriminant = B * B - 4 * A * C
                            self.result_text1.insert(tk.END, f"  Ecuația: x² + {B}x + {C} = 0\n")
                            self.result_text1.insert(tk.END, f"  Discriminant: {discriminant}\n")

                            if discriminant >= 0:
                                sqrt_d = math.sqrt(discriminant)
                                if sqrt_d == int(sqrt_d):
                                    x1 = (-B + sqrt_d) / (2 * A)
                                    x2 = (-B - sqrt_d) / (2 * A)
                                    self.result_text1.insert(tk.END, f"  Soluții: x₁ = {x1}, x₂ = {x2}\n")

                                    # Verificăm dacă sunt numere prime
                                    if x1 > 0 and x1 == int(x1):
                                        if self.is_prime(int(x1)):
                                            self.result_text1.insert(tk.END, f"  x₁ = {int(x1)} este PRIM!\n")
                                    if x2 > 0 and x2 == int(x2):
                                        if self.is_prime(int(x2)):
                                            self.result_text1.insert(tk.END, f"  x₂ = {int(x2)} este PRIM!\n")

                self.result_text1.insert(tk.END, "\n")

        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la calculul fracției continue: {str(e)}")

    def find_factors(self, n):
        """Găsește toți factorii unui număr"""
        factors = []
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                factors.append((i, n // i))
                if i != n // i:
                    factors.append((n // i, i))
        return factors

    def is_prime(self, n):
        """Verifică dacă un număr este prim"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def solve_congruence_system(self):
        try:
            n = int(self.n2_entry.get())

            self.result_text2.delete(1.0, tk.END)

            # Descompunem n în factori primi
            factors = self.prime_factorization(n)
            self.result_text2.insert(tk.END, f"Descompunerea în factori primi a lui {n}:\n")
            self.result_text2.insert(tk.END, f"{n} = {' × '.join(map(str, factors))}\n\n")

            # Verificăm dacă factorii sunt congruenți cu 3 (mod 4)
            p, q = factors[0], factors[1] if len(factors) > 1 else factors[0]

            self.result_text2.insert(tk.END, f"p = {p}, q = {q}\n")
            self.result_text2.insert(tk.END, f"p ≡ {p % 4} (mod 4)\n")
            self.result_text2.insert(tk.END, f"q ≡ {q % 4} (mod 4)\n\n")

            if p % 4 == 3 and q % 4 == 3:
                self.result_text2.insert(tk.END, "Ambele numere sunt congruente cu 3 (mod 4)\n\n")

                # Rezolvăm sistemul de congruențe
                self.result_text2.insert(tk.END, "Rezolvăm sistemul:\n")
                self.result_text2.insert(tk.END, "x ≡ ±1 (mod p)\n")
                self.result_text2.insert(tk.END, "x ≡ ±1 (mod q)\n\n")

                # Toate combinațiile posibile
                solutions = []
                for sign1 in [1, -1]:
                    for sign2 in [1, -1]:
                        # Rezolvăm x ≡ sign1 (mod p) și x ≡ sign2 (mod q)
                        sol = self.chinese_remainder_theorem(sign1, p, sign2, q)
                        if sol is not None:
                            solutions.append(sol % n)

                self.result_text2.insert(tk.END, "Soluții găsite prin Teorema Chineză a Resturilor:\n")
                for i, sol in enumerate(set(solutions)):
                    self.result_text2.insert(tk.END, f"x_{i + 1} ≡ {sol} (mod {n})\n")

                self.result_text2.insert(tk.END, f"\nRădăcinile pătratice ale lui 1 modulo {n} sunt:\n")
                for sol in set(solutions):
                    self.result_text2.insert(tk.END, f"{sol}, ")

        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la rezolvarea sistemului: {str(e)}")

    def prime_factorization(self, n):
        """Descompune un număr în factori primi"""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors

    def chinese_remainder_theorem(self, a1, m1, a2, m2):
        """Rezolvă sistemul x ≡ a1 (mod m1), x ≡ a2 (mod m2)"""
        gcd, x, y = self.extended_gcd(m1, m2)
        if gcd != 1:
            return None  # Nu există soluție unică

        solution = (a1 * m2 * y + a2 * m1 * x) % (m1 * m2)
        return solution

    def factorize_with_base(self):
        try:
            n = int(self.n3_entry.get())
            base = list(map(int, self.base_entry.get().split(',')))
            start_nums = list(map(int, self.start_nums_entry.get().split(',')))

            self.result_text3.delete(1.0, tk.END)

            self.result_text3.insert(tk.END, f"Factorizarea lui n = {n}\n")
            self.result_text3.insert(tk.END, f"Baza B = {base}\n")
            self.result_text3.insert(tk.END, f"Numere de plecare: {start_nums}\n\n")

            # Pentru fiecare număr de plecare, calculăm x² mod n
            smooth_numbers = []

            for x in start_nums:
                x_squared = x * x
                remainder = x_squared % n

                self.result_text3.insert(tk.END, f"Pentru x = {x}:\n")
                self.result_text3.insert(tk.END, f"x² = {x_squared}\n")
                self.result_text3.insert(tk.END, f"x² ≡ {remainder} (mod {n})\n")

                # Verificăm dacă remainder este smooth cu baza B
                factorization = self.factorize_with_given_base(remainder, base)
                if factorization is not None:
                    self.result_text3.insert(tk.END, f"{remainder} este B-smooth: {factorization}\n")
                    smooth_numbers.append((x, remainder, factorization))
                else:
                    self.result_text3.insert(tk.END, f"{remainder} NU este B-smooth cu baza dată\n")

                self.result_text3.insert(tk.END, "\n")

            if len(smooth_numbers) >= 2:
                self.result_text3.insert(tk.END, "Numere B-smooth găsite:\n")
                for x, remainder, fact in smooth_numbers:
                    self.result_text3.insert(tk.END, f"x = {x}: {remainder} = {fact}\n")

                # Încercăm să găsim o relație de congruență
                self.result_text3.insert(tk.END, "\nCăutăm relații de congruență...\n")

                # Exemplu simplu: dacă avem două pătrate perfecte
                if len(smooth_numbers) >= 2:
                    x1, r1, f1 = smooth_numbers[0]
                    x2, r2, f2 = smooth_numbers[1]

                    # Verificăm dacă produsul exponenților este par
                    self.result_text3.insert(tk.END, f"\nAnalizăm {x1}² ≡ {r1} (mod {n}) și {x2}² ≡ {r2} (mod {n})\n")

                    # Calculăm gcd(x1 - x2, n) și gcd(x1 + x2, n)
                    gcd1 = self.gcd(abs(x1 - x2), n)
                    gcd2 = self.gcd(x1 + x2, n)

                    self.result_text3.insert(tk.END, f"gcd(|{x1} - {x2}|, {n}) = gcd({abs(x1 - x2)}, {n}) = {gcd1}\n")
                    self.result_text3.insert(tk.END, f"gcd({x1} + {x2}, {n}) = gcd({x1 + x2}, {n}) = {gcd2}\n")

                    if 1 < gcd1 < n:
                        self.result_text3.insert(tk.END, f"\nFactor găsit: {gcd1}\n")
                        self.result_text3.insert(tk.END, f"Factorizarea: {n} = {gcd1} × {n // gcd1}\n")
                    elif 1 < gcd2 < n:
                        self.result_text3.insert(tk.END, f"\nFactor găsit: {gcd2}\n")
                        self.result_text3.insert(tk.END, f"Factorizarea: {n} = {gcd2} × {n // gcd2}\n")
                    else:
                        # Încercăm o abordare diferită
                        product = r1 * r2
                        sqrt_product = int(math.sqrt(product))
                        if sqrt_product * sqrt_product == product:
                            y = sqrt_product
                            x_combined = (x1 * x2) % n

                            gcd3 = self.gcd(abs(x_combined - y), n)
                            gcd4 = self.gcd(x_combined + y, n)

                            self.result_text3.insert(tk.END, f"\nProdusul resturilor: {product} = {sqrt_product}²\n")
                            self.result_text3.insert(tk.END, f"gcd(|{x_combined} - {y}|, {n}) = {gcd3}\n")
                            self.result_text3.insert(tk.END, f"gcd({x_combined} + {y}, {n}) = {gcd4}\n")

                            if 1 < gcd3 < n:
                                self.result_text3.insert(tk.END, f"\nFactor găsit: {gcd3}\n")
                                self.result_text3.insert(tk.END, f"Factorizarea: {n} = {gcd3} × {n // gcd3}\n")
                            elif 1 < gcd4 < n:
                                self.result_text3.insert(tk.END, f"\nFactor găsit: {gcd4}\n")
                                self.result_text3.insert(tk.END, f"Factorizarea: {n} = {gcd4} × {n // gcd4}\n")

        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la factorizarea cu bază: {str(e)}")

    def factorize_with_given_base(self, n, base):
        """Încearcă să factorizeze n folosind doar numerele din baza dată"""
        original_n = n
        factorization = {}

        for prime in base:
            while n % prime == 0:
                factorization[prime] = factorization.get(prime, 0) + 1
                n //= prime

        if n == 1:  # Numărul este complet factorizat cu baza
            return factorization
        else:
            return None  # Nu este B-smooth


def main():
    root = tk.Tk()
    app = NumberTheoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()