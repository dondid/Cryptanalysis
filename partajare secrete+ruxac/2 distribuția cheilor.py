import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import random
import sympy


class ShamirSecretSharingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shamir Secret Sharing")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f5fa")

        # Main Frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Parameters Frame
        param_frame = ttk.LabelFrame(main_frame, text="Parametri", padding="10")
        param_frame.pack(fill="x", pady=10)

        # Prime p
        ttk.Label(param_frame, text="Numărul prim p:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.prime_entry = ttk.Entry(param_frame, width=10)
        self.prime_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.prime_entry.insert(0, "23")

        # Number of participants
        ttk.Label(param_frame, text="Numărul de participanți n:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.n_entry = ttk.Entry(param_frame, width=10)
        self.n_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.n_entry.insert(0, "5")

        # Threshold k
        ttk.Label(param_frame, text="Pragul k:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.k_entry = ttk.Entry(param_frame, width=10)
        self.k_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.k_entry.insert(0, "3")

        # Secret key K
        ttk.Label(param_frame, text="Cheia secretă K:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.key_entry = ttk.Entry(param_frame, width=10)
        self.key_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.key_entry.insert(0, "19")

        # Generate button
        self.generate_btn = ttk.Button(param_frame, text="Generează distribuția", command=self.generate_distribution)
        self.generate_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Rezultate", padding="10")
        results_frame.pack(fill="both", expand=True, pady=10)

        # Public values
        ttk.Label(results_frame, text="Valori publice x_i:").pack(anchor="w", pady=(5, 0))
        self.public_values = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.public_values.pack(fill="x", pady=5)

        # Polynomial coefficients
        ttk.Label(results_frame, text="Coeficienții polinomului:").pack(anchor="w", pady=(5, 0))
        self.polynomial_coeffs = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.polynomial_coeffs.pack(fill="x", pady=5)

        # Polynomial formula
        ttk.Label(results_frame, text="Formula polinomului:").pack(anchor="w", pady=(5, 0))
        self.polynomial_formula = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.polynomial_formula.pack(fill="x", pady=5)

        # Shared values
        ttk.Label(results_frame, text="Valorile distribuite y_i = f(x_i):").pack(anchor="w", pady=(5, 0))
        self.shared_values = scrolledtext.ScrolledText(results_frame, width=80, height=2)
        self.shared_values.pack(fill="x", pady=5)

        # Reconstruction Frame
        reconstruction_frame = ttk.LabelFrame(main_frame, text="Reconstrucția secretului", padding="10")
        reconstruction_frame.pack(fill="both", expand=True, pady=10)

        # Subset selection
        ttk.Label(reconstruction_frame,
                  text="Selectați participanții pentru reconstrucție (introduceți indici separați prin virgulă):").pack(
            anchor="w", pady=(5, 0))
        self.subset_entry = ttk.Entry(reconstruction_frame, width=50)
        self.subset_entry.pack(fill="x", pady=5)

        # Reconstruct button
        self.reconstruct_btn = ttk.Button(reconstruction_frame, text="Reconstruiește secretul",
                                          command=self.reconstruct_secret)
        self.reconstruct_btn.pack(pady=10)

        # Reconstruction result
        ttk.Label(reconstruction_frame, text="Rezultatul reconstrucției:").pack(anchor="w", pady=(5, 0))
        self.reconstruction_result = scrolledtext.ScrolledText(reconstruction_frame, width=80, height=4)
        self.reconstruction_result.pack(fill="both", expand=True, pady=5)


        # Explanation section
        explanation_frame = ttk.LabelFrame(main_frame, text="Explicație matematică", padding="10")
        explanation_frame.pack(fill="both", expand=True, pady=10)

        self.explanation_text = scrolledtext.ScrolledText(explanation_frame, width=80, height=10)
        self.explanation_text.pack(fill="both", expand=True)
        self.set_explanation()

        # Internal variables
        self.p = 23
        self.n = 5
        self.k = 3
        self.secret_key = 19
        self.x_values = []
        self.y_values = []
        self.coefficients = []

    def set_explanation(self):
        explanation = """Protocolul Shamir pentru distribuția secretului:

1. Inițializare:
   - D alege n elemente distincte x₁, ..., xₙ ∈ Zₚ (valori publice)
   - Fiecare participant Pᵢ cunoaște valoarea xᵢ

2. Distribuția cheii:
   - D dorește să distribuie cheia secretă K ∈ Zₚ
   - D selectează aleator k-1 elemente a₁, ..., aₖ₋₁ ∈ Zₚ
   - Se construiește polinomul: f(X) = K + Σ(j=1 to k-1) aⱼXʲ (mod p)

3. Distribuirea:
   - Pentru fiecare participant Pᵢ (1 ≤ i ≤ n), D calculează yᵢ = f(xᵢ)
   - D comunică yᵢ către participantul Pᵢ

4. Reconstruirea secretului:
   - Orice subset de k sau mai mulți participanți pot reconstrui secretul K
   - Reconstrucția folosește interpolarea Lagrange pentru a găsi f(0) = K
   - Un subset mai mic de k participanți nu poate determina secretul K

Această schemă asigură că secretul poate fi recuperat doar când un număr suficient de participanți colaborează.
"""
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, explanation)

    def generate_distribution(self):
        try:
            self.p = int(self.prime_entry.get())
            self.n = int(self.n_entry.get())
            self.k = int(self.k_entry.get())
            self.secret_key = int(self.key_entry.get()) % self.p

            # Check if p is prime
            if not sympy.isprime(self.p):
                raise ValueError(f"Eroare: {self.p} nu este un număr prim.")

            # Check if k and n are valid
            if self.k <= 1 or self.k > self.n:
                raise ValueError(f"Eroare: Pragul k trebuie să fie între 2 și n={self.n}.")

            # Generate random distinct x values
            self.x_values = []
            while len(self.x_values) < self.n:
                x = random.randint(1, self.p - 1)
                if x not in self.x_values:
                    self.x_values.append(x)

            # Generate random coefficients
            self.coefficients = [self.secret_key]  # a_0 = K
            for i in range(1, self.k):
                self.coefficients.append(random.randint(1, self.p - 1))

            # Calculate polynomial values
            self.y_values = []
            for x in self.x_values:
                y = self.evaluate_polynomial(x)
                self.y_values.append(y)

            # Update UI
            self.update_distribution_display()

        except ValueError as e:
            self.show_error(str(e))

    def evaluate_polynomial(self, x):
        result = 0
        for i, coef in enumerate(self.coefficients):
            result = (result + coef * pow(x, i, self.p)) % self.p
        return result

    def update_distribution_display(self):
        # Display public values
        self.public_values.delete(1.0, tk.END)
        x_str = ", ".join([f"x_{i + 1} = {x}" for i, x in enumerate(self.x_values)])
        self.public_values.insert(tk.END, x_str)

        # Display polynomial coefficients
        self.polynomial_coeffs.delete(1.0, tk.END)
        coef_str = ", ".join([f"a_{i} = {coef}" for i, coef in enumerate(self.coefficients)])
        self.polynomial_coeffs.insert(tk.END, coef_str)

        # Display polynomial formula
        self.polynomial_formula.delete(1.0, tk.END)
        terms = [f"{self.coefficients[0]}"]
        for i in range(1, len(self.coefficients)):
            terms.append(f"{self.coefficients[i]}X^{i}")
        formula = f"f(X) = {' + '.join(terms)} (mod {self.p})"
        self.polynomial_formula.insert(tk.END, formula)

        # Display shared values
        self.shared_values.delete(1.0, tk.END)
        y_str = ", ".join([f"y_{i + 1} = f({x}) = {y}" for i, (x, y) in enumerate(zip(self.x_values, self.y_values))])
        self.shared_values.insert(tk.END, y_str)

    def reconstruct_secret(self):
        try:
            # Get subset of participants
            subset_str = self.subset_entry.get().strip()
            if not subset_str:
                raise ValueError("Introduceți indici separați prin virgulă")

            indices = [int(idx.strip()) - 1 for idx in subset_str.split(",")]
            if any(idx < 0 or idx >= self.n for idx in indices):
                raise ValueError(f"Indicii trebuie să fie între 1 și {self.n}")

            # Check if we have enough participants
            if len(indices) < self.k:
                self.reconstruction_result.delete(1.0, tk.END)
                self.reconstruction_result.insert(tk.END,
                                                  f"Avertisment: Aveți doar {len(indices)} participanți, dar pragul este k={self.k}.\n")
                self.reconstruction_result.insert(tk.END, "Reconstrucția secretului ar putea să nu fie corectă!")

            # Get subset of x and y values
            x_subset = [self.x_values[i] for i in indices]
            y_subset = [self.y_values[i] for i in indices]

            # Reconstruct secret using Lagrange interpolation
            reconstructed_secret = self.lagrange_interpolation(x_subset, y_subset, 0)

            # Display reconstruction
            self.reconstruction_result.delete(1.0, tk.END)

            # Show calculation steps
            self.reconstruction_result.insert(tk.END,
                                              f"Subset de {len(indices)} participanți: {', '.join([f'P_{i + 1}' for i in indices])}\n")
            self.reconstruction_result.insert(tk.END, f"Valori x: {x_subset}\n")
            self.reconstruction_result.insert(tk.END, f"Valori y: {y_subset}\n")

            # Show result and verification
            actual_secret = self.coefficients[0]
            self.reconstruction_result.insert(tk.END, f"\nSecret reconstruit: f(0) = {reconstructed_secret}\n")
            self.reconstruction_result.insert(tk.END, f"Secret original: K = {actual_secret}\n")

            if reconstructed_secret == actual_secret:
                self.reconstruction_result.insert(tk.END, "\nReconstrucția a reușit! Secretul a fost recuperat corect.")
            else:
                self.reconstruction_result.insert(tk.END,
                                                  "\nEroare în reconstrucție! Secretul nu a fost recuperat corect.")

        except ValueError as e:
            self.show_error(str(e))

    def lagrange_interpolation(self, x_values, y_values, x):
        # Lagrange interpolation formula
        result = 0
        for i, (xi, yi) in enumerate(zip(x_values, y_values)):
            # Calculate the Lagrange basis polynomial
            numerator = 1
            denominator = 1
            for j, xj in enumerate(x_values):
                if i != j:
                    numerator = (numerator * (x - xj)) % self.p
                    denominator = (denominator * (xi - xj)) % self.p

            # Calculate the modular multiplicative inverse
            inverse_denominator = pow(denominator, self.p - 2, self.p)

            # Calculate the term and add to result
            term = (yi * numerator * inverse_denominator) % self.p
            result = (result + term) % self.p

        return result

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Eroare")
        error_window.geometry("400x100")

        ttk.Label(error_window, text=message, wraplength=380).pack(padx=20, pady=20)
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ShamirSecretSharingApp(root)
    root.mainloop()