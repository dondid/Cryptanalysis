import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import sympy


class ShamirSpecificExampleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmul lui Shamir - Exemplu Specific")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f5fa")

        # Main Frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Tabs
        tab_control = ttk.Notebook(main_frame)

        # Tab for Part 1
        self.tab1 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text="1. Partajarea Secretului")

        # Tab for Part 2
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab2, text="2. Reconstituirea Secretului")

        tab_control.pack(fill="both", expand=True)

        # Setup tabs
        self.setup_tab1()
        self.setup_tab2()

        # Initialize with example values
        self.initialize_example()

    def setup_tab1(self):
        # Parameters Frame for Part 1
        param_frame = ttk.LabelFrame(self.tab1, text="Parametrii Exemplului", padding="10")
        param_frame.pack(fill="x", pady=10)

        ttk.Label(param_frame, text="Sistemul confidențial (t,n):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.system_entry = ttk.Entry(param_frame, width=10)
        self.system_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.system_entry.insert(0, "(3,5)")

        ttk.Label(param_frame, text="Secretul S:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.secret_entry = ttk.Entry(param_frame, width=10)
        self.secret_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.secret_entry.insert(0, "4")

        ttk.Label(param_frame, text="Cheia K:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.key_entry = ttk.Entry(param_frame, width=10)
        self.key_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.key_entry.insert(0, "17")

        ttk.Label(param_frame, text="Modulul p:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.prime_entry = ttk.Entry(param_frame, width=10)
        self.prime_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.prime_entry.insert(0, "23")

        ttk.Label(param_frame, text="Coeficienți a₁, a₂:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.coefs_entry = ttk.Entry(param_frame, width=10)
        self.coefs_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.coefs_entry.insert(0, "10,2")

        # Generate button
        self.generate_btn = ttk.Button(param_frame, text="Generează Distribuția", command=self.generate_distribution)
        self.generate_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Results Frame
        results_frame = ttk.LabelFrame(self.tab1, text="Rezultate", padding="10")
        results_frame.pack(fill="both", expand=True, pady=10)

        # Public values
        ttk.Label(results_frame, text="Valori publice x_i:").pack(anchor="w", pady=(5, 0))
        self.public_values = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.public_values.pack(fill="x", pady=5)

        # Polynomial formula
        ttk.Label(results_frame, text="Formula polinomului:").pack(anchor="w", pady=(5, 0))
        self.polynomial_formula = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.polynomial_formula.pack(fill="x", pady=5)

        # Shared values calculation
        ttk.Label(results_frame, text="Calculul valorilor distribuite y_i = f(x_i):").pack(anchor="w", pady=(5, 0))
        self.shares_calculation = scrolledtext.ScrolledText(results_frame, width=80, height=10)
        self.shares_calculation.pack(fill="x", pady=5)

        # Shared values summary
        ttk.Label(results_frame, text="Valorile distribuite (rezumat):").pack(anchor="w", pady=(5, 0))
        self.shared_values = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.shared_values.pack(fill="x", pady=5)

    def setup_tab2(self):
        # Parameters Frame for Part 2
        param_frame = ttk.LabelFrame(self.tab2, text="Parametrii Exemplului", padding="10")
        param_frame.pack(fill="x", pady=10)

        ttk.Label(param_frame, text="Sistemul confidențial (t,n):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.system_entry2 = ttk.Entry(param_frame, width=10)
        self.system_entry2.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.system_entry2.insert(0, "(3,5)")

        ttk.Label(param_frame, text="Cheia K:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.key_entry2 = ttk.Entry(param_frame, width=10)
        self.key_entry2.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.key_entry2.insert(0, "17")

        ttk.Label(param_frame, text="Modulul p:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.prime_entry2 = ttk.Entry(param_frame, width=10)
        self.prime_entry2.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.prime_entry2.insert(0, "23")

        ttk.Label(param_frame, text="Valorile publice:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.public_values2 = ttk.Entry(param_frame, width=30)
        self.public_values2.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.public_values2.insert(0, "1,4,5")

        ttk.Label(param_frame, text="Valorile partajate:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.shared_values2 = ttk.Entry(param_frame, width=30)
        self.shared_values2.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.shared_values2.insert(0, "12,4,15")

        # Reconstruct button
        self.reconstruct_btn = ttk.Button(param_frame, text="Reconstruiește Secretul", command=self.reconstruct_secret)
        self.reconstruct_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Results Frame
        results_frame = ttk.LabelFrame(self.tab2, text="Reconstrucția Secretului", padding="10")
        results_frame.pack(fill="both", expand=True, pady=10)

        # Lagrange interpolation calculation
        ttk.Label(results_frame, text="Calculul interpolării Lagrange:").pack(anchor="w", pady=(5, 0))
        self.lagrange_calculation = scrolledtext.ScrolledText(results_frame, width=80, height=15)
        self.lagrange_calculation.pack(fill="both", expand=True, pady=5)

        # Secret result
        ttk.Label(results_frame, text="Secretul reconstruit:").pack(anchor="w", pady=(5, 0))
        self.secret_result = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.secret_result.pack(fill="x", pady=5)

    def initialize_example(self):
        # Call both generation and reconstruction to show example
        self.generate_distribution()
        self.reconstruct_secret()

    def generate_distribution(self):
        try:
            # Parse input values
            t, n = map(int, self.system_entry.get().strip("()").split(","))
            secret = int(self.secret_entry.get())
            key = int(self.key_entry.get())
            p = int(self.prime_entry.get())
            a1, a2 = map(int, self.coefs_entry.get().split(","))

            # Check if p is prime
            if not sympy.isprime(p):
                raise ValueError(f"Eroare: {p} nu este un număr prim.")

            # Generate public x values (x_i = i)
            x_values = list(range(1, n + 1))

            # Initialize the polynomial coefficients
            coefficients = [secret, a1, a2]  # f(X) = secret + a1*X + a2*X^2

            # Calculate shares
            y_values = []
            calculations = []

            for i, x in enumerate(x_values):
                y = self.evaluate_polynomial(coefficients, x, p)
                y_values.append(y)

                # Create detailed calculation
                calc = f"f({x}) = {secret} + {a1}·{x} + {a2}·{x}² (mod {p})\n"
                calc += f"     = {secret} + {a1 * x} + {a2 * x * x} (mod {p})\n"
                calc += f"     = {(secret + a1 * x + a2 * x * x)} (mod {p})\n"
                calc += f"     = {y}\n"
                calculations.append(calc)

            # Update UI
            self.public_values.delete(1.0, tk.END)
            x_str = ", ".join([f"x_{i + 1} = {x}" for i, x in enumerate(x_values)])
            self.public_values.insert(tk.END, x_str)

            # Display polynomial formula
            self.polynomial_formula.delete(1.0, tk.END)
            formula = f"f(X) = {secret} + {a1}X + {a2}X² (mod {p})"
            self.polynomial_formula.insert(tk.END, formula)

            # Display share calculations
            self.shares_calculation.delete(1.0, tk.END)
            self.shares_calculation.insert(tk.END, "\n".join(calculations))

            # Display shared values
            self.shared_values.delete(1.0, tk.END)
            y_str = ", ".join([f"f({x}) = {y}" for x, y in zip(x_values, y_values)])
            self.shared_values.insert(tk.END, y_str)

        except Exception as e:
            self.show_error(str(e))

    def evaluate_polynomial(self, coefficients, x, p):
        result = 0
        for i, coef in enumerate(coefficients):
            result = (result + coef * pow(x, i, p)) % p
        return result

    def reconstruct_secret(self):
        try:
            # Parse input values
            t, n = map(int, self.system_entry2.get().strip("()").split(","))
            key = int(self.key_entry2.get())
            p = int(self.prime_entry2.get())

            # Parse x and y values
            x_values = list(map(int, self.public_values2.get().split(",")))
            y_values = list(map(int, self.shared_values2.get().split(",")))

            # Check if we have enough shares
            if len(x_values) < t:
                raise ValueError(f"Eroare: Avem doar {len(x_values)} valori, dar avem nevoie de cel puțin {t}.")

            # Check if x and y arrays have same length
            if len(x_values) != len(y_values):
                raise ValueError("Eroare: Numărul de valori x și y trebuie să fie același.")

            # Perform Lagrange interpolation to reconstruct the secret
            lagrange_calc = "Calculul factorilor Lagrange pentru f(0):\n\n"
            secret = 0

            for i in range(len(x_values)):
                # Calculate the Lagrange basis polynomial L_i(0)
                num = 1
                den = 1
                term_calc = f"L_{i + 1}(0) = "
                parts = []

                for j in range(len(x_values)):
                    if i != j:
                        term_calc += f"(0-{x_values[j]})·"
                        parts.append(f"(0-{x_values[j]})")
                        num = (num * (0 - x_values[j])) % p

                term_calc = term_calc[:-1] + " / "  # Remove last dot

                for j in range(len(x_values)):
                    if i != j:
                        term_calc += f"({x_values[i]}-{x_values[j]})·"
                        parts.append(f"({x_values[i]}-{x_values[j]})")
                        den = (den * (x_values[i] - x_values[j])) % p

                term_calc = term_calc[:-1] + "\n"  # Remove last dot

                # Calculate modular multiplicative inverse
                den_inv = pow(den, p - 2, p)  # Fermat's little theorem for modular inverse

                # Calculate the term and add to result
                term = (y_values[i] * num * den_inv) % p
                secret = (secret + term) % p

                # Add step-by-step calculation
                term_calc += f"  = ({' · '.join(parts[:len(x_values) - 1])}) / ({' · '.join(parts[len(x_values) - 1:])})\n"
                term_calc += f"  = {num} / {den} (mod {p})\n"
                term_calc += f"  = {num} · {den}^(-1) (mod {p})\n"
                term_calc += f"  = {num} · {den_inv} (mod {p})\n"
                term_calc += f"  = {(num * den_inv) % p}\n\n"

                lagrange_calc += term_calc

            # Add final calculation
            lagrange_calc += "Calculul secretului S = f(0):\n"
            terms = []
            for i in range(len(x_values)):
                li_val = (pow((0 - x_values[(i + 1) % len(x_values)]) * (0 - x_values[(i + 2) % len(x_values)]), 1, p) *
                          pow((x_values[i] - x_values[(i + 1) % len(x_values)]) * (
                                      x_values[i] - x_values[(i + 2) % len(x_values)]), p - 2, p)) % p
                terms.append(f"{y_values[i]} · L_{i + 1}(0)")

            lagrange_calc += f"f(0) = {' + '.join(terms)} (mod {p})\n"
            lagrange_calc += f"     = {secret}\n"

            # Display Lagrange calculation
            self.lagrange_calculation.delete(1.0, tk.END)
            self.lagrange_calculation.insert(tk.END, lagrange_calc)

            # Display secret
            self.secret_result.delete(1.0, tk.END)
            self.secret_result.insert(tk.END, f"Secretul S = f(0) = {secret}")

        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Eroare")
        error_window.geometry("400x100")

        ttk.Label(error_window, text=message, wraplength=380).pack(padx=20, pady=20)
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ShamirSpecificExampleApp(root)
    root.mainloop()