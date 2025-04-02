import tkinter as tk
import math
from tkinter import scrolledtext, StringVar, Label, Entry, Button, Frame, ttk, IntVar, Radiobutton
from collections import defaultdict


class MathAlgorithmsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmi Matematici")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # First tab - Order of a natural number
        self.order_tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.order_tab, text="Ordinul unui număr natural")
        self.setup_order_tab()

        # Second tab - Decomposition into two squares
        self.decomp_tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.decomp_tab, text="Descompunere în sumă de două pătrate")
        self.setup_decomp_tab()

    def setup_order_tab(self):
        """Setup UI for the order of a natural number algorithm tab."""
        # Input frame
        input_frame = Frame(self.order_tab, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Number a
        Label(input_frame, text="a (număr natural):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.a_var = StringVar()
        Entry(input_frame, textvariable=self.a_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Modulus n
        Label(input_frame, text="n (modulul):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
        self.n_var = StringVar()
        Entry(input_frame, textvariable=self.n_var, width=20).grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = Frame(self.order_tab, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Calculează Ordinul", command=self.calculate_order,
               bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Șterge", command=self.clear_order_output,
               bg="#f44336", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Exemplu (a=2, n=11)", command=self.load_order_example,
               bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Output
        output_frame = Frame(self.order_tab, bg="#f0f0f0")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        Label(output_frame, text="Pași de calcul:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")

        self.order_output = scrolledtext.ScrolledText(output_frame, width=80, height=20, font=("Courier", 10))
        self.order_output.pack(fill=tk.BOTH, expand=True)

        # Result
        self.order_result = StringVar()
        Label(self.order_tab, textvariable=self.order_result, bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)

    def setup_decomp_tab(self):
        """Setup UI for the decomposition into two squares algorithm tab."""
        # Input frame
        input_frame = Frame(self.decomp_tab, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Number p
        Label(input_frame, text="p (număr prim de forma 4k+1):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.p_var = StringVar()
        Entry(input_frame, textvariable=self.p_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = Frame(self.decomp_tab, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Descompune în Sumă de Pătrate", command=self.decompose_into_squares,
               bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Șterge", command=self.clear_decomp_output,
               bg="#f44336", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Exemplu (p=461)", command=self.load_decomp_example,
               bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Output
        output_frame = Frame(self.decomp_tab, bg="#f0f0f0")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        Label(output_frame, text="Pași de calcul:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")

        self.decomp_output = scrolledtext.ScrolledText(output_frame, width=80, height=20, font=("Courier", 10))
        self.decomp_output.pack(fill=tk.BOTH, expand=True)

        # Result
        self.decomp_result = StringVar()
        Label(self.decomp_tab, textvariable=self.decomp_result, bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)

    def is_prime(self, n):
        """Check if a number is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def gcd(self, a, b):
        """Calculate the greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a

    def phi(self, n):
        """Calculate Euler's totient function φ(n)."""
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

    def factorize(self, n):
        """Factorize a number into its prime factors."""
        factors = defaultdict(int)
        while n % 2 == 0:
            factors[2] += 1
            n //= 2
        i = 3
        while i * i <= n:
            while n % i == 0:
                factors[i] += 1
                n //= i
            i += 2
        if n > 2:
            factors[n] += 1
        return factors

    def calculate_order(self):
        """Calculate the order of a number using the exact algorithm from the image."""
        try:
            a = int(self.a_var.get())
            n = int(self.n_var.get())

            self.order_output.delete(1.0, tk.END)
            self.order_output.insert(tk.END, f"Calcularea ordinului lui {a} modulo {n}\n")
            self.order_output.insert(tk.END, "-" * 60 + "\n\n")

            # Check if gcd(a, n) = 1
            if self.gcd(a, n) != 1:
                self.order_output.insert(tk.END, f"gcd({a}, {n}) ≠ 1, deci {a} nu are ordin modulo {n}\n")
                self.order_result.set("Nu există ordin (gcd ≠ 1)")
                return

            # Step 1: t ← φ(n)
            phi_n = self.phi(n)
            t = phi_n
            self.order_output.insert(tk.END, f"1. t ← φ({n}) = {phi_n}\n")

            # Factorize phi_n
            factors = self.factorize(phi_n)
            self.order_output.insert(tk.END, f"   Descompunerea lui φ({n}): {dict(factors)}\n")

            for p, exp in factors.items():
                self.order_output.insert(tk.END, f"2. Pentru factorul prim {p}^{exp}:\n")

                # Step 2.1: t ← t/(p^exp)
                t_temp = t // (p ** exp)
                self.order_output.insert(tk.END, f"   2.1. t ← t/{p}^{exp} = {t_temp}\n")

                # Step 2.2: a1 ← a^t_temp mod n
                a1 = pow(a, t_temp, n)
                self.order_output.insert(tk.END, f"   2.2. a1 ← {a}^{t_temp} mod {n} = {a1}\n")

                # Step 2.3: While a1 ≠ 1 mod n
                while a1 != 1:
                    # Step 2.3.1: a1 ← a1^p mod n
                    a1 = pow(a1, p, n)
                    self.order_output.insert(tk.END, f"   2.3.1. a1 ← a1^{p} mod {n} = {a1}\n")

                    # Step 2.3.2: t ← t * p
                    t = t * p
                    self.order_output.insert(tk.END, f"   2.3.2. t ← t * {p} = {t}\n")

                self.order_output.insert(tk.END, f"   După procesare, t = {t}\n")

            self.order_output.insert(tk.END, f"\nRezultat final:\n")
            self.order_result.set(f"Ordinul lui {a} modulo {n} este {t}")

            # Check if it's a primitive root
            if t == phi_n:
                self.order_output.insert(tk.END,
                                         f"\nDeoarece ordinul {t} = φ({n}), {a} este rădăcină primitivă modulo {n}\n")

        except ValueError:
            self.order_output.delete(1.0, tk.END)
            self.order_output.insert(tk.END, "Eroare: Verificați valorile de intrare. Trebuie să fie numere întregi.\n")
            self.order_result.set("Eroare de intrare")

    def decompose_into_squares(self):
        """Decompose a prime number p of the form 4k+1 into sum of two squares using Lagrange's algorithm."""
        try:
            p = int(self.p_var.get())

            self.decomp_output.delete(1.0, tk.END)
            self.decomp_output.insert(tk.END, f"Descompunerea numărului {p} în sumă de două pătrate\n")
            self.decomp_output.insert(tk.END, "-" * 60 + "\n\n")

            # Check if p is prime
            if not self.is_prime(p):
                self.decomp_output.insert(tk.END, f"{p} nu este prim. Algoritm aplicabil doar numerelor prime.\n")
                self.decomp_result.set("Numărul nu este prim")
                return

            # Check if p is of the form 4k+1
            if p % 4 != 1:
                self.decomp_output.insert(tk.END,
                                          f"{p} nu este de forma 4k+1. Algoritm aplicabil doar numerelor prime de forma 4k+1.\n")
                self.decomp_result.set("Numărul nu are forma 4k+1")
                return

            # Initialize variables as per the algorithm
            sqrt_p = math.isqrt(p)
            a = [sqrt_p]
            b = [0]
            c = [1]

            self.decomp_output.insert(tk.END, f"Initializare:\n")
            self.decomp_output.insert(tk.END, f"a₀ = [√{p}] = {a[0]}\n")
            self.decomp_output.insert(tk.END, f"b₀ = 0\n")
            self.decomp_output.insert(tk.END, f"c₀ = 1\n\n")

            i = 0
            max_iterations = 100  # Safety measure
            solution_found = False

            while i < max_iterations:
                # Calculate next b
                b_next = a[i] * c[i] - b[i]
                self.decomp_output.insert(tk.END, f"Iterația {i + 1}:\n")
                self.decomp_output.insert(tk.END,
                                          f"b_{i + 1} = a_{i}*c_{i} - b_{i} = {a[i]}*{c[i]} - {b[i]} = {b_next}\n")

                # Calculate next c
                c_next = (p - b_next ** 2) // c[i]
                self.decomp_output.insert(tk.END,
                                          f"c_{i + 1} = (p - b_{i + 1}²)/c_{i} = ({p} - {b_next}²)/{c[i]} = {c_next}\n")

                # Calculate next a
                a_next = (sqrt_p + b_next) // c_next
                self.decomp_output.insert(tk.END,
                                          f"a_{i + 1} = [(√{p} + b_{i + 1})/c_{i + 1}] = [({sqrt_p} + {b_next})/{c_next}] = {a_next}\n\n")

                # Append new values
                a.append(a_next)
                b.append(b_next)
                c.append(c_next)

                # Check if we found a solution
                if i > 0 and c[i + 1] == c[i]:
                    x = b[i + 1]
                    y = c[i]
                    if x ** 2 + y ** 2 == p:
                        self.decomp_output.insert(tk.END,
                                                  f"Am găsit soluția: {p} = {x}² + {y}² = {x ** 2} + {y ** 2}\n")
                        self.decomp_result.set(f"{p} = {x}² + {y}²")
                        solution_found = True
                        break

                i += 1

            if not solution_found:
                self.decomp_output.insert(tk.END, "Nu s-a găsit soluția după numărul maxim de iterații.\n")
                self.decomp_result.set("Nu s-a găsit descompunerea")

        except ValueError:
            self.decomp_output.delete(1.0, tk.END)
            self.decomp_output.insert(tk.END,
                                      "Eroare: Verificați valorile de intrare. Trebuie să fie numere întregi.\n")
            self.decomp_result.set("Eroare de intrare")

    def clear_order_output(self):
        """Clear the order tab output and inputs."""
        self.order_output.delete(1.0, tk.END)
        self.a_var.set("")
        self.n_var.set("")
        self.order_result.set("")

    def clear_decomp_output(self):
        """Clear the decomposition tab output and inputs."""
        self.decomp_output.delete(1.0, tk.END)
        self.p_var.set("")
        self.decomp_result.set("")

    def load_order_example(self):
        """Load the example for order calculation (a=2, n=11)."""
        self.a_var.set("2")
        self.n_var.set("11")
        self.calculate_order()

    def load_decomp_example(self):
        """Load the example for decomposition (p=461)."""
        self.p_var.set("461")
        self.decompose_into_squares()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = MathAlgorithmsApp(root)
    root.mainloop()