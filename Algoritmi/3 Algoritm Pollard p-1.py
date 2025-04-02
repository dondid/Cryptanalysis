import tkinter as tk
import math
from tkinter import scrolledtext, StringVar, Label, Entry, Button


class PollardP1App:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmul Pollard p-1")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        # Input frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10)

        # Number to factor
        Label(input_frame, text="n (număr de factorizat):", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.n_var = StringVar()
        Entry(input_frame, textvariable=self.n_var, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Bound B
        Label(input_frame, text="B (limită):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
        self.b_var = StringVar()
        self.b_var.set("180")  # Default value
        Entry(input_frame, textvariable=self.b_var, width=20).grid(row=1, column=1, padx=10, pady=5)

        # Base g
        Label(input_frame, text="g (baza):", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
        self.g_var = StringVar()
        self.g_var.set("2")  # Default value
        Entry(input_frame, textvariable=self.g_var, width=20).grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Run button
        Button(button_frame, text="Rulează Algoritmul", command=self.run_algorithm,
               bg="#4CAF50", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

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

    def pollard_p1(self, n, B, g):
        """
        Implement Pollard's p-1 algorithm.

        Args:
            n: Number to factor
            B: Bound
            g: Base (usually 2)

        Returns:
            Tuple containing (factor, steps_log)
        """
        if n % 2 == 0:
            return 2, ["1. n este par, deci 2 este un factor."]

        steps_log = []

        # Step 1: a ← g
        a = g
        steps_log.append(f"1. a ← {g}")

        # Step 2: for j = 2 to B do a ← a^j mod n
        steps_log.append(f"2. Pentru j = 2 până la {B}:")

        for j in range(2, B + 1):
            a_old = a
            a = pow(a, j, n)
            steps_log.append(f"   j = {j}: a ← {a_old}^{j} mod {n} = {a}")

        # Step 3: d ← gcd(a-1, n)
        d = self.gcd(a - 1, n)
        steps_log.append(f"3. d ← gcd(a-1, n) = gcd({a}-1, {n}) = {d}")

        # Step 4: Check if d is a factor
        if d > 1 and d < n:
            steps_log.append(f"4. d = {d} > 1, deci {d} este factor al lui {n}")

            # Check if d is prime
            is_prime = all(d % i != 0 for i in range(2, int(math.sqrt(d)) + 1))
            if is_prime:
                steps_log.append(f"   {d} este un factor prim")
            else:
                steps_log.append(f"   {d} nu este prim")

            # Show the factorization
            if n % d == 0:
                other_factor = n // d
                steps_log.append(f"   Descompunerea finală: {n} = {d} × {other_factor}")
        else:
            steps_log.append(f"4. d = {d}, nu s-a găsit un divizor al lui {n}")

        return d, steps_log

    def run_algorithm(self):
        """Run the algorithm with the input values and display results."""
        try:
            n = int(self.n_var.get())
            B = int(self.b_var.get())
            g = int(self.g_var.get())

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Rularea algoritmului Pollard p-1\n")
            self.output_text.insert(tk.END, f"n = {n}, B = {B}, g = {g}\n")
            self.output_text.insert(tk.END, "-" * 60 + "\n\n")

            # Run the algorithm
            factor, steps = self.pollard_p1(n, B, g)

            # Display steps
            for step in steps:
                self.output_text.insert(tk.END, step + "\n")

            # Display result
            if factor > 1 and factor < n:
                self.result_var.set(f"Factor găsit: {factor}")
                if n % factor == 0:
                    other_factor = n // factor
                    self.output_text.insert(tk.END, f"\nFactorizare completă: {n} = {factor} × {other_factor}\n")
            else:
                self.result_var.set("Nu s-a găsit un factor")

        except ValueError:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Eroare: Verificați valorile de intrare. Trebuie să fie numere întregi.\n")
            self.result_var.set("Eroare de intrare")

    def clear_output(self):
        """Clear the output and inputs."""
        self.output_text.delete(1.0, tk.END)
        self.n_var.set("")
        self.b_var.set("180")
        self.g_var.set("2")
        self.result_var.set("")

    def load_example(self):
        """Load the example from the image."""
        self.n_var.set("15770708441")
        self.b_var.set("180")
        self.g_var.set("2")
        self.run_algorithm()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PollardP1App(root)
    root.mainloop()