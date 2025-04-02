import tkinter as tk
import math
from tkinter import scrolledtext, StringVar, Label, Entry, Button
import random


class PollardP1App:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmul Pollard p-1")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Input frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Number to factor
        Label(input_frame, text="n (număr de factorizat):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.n_var = StringVar()
        Entry(input_frame, textvariable=self.n_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Bound B
        Label(input_frame, text="B (margine):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
        self.b_var = StringVar()
        self.b_var.set("19")  # Default value
        Entry(input_frame, textvariable=self.b_var, width=20).grid(row=1, column=1, padx=10, pady=5)

        # Base a
        Label(input_frame, text="a (baza, între 2 și n-1):", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
        self.a_var = StringVar()
        self.a_var.set("3")  # Default value
        Entry(input_frame, textvariable=self.a_var, width=20).grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Run button
        Button(button_frame, text="Rulează Algoritmul", command=self.run_algorithm,
               bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Random A button
        Button(button_frame, text="A Aleator", command=self.generate_random_a,
               bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Clear button
        Button(button_frame, text="Șterge", command=self.clear_output,
               bg="#f44336", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Example button
        Button(button_frame, text="Exemplu", command=self.load_example,
               bg="#2196F3", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # Output text area
        output_frame = tk.Frame(root, bg="#f0f0f0")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Label for output
        Label(output_frame, text="Pași de calcul:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")

        # Scrolled text for output
        self.output_text = scrolledtext.ScrolledText(output_frame, width=80, height=20, font=("Courier", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Result label
        self.result_var = StringVar()
        self.result_var.set("")
        self.result_label = Label(root, textvariable=self.result_var, bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)

    def gcd(self, a, b):
        """Calculate the greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a

    def is_prime(self, num):
        """Check if a number is prime."""
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True

    def get_primes_up_to(self, limit):
        """Get all prime numbers up to the given limit."""
        primes = []
        for i in range(2, limit + 1):
            if self.is_prime(i):
                primes.append(i)
        return primes

    def factor_number(self, num):
        """Get the prime factorization of a number."""
        if num <= 1:
            return []

        factors = []
        i = 2
        while i * i <= num:
            while num % i == 0:
                factors.append(i)
                num //= i
            i += 1

        if num > 1:
            factors.append(num)

        return factors

    def pollard_p1(self, n, B, a):
        """
        Implement the improved Pollard's p-1 algorithm from the image.

        Args:
            n: Number to factor
            B: Bound
            a: Base (between 2 and n-1)

        Returns:
            Tuple containing (factor, steps_log)
        """
        steps_log = []

        # Step 1: Choose bound B (already provided as input)
        steps_log.append(f"1. Aleasă margine B = {B}")

        # Step 2: Choose random a, 2 <= a <= n-1 and compute d = gcd(a, n)
        steps_log.append(f"2. Ales a = {a}, calculez d = gcd(a, n)")
        d = self.gcd(a, n)
        steps_log.append(f"   d = gcd({a}, {n}) = {d}")

        if d >= 2:
            steps_log.append(f"   d = {d} >= 2, returnez d și mă opresc")
            return d, steps_log

        # Step 3: For each prime q <= B
        steps_log.append(f"3. Pentru fiecare număr prim q <= {B}, execut:")

        primes = self.get_primes_up_to(B)
        for q in primes:
            # Step 3.1: Calculate l = [ln n / ln q]
            l = int(math.log(n) / math.log(q))
            steps_log.append(f"   q = {q}, l = [ln({n})/ln({q})] = {l}")

            # Step 3.2: Calculate a = a^(q^l) mod n
            a_old = a
            a = pow(a, pow(q, l), n)
            steps_log.append(f"   a = {a_old}^({q}^{l}) mod {n} = {a}")

        # Step 4: Calculate d = gcd(a-1, n)
        steps_log.append(f"4. Calculez d = gcd(a-1, n)")
        d = self.gcd(a - 1, n)
        steps_log.append(f"   d = gcd({a}-1, {n}) = {d}")

        # Step 5: If d = 1 or d = n, return failure; otherwise, return d
        if d == 1 or d == n:
            steps_log.append(f"5. d = {d} {'= 1' if d == 1 else '= n'}, returnez mesaj de eșec")
            return 1, steps_log  # Failure
        else:
            steps_log.append(f"5. d = {d}, 1 < d < n, returnez d ca factor")

            # Check if d is prime
            if self.is_prime(d):
                steps_log.append(f"   {d} este un factor prim")
            else:
                factors = self.factor_number(d)
                factors_str = " × ".join(map(str, factors))
                steps_log.append(f"   {d} = {factors_str}")

            # Show the factorization
            other_factor = n // d
            steps_log.append(f"   Descompunerea: {n} = {d} × {other_factor}")

            if not self.is_prime(other_factor) and other_factor > 1:
                factors = self.factor_number(other_factor)
                factors_str = " × ".join(map(str, factors))
                steps_log.append(f"   {other_factor} = {factors_str}")

            return d, steps_log

    def generate_random_a(self):
        """Generate a random value for a between 2 and n-1."""
        try:
            n = int(self.n_var.get())
            if n > 3:
                a = random.randint(2, n - 1)
                self.a_var.set(str(a))
                self.output_text.insert(tk.END, f"Generat a aleator: {a}\n")
            else:
                self.output_text.insert(tk.END, "n trebuie să fie mai mare decât 3 pentru a genera un a aleator\n")
        except ValueError:
            self.output_text.insert(tk.END, "Introduceți un număr valid pentru n înainte de a genera a\n")

    def run_algorithm(self):
        """Run the algorithm with the input values and display results."""
        try:
            n = int(self.n_var.get())
            B = int(self.b_var.get())
            a = int(self.a_var.get())

            if a < 2 or a >= n:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"Eroare: a trebuie să fie între 2 și {n - 1}\n")
                return

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Rularea algoritmului Pollard p-1\n")
            self.output_text.insert(tk.END, f"n = {n}, B = {B}, a = {a}\n")
            self.output_text.insert(tk.END, "-" * 60 + "\n\n")

            # Run the algorithm
            factor, steps = self.pollard_p1(n, B, a)

            # Display steps
            for step in steps:
                self.output_text.insert(tk.END, step + "\n")

            # Display result
            if factor > 1 and factor < n:
                self.result_var.set(f"Factor găsit: {factor}")

                # Complete factorization
                other_factor = n // factor
                if other_factor > 1:
                    self.output_text.insert(tk.END, f"\nFactorizare completă: {n} = {factor} × {other_factor}\n")

                    # Check if the factorization is into primes
                    if self.is_prime(factor) and self.is_prime(other_factor):
                        self.output_text.insert(tk.END, "Aceasta este descompunerea în factori primi.\n")
                    else:
                        self.output_text.insert(tk.END, "Descompunerea mai poate fi continuată.\n")
            else:
                self.result_var.set("Nu s-a găsit un factor propriu")

        except ValueError:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Eroare: Verificați valorile de intrare. Trebuie să fie numere întregi.\n")
            self.result_var.set("Eroare de intrare")

    def clear_output(self):
        """Clear the output and inputs."""
        self.output_text.delete(1.0, tk.END)
        self.n_var.set("")
        self.b_var.set("19")
        self.a_var.set("3")
        self.result_var.set("")

    def load_example(self):
        """Load the example from the image."""
        self.n_var.set("19048567")
        self.b_var.set("19")
        self.a_var.set("3")
        self.run_algorithm()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PollardP1App(root)
    root.mainloop()