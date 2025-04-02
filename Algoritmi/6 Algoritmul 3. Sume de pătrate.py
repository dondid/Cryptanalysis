import tkinter as tk
import math
from tkinter import scrolledtext, StringVar, Label, Entry, Button, Frame, ttk, IntVar, Radiobutton
from collections import defaultdict


class MathAlgorithmsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmi Matematici Avansați")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # First tab - Square sums decomposition
        self.square_tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.square_tab, text="Sumă de pătrate")
        self.setup_square_tab()

        # Second tab - Legendre symbol
        self.legendre_tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.legendre_tab, text="Simbolul Legendre")
        self.setup_legendre_tab()

        # Third tab - Jacobi symbol
        self.jacobi_tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.jacobi_tab, text="Simbolul Jacobi")
        self.setup_jacobi_tab()

    def setup_square_tab(self):
        """Setup UI for the square sums decomposition tab."""
        # Input frame
        input_frame = Frame(self.square_tab, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Prime number p
        Label(input_frame, text="p (număr prim de forma 4k+1):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.p_var = StringVar()
        Entry(input_frame, textvariable=self.p_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = Frame(self.square_tab, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Descompune în Pătrate", command=self.decompose_into_squares,
               bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Șterge", command=self.clear_square_output,
               bg="#f44336", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Exemplu (p=461)", command=self.load_square_example,
               bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Output
        output_frame = Frame(self.square_tab, bg="#f0f0f0")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        Label(output_frame, text="Pași de calcul:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")

        self.square_output = scrolledtext.ScrolledText(output_frame, width=90, height=20, font=("Courier", 10))
        self.square_output.pack(fill=tk.BOTH, expand=True)

        # Result
        self.square_result = StringVar()
        Label(self.square_tab, textvariable=self.square_result, bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)

    def setup_legendre_tab(self):
        """Setup UI for the Legendre symbol calculation tab."""
        # Input frame
        input_frame = Frame(self.legendre_tab, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Number a
        Label(input_frame, text="a (număr întreg):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.a_leg_var = StringVar()
        Entry(input_frame, textvariable=self.a_leg_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Prime p
        Label(input_frame, text="p (număr prim impar):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
        self.p_leg_var = StringVar()
        Entry(input_frame, textvariable=self.p_leg_var, width=20).grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = Frame(self.legendre_tab, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Calculează Simbolul", command=self.calculate_legendre,
               bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Șterge", command=self.clear_legendre_output,
               bg="#f44336", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Exemplu (a=14, p=17)", command=self.load_legendre_example,
               bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Output
        output_frame = Frame(self.legendre_tab, bg="#f0f0f0")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        Label(output_frame, text="Pași de calcul:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")

        self.legendre_output = scrolledtext.ScrolledText(output_frame, width=90, height=20, font=("Courier", 10))
        self.legendre_output.pack(fill=tk.BOTH, expand=True)

        # Result
        self.legendre_result = StringVar()
        Label(self.legendre_tab, textvariable=self.legendre_result, bg="#f0f0f0", font=("Arial", 12, "bold")).pack(
            pady=10)

    def setup_jacobi_tab(self):
        """Setup UI for the Jacobi symbol calculation tab."""
        # Input frame
        input_frame = Frame(self.jacobi_tab, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Number a
        Label(input_frame, text="a (număr întreg):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.a_jac_var = StringVar()
        Entry(input_frame, textvariable=self.a_jac_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Odd n
        Label(input_frame, text="n (număr impar):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
        self.n_jac_var = StringVar()
        Entry(input_frame, textvariable=self.n_jac_var, width=20).grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = Frame(self.jacobi_tab, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Calculează Simbolul", command=self.calculate_jacobi,
               bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Șterge", command=self.clear_jacobi_output,
               bg="#f44336", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        Button(btn_frame, text="Exemplu (a=14, n=1275)", command=self.load_jacobi_example,
               bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Output
        output_frame = Frame(self.jacobi_tab, bg="#f0f0f0")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        Label(output_frame, text="Pași de calcul:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")

        self.jacobi_output = scrolledtext.ScrolledText(output_frame, width=90, height=20, font=("Courier", 10))
        self.jacobi_output.pack(fill=tk.BOTH, expand=True)

        # Result
        self.jacobi_result = StringVar()
        Label(self.jacobi_tab, textvariable=self.jacobi_result, bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)

    # Helper methods
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

    # Square sums decomposition algorithm
    def decompose_into_squares(self):
        """Decompose a prime number p of the form 4k+1 into sum of two squares."""
        try:
            p = int(self.p_var.get())

            self.square_output.delete(1.0, tk.END)
            self.square_output.insert(tk.END, f"Descompunerea numărului {p} în sumă de două pătrate\n")
            self.square_output.insert(tk.END, "-" * 80 + "\n\n")

            # Check if p is prime
            if not self.is_prime(p):
                self.square_output.insert(tk.END, f"{p} nu este prim. Algoritm aplicabil doar numerelor prime.\n")
                self.square_result.set("Numărul nu este prim")
                return

            # Check if p is of the form 4k+1
            if p % 4 != 1:
                self.square_output.insert(tk.END,
                                          f"{p} nu este de forma 4k+1. Algoritm aplicabil doar numerelor prime de forma 4k+1.\n")
                self.square_result.set("Numărul nu are forma 4k+1")
                return

            # Initialize variables as per the algorithm
            sqrt_p = math.isqrt(p)
            a = [sqrt_p]
            b = [0]
            c = [1]

            self.square_output.insert(tk.END, f"Initializare:\n")
            self.square_output.insert(tk.END, f"a₀ = [√{p}] = {a[0]}\n")
            self.square_output.insert(tk.END, f"b₀ = 0\n")
            self.square_output.insert(tk.END, f"c₀ = 1\n\n")

            i = 0
            max_iterations = 100  # Safety measure
            solution_found = False

            while i < max_iterations:
                # Calculate next b
                b_next = a[i] * c[i] - b[i]
                self.square_output.insert(tk.END, f"Iterația {i + 1}:\n")
                self.square_output.insert(tk.END,
                                          f"b_{i + 1} = a_{i}*c_{i} - b_{i} = {a[i]}*{c[i]} - {b[i]} = {b_next}\n")

                # Calculate next c
                c_next = (p - b_next ** 2) // c[i]
                self.square_output.insert(tk.END,
                                          f"c_{i + 1} = (p - b_{i + 1}²)/c_{i} = ({p} - {b_next}²)/{c[i]} = {c_next}\n")

                # Calculate next a
                a_next = (sqrt_p + b_next) // c_next
                self.square_output.insert(tk.END,
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
                        self.square_output.insert(tk.END,
                                                  f"Am găsit soluția: {p} = {x}² + {y}² = {x ** 2} + {y ** 2}\n")
                        self.square_result.set(f"{p} = {x}² + {y}²")
                        solution_found = True
                        break

                i += 1

            if not solution_found:
                self.square_output.insert(tk.END, "Nu s-a găsit soluția după numărul maxim de iterații.\n")
                self.square_result.set("Nu s-a găsit descompunerea")

        except ValueError:
            self.square_output.delete(1.0, tk.END)
            self.square_output.insert(tk.END,
                                      "Eroare: Verificați valorile de intrare. Trebuie să fie numere întregi.\n")
            self.square_result.set("Eroare de intrare")

    # Legendre symbol calculation
    def calculate_legendre(self):
        """Calculate the Legendre symbol (a/p) using Euler's criterion."""
        try:
            a = int(self.a_leg_var.get())
            p = int(self.p_leg_var.get())

            self.legendre_output.delete(1.0, tk.END)
            self.legendre_output.insert(tk.END, f"Calcularea simbolului Legendre ({a}/{p})\n")
            self.legendre_output.insert(tk.END, "-" * 80 + "\n\n")

            # Check if p is an odd prime
            if p == 2 or not self.is_prime(p):
                self.legendre_output.insert(tk.END,
                                            f"{p} nu este un număr prim impar. Simbolul Legendre este definit doar pentru numere prime impare.\n")
                self.legendre_result.set("p trebuie să fie prim impar")
                return

            # Check if a is divisible by p
            if a % p == 0:
                self.legendre_output.insert(tk.END, f"{a} este divizibil cu {p}\n")
                self.legendre_output.insert(tk.END, f"Rezultat: ({a}/{p}) = 0\n")
                self.legendre_result.set(f"({a}/{p}) = 0")
                return

            # Calculate using Euler's criterion
            exponent = (p - 1) // 2
            result = pow(a, exponent, p)

            self.legendre_output.insert(tk.END, f"Calculăm a^((p-1)/2) mod p:\n")
            self.legendre_output.insert(tk.END, f"({p}-1)/2 = {exponent}\n")
            self.legendre_output.insert(tk.END, f"{a}^{exponent} mod {p} = {result}\n\n")

            if result == 1:
                self.legendre_output.insert(tk.END, f"Rezultat: ({a}/{p}) = 1 (a este rest pătratic modulo {p})\n")
                self.legendre_result.set(f"({a}/{p}) = 1")
            elif result == p - 1:
                self.legendre_output.insert(tk.END, f"Rezultat: ({a}/{p}) = -1 (a NU este rest pătratic modulo {p})\n")
                self.legendre_result.set(f"({a}/{p}) = -1")
            else:
                self.legendre_output.insert(tk.END, f"Rezultat neașteptat: {result}\n")
                self.legendre_result.set("Eroare de calcul")

        except ValueError:
            self.legendre_output.delete(1.0, tk.END)
            self.legendre_output.insert(tk.END,
                                        "Eroare: Verificați valorile de intrare. Trebuie să fie numere întregi.\n")
            self.legendre_result.set("Eroare de intrare")

    # Jacobi symbol calculation
    def calculate_jacobi(self):
        """Calculate the Jacobi symbol (a/n) using the algorithm."""
        try:
            a = int(self.a_jac_var.get())
            n = int(self.n_jac_var.get())

            self.jacobi_output.delete(1.0, tk.END)
            self.jacobi_output.insert(tk.END, f"Calcularea simbolului Jacobi ({a}/{n})\n")
            self.jacobi_output.insert(tk.END, "-" * 80 + "\n\n")

            # Check if n is odd
            if n % 2 == 0 or n <= 0:
                self.jacobi_output.insert(tk.END,
                                          f"{n} nu este un număr impar pozitiv. Simbolul Jacobi este definit doar pentru numere impare pozitive.\n")
                self.jacobi_result.set("n trebuie să fie impar pozitiv")
                return

            # Handle the case when gcd(a, n) != 1
            if self.gcd(a, n) != 1:
                self.jacobi_output.insert(tk.END, f"CMMDC({a}, {n}) ≠ 1\n")
                self.jacobi_output.insert(tk.END, f"Rezultat: ({a}/{n}) = 0\n")
                self.jacobi_result.set(f"({a}/{n}) = 0")
                return

            # Initialize
            a_original = a
            n_original = n
            a = a % n
            result = 1

            self.jacobi_output.insert(tk.END, f"Procesăm ({a_original}/{n_original}):\n")

            while a != 0:
                # Remove factors of 2 from a
                t = 0
                while a % 2 == 0:
                    a = a // 2
                    t += 1

                if t > 0:
                    self.jacobi_output.insert(tk.END, f"Extragem factori de 2 din a: {t} factori\n")
                    # Apply the rule for factors of 2
                    if t % 2 == 1:
                        mod = n % 8
                        if mod == 3 or mod == 5:
                            result *= -1
                            self.jacobi_output.insert(tk.END, f"({2}/{n})^{t} = -1 (deoarece n ≡ {mod} mod 8)\n")
                        else:
                            self.jacobi_output.insert(tk.END, f"({2}/{n})^{t} = 1 (deoarece n ≡ {mod} mod 8)\n")

                # Now a is odd, apply reciprocity law
                if a > 1:
                    self.jacobi_output.insert(tk.END, f"Aplicăm legea reciprocității: ({a}/{n})\n")
                    if a % 4 == 3 and n % 4 == 3:
                        result *= -1
                        self.jacobi_output.insert(tk.END, f"Schimbăm semnul deoarece ambele numere ≡ 3 mod 4\n")

                    # Swap a and n
                    a, n = n % a, a
                    self.jacobi_output.insert(tk.END, f"Reducem: acum calculăm ({a}/{n})\n")
                else:
                    break

            if n == 1:
                self.jacobi_output.insert(tk.END, f"\nRezultat final: ({a_original}/{n_original}) = {result}\n")
                self.jacobi_result.set(f"({a_original}/{n_original}) = {result}")
            else:
                self.jacobi_output.insert(tk.END, f"\nRezultat neașteptat în calcul\n")
                self.jacobi_result.set("Eroare de calcul")

        except ValueError:
            self.jacobi_output.delete(1.0, tk.END)
            self.jacobi_output.insert(tk.END,
                                      "Eroare: Verificați valorile de intrare. Trebuie să fie numere întregi.\n")
            self.jacobi_result.set("Eroare de intrare")

    # Clear methods
    def clear_square_output(self):
        """Clear the square sums tab output and inputs."""
        self.square_output.delete(1.0, tk.END)
        self.p_var.set("")
        self.square_result.set("")

    def clear_legendre_output(self):
        """Clear the Legendre symbol tab output and inputs."""
        self.legendre_output.delete(1.0, tk.END)
        self.a_leg_var.set("")
        self.p_leg_var.set("")
        self.legendre_result.set("")

    def clear_jacobi_output(self):
        """Clear the Jacobi symbol tab output and inputs."""
        self.jacobi_output.delete(1.0, tk.END)
        self.a_jac_var.set("")
        self.n_jac_var.set("")
        self.jacobi_result.set("")

    # Example methods
    def load_square_example(self):
        """Load the example for square sums decomposition (p=461)."""
        self.p_var.set("461")
        self.decompose_into_squares()

    def load_legendre_example(self):
        """Load the example for Legendre symbol (a=14, p=17)."""
        self.a_leg_var.set("14")
        self.p_leg_var.set("17")
        self.calculate_legendre()

    def load_jacobi_example(self):
        """Load the example for Jacobi symbol (a=14, n=1275)."""
        self.a_jac_var.set("14")
        self.n_jac_var.set("1275")
        self.calculate_jacobi()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = MathAlgorithmsApp(root)
    root.mainloop()