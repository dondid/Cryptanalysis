import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
from fractions import Fraction


class ContinuedFractionSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Rezolvator Fracții Continue")
        self.root.geometry("900x700")

        # Variabile
        self.n_var = tk.StringVar(value="160523347")
        self.b_var = tk.StringVar(value="60728973")

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurare grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Parametri de intrare", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(input_frame, text="n =").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        n_entry = ttk.Entry(input_frame, textvariable=self.n_var, width=20)
        n_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))

        ttk.Label(input_frame, text="b =").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        b_entry = ttk.Entry(input_frame, textvariable=self.b_var, width=20)
        b_entry.grid(row=0, column=3, sticky=(tk.W, tk.E))

        # Buton de calcul
        calc_button = ttk.Button(input_frame, text="Calculează", command=self.calculate)
        calc_button.grid(row=0, column=4, padx=(20, 0))

        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        # Rezultate
        results_frame = ttk.LabelFrame(main_frame, text="Rezultate și Explicații", padding="10")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, width=80, height=35)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        main_frame.rowconfigure(1, weight=1)

    def gcd(self, a, b):
        """Calculează cel mai mare divizor comun folosind algoritmul lui Euclid"""
        while b:
            a, b = b, a % b
        return a

    def factorize(self, n):
        """Factorizează un număr întreg"""
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

    def develop_continued_fraction(self, a, b):
        """Dezvoltă fracția a/b în fracție continuă"""
        quotients = []
        steps = []

        original_a, original_b = a, b

        while b != 0:
            q = a // b
            quotients.append(q)
            remainder = a % b
            steps.append({
                'dividend': a,
                'divisor': b,
                'quotient': q,
                'remainder': remainder
            })
            a, b = b, remainder

        return quotients, steps

    def calculate_convergents(self, quotients, num_convergents=10):
        """Calculează convergentele fracției continue"""
        convergents = []

        if len(quotients) == 0:
            return convergents

        # Primele două convergente
        h_prev2, h_prev1 = 0, 1
        k_prev2, k_prev1 = 1, 0

        for i, q in enumerate(quotients[:num_convergents]):
            h_curr = q * h_prev1 + h_prev2
            k_curr = q * k_prev1 + k_prev2

            convergents.append({
                'index': i,
                'quotient': q,
                'numerator': h_curr,
                'denominator': k_curr,
                'value': h_curr / k_curr if k_curr != 0 else float('inf')
            })

            h_prev2, h_prev1 = h_prev1, h_curr
            k_prev2, k_prev1 = k_prev1, k_curr

        return convergents

    def solve_quadratic_equation(self, n):
        """Rezolvă ecuația x² - (n - φ(n) + 1)x + n = 0"""
        # Calculăm φ(n) - funcția lui Euler
        phi_n = self.euler_totient(n)

        # Coeficienții ecuației: x² - (n - φ(n) + 1)x + n = 0
        a = 1
        b = -(n - phi_n + 1)
        c = n

        discriminant = b * b - 4 * a * c

        if discriminant >= 0:
            sqrt_discriminant = math.sqrt(discriminant)
            x1 = (-b + sqrt_discriminant) / (2 * a)
            x2 = (-b - sqrt_discriminant) / (2 * a)

            return {
                'phi_n': phi_n,
                'a': a,
                'b': b,
                'c': c,
                'discriminant': discriminant,
                'x1': x1,
                'x2': x2
            }
        else:
            return {
                'phi_n': phi_n,
                'a': a,
                'b': b,
                'c': c,
                'discriminant': discriminant,
                'x1': None,
                'x2': None
            }

    def euler_totient(self, n):
        """Calculează funcția φ(n) a lui Euler"""
        result = n
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result

    def calculate(self):
        try:
            n = int(self.n_var.get())
            b = int(self.b_var.get())

            if n <= 0 or b <= 0:
                messagebox.showerror("Eroare", "Valorile n și b trebuie să fie numere întregi pozitive")
                return

            # Șterge rezultatele anterioare
            self.results_text.delete(1.0, tk.END)

            # Afișează header-ul
            self.results_text.insert(tk.END, "=" * 80 + "\n")
            self.results_text.insert(tk.END, "REZOLVAREA PROBLEMEI DE FRACȚII CONTINUE\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")

            # 1. Dezvoltarea în fracție continuă
            self.results_text.insert(tk.END, f"1. DEZVOLTAREA FRACȚIEI {b}/{n} ÎN FRACȚIE CONTINUĂ\n")
            self.results_text.insert(tk.END, "-" * 60 + "\n\n")

            quotients, steps = self.develop_continued_fraction(b, n)

            self.results_text.insert(tk.END, "Algoritmul diviziunilor succesive:\n\n")

            for i, step in enumerate(steps):
                self.results_text.insert(tk.END,
                                         f"Pasul {i + 1}: {step['dividend']} = {step['quotient']} × {step['divisor']} + {step['remainder']}\n")

            self.results_text.insert(tk.END, f"\nCoeficienții fracției continue: {quotients}\n")
            self.results_text.insert(tk.END, f"Fracția continuă: [{', '.join(map(str, quotients))}]\n\n")

            # 2. Calcularea convergentelor
            self.results_text.insert(tk.END, "2. CALCULAREA CONVERGENTELOR\n")
            self.results_text.insert(tk.END, "-" * 60 + "\n\n")

            convergents = self.calculate_convergents(quotients, 10)

            self.results_text.insert(tk.END, "Convergentele sunt:\n\n")
            self.results_text.insert(tk.END, "Index | Coef | Numărător | Numitor | Valoare\n")
            self.results_text.insert(tk.END, "------|------|-----------|---------|----------\n")

            for conv in convergents:
                self.results_text.insert(tk.END,
                                         f"{conv['index']:5d} | {conv['quotient']:4d} | {conv['numerator']:9d} | {conv['denominator']:7d} | {conv['value']:.6f}\n")

            # 3. Verificarea convergenței
            if len(convergents) > 0:
                last_conv = convergents[-1]
                phi_n_frac = last_conv['numerator'] / last_conv['denominator']

                self.results_text.insert(tk.END, f"\nPentru fracția {b}/{n}, avem φ(n) ≈ {phi_n_frac:.6f}\n")

                # Verifică dacă |φ-1|
                error = abs(phi_n_frac - 1)
                self.results_text.insert(tk.END, f"Eroarea |φ-1| = {error:.6f}\n")

            # 4. Factorizarea lui n
            self.results_text.insert(tk.END, "\n3. FACTORIZAREA LUI n\n")
            self.results_text.insert(tk.END, "-" * 60 + "\n\n")

            factors = self.factorize(n)
            self.results_text.insert(tk.END, f"n = {n}\n")
            self.results_text.insert(tk.END, f"Factorii primi: {factors}\n")

            if len(factors) >= 2:
                p, q = factors[0], factors[1] if len(factors) > 1 else factors[0]
                self.results_text.insert(tk.END, f"n = {p} × {q}\n")

            # 5. Rezolvarea ecuației pătratice
            self.results_text.insert(tk.END, "\n4. REZOLVAREA ECUAȚIEI PĂTRATICE\n")
            self.results_text.insert(tk.END, "-" * 60 + "\n\n")

            quad_solution = self.solve_quadratic_equation(n)

            self.results_text.insert(tk.END, f"Calculăm φ(n) = {quad_solution['phi_n']}\n")
            self.results_text.insert(tk.END, f"Ecuația: x² - ({n} - {quad_solution['phi_n']} + 1)x + {n} = 0\n")
            self.results_text.insert(tk.END, f"Simplificat: x² - {-quad_solution['b']}x + {quad_solution['c']} = 0\n\n")

            if quad_solution['discriminant'] >= 0:
                self.results_text.insert(tk.END, f"Discriminantul Δ = {quad_solution['discriminant']}\n")
                self.results_text.insert(tk.END, f"√Δ = {math.sqrt(quad_solution['discriminant']):.6f}\n\n")

                if quad_solution['x1'] is not None:
                    self.results_text.insert(tk.END, f"Soluțiile ecuației:\n")
                    self.results_text.insert(tk.END, f"x₁ = {quad_solution['x1']:.6f}\n")
                    self.results_text.insert(tk.END, f"x₂ = {quad_solution['x2']:.6f}\n\n")

                    # Verifică dacă soluțiile sunt numere prime
                    if abs(quad_solution['x1'] - round(quad_solution['x1'])) < 1e-6:
                        p1 = int(round(quad_solution['x1']))
                        self.results_text.insert(tk.END, f"x₁ ≈ {p1} (număr întreg)\n")

                    if abs(quad_solution['x2'] - round(quad_solution['x2'])) < 1e-6:
                        p2 = int(round(quad_solution['x2']))
                        self.results_text.insert(tk.END, f"x₂ ≈ {p2} (număr întreg)\n")
            else:
                self.results_text.insert(tk.END, "Ecuația nu are soluții reale (discriminant negativ)\n")

            # 6. Concluzie
            self.results_text.insert(tk.END, "\n5. CONCLUZIE\n")
            self.results_text.insert(tk.END, "-" * 60 + "\n\n")

            self.results_text.insert(tk.END, f"Pentru n = {n} și b = {b}:\n")
            self.results_text.insert(tk.END, f"• Fracția continuă: [{', '.join(map(str, quotients))}]\n")
            self.results_text.insert(tk.END, f"• Numărul de convergente calculate: {len(convergents)}\n")
            self.results_text.insert(tk.END, f"• Factorizarea: {' × '.join(map(str, factors))}\n")

            if quad_solution['x1'] is not None:
                self.results_text.insert(tk.END,
                                         f"• Soluțiile ecuației pătratice: {quad_solution['x1']:.6f}, {quad_solution['x2']:.6f}\n")

            self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n")

        except ValueError:
            messagebox.showerror("Eroare", "Vă rugăm să introduceți numere întregi valide")
        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")


def main():
    root = tk.Tk()
    app = ContinuedFractionSolver(root)
    root.mainloop()


if __name__ == "__main__":
    main()