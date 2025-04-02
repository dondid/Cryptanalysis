import math
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext


def gcd(a, b):
    """Calculează cel mai mare divizor comun folosind algoritmul lui Euclid"""
    while b:
        a, b = b, a % b
    return a


def pollard_rho(n, iterations=1000, log_callback=None):
    """
    Implementarea algoritmului Pollard-rho pentru factorizarea numerelor

    Args:
        n: numărul care trebuie factorizat (> 2, compus)
        iterations: numărul maxim de iterații
        log_callback: funcție pentru a înregistra pașii algoritmului

    Returns:
        int: un factor propriu al lui n sau None dacă nu găsește
    """

    # Funcție pentru a înregistra pașii
    def log(message):
        if log_callback:
            log_callback(message)

    # Verifică cazurile simple
    if n <= 1:
        return None

    if n % 2 == 0:
        return 2

    # Pasul 1: Inițializare
    a = 2
    b = 2
    log(f"PASUL 1: Pune a ← 2, b ← 2")

    # Definim funcția polinomială f(x) = x² + 1 mod n
    def f(x):
        return (x ** 2 + 1) % n

    # Pasul 2: Iterăm
    log(f"\nPASUL 2: Pentru i = 1, 2, ... execută:")

    for i in range(1, iterations + 1):
        # Pasul 2.1: Calculează noile valori pentru a și b
        a = f(a)
        b = f(f(b))  # b face doi pași pentru fiecare pas al lui a

        log(f"  Iterația {i}:")
        log(f"    2.1. Calculează a ← a² + 1 mod n = {a}² + 1 mod {n} = {f(a)}")
        log(f"        Calculează b ← b² + 1 mod n = {b}² + 1 mod {n} = {f(b)}")
        log(f"        Calculează b ← b² + 1 mod n = {f(b)}² + 1 mod {n} = {f(f(b))}")

        # Pasul 2.2: Calculează d = gcd(|a - b|, n)
        d = gcd(abs(a - b), n)
        log(f"    2.2. Calculează d = (a - b, n) = gcd(|{a} - {b}|, {n}) = gcd({abs(a - b)}, {n}) = {d}")

        # Pasul 2.3: Dacă 1 < d < n, returnează d
        if 1 < d < n:
            log(f"    2.3. Dacă 1 < d < n, atunci returnează d și se oprește.")
            log(f"        Avem 1 < {d} < {n}, deci am găsit un factor: {d}")
            return d

        # Pasul 2.4: Dacă d = n, eșec (trebuie aleasă altă funcție)
        if d == n:
            log(f"    2.4. Dacă d = n, atunci returnează mesaj de eșec.")
            log(f"        Avem d = {d} = {n}, deci algoritmul eșuează. Trebuie aleasă o altă funcție polinomială.")
            return None

    log("\nAlgoritmul nu a găsit un factor în numărul specificat de iterații.")
    return None


def factorize_with_pollard_rho(n, iterations=1000, log_callback=None):
    """
    Factorizează complet un număr folosind algoritmul Pollard-rho

    Args:
        n: numărul de factorizat
        iterations: numărul maxim de iterații per factor
        log_callback: funcție pentru logare

    Returns:
        list: lista factorilor primi ai lui n
    """

    def log(message):
        if log_callback:
            log_callback(message)

    if n <= 1:
        return []

    if is_prime(n):
        log(f"{n} este prim.")
        return [n]

    factors = []
    queue = [n]

    while queue:
        current = queue.pop(0)

        if is_prime(current):
            log(f"{current} este prim, îl adăugăm la lista factorilor.")
            factors.append(current)
            continue

        factor = pollard_rho(current, iterations, log_callback)

        if factor is None:
            # Încercăm o metodă alternativă
            log(f"Pollard-rho a eșuat pentru {current}. Încercăm factorizare prin încercare.")
            for i in range(2, int(math.sqrt(current)) + 1):
                if current % i == 0:
                    factor = i
                    log(f"Am găsit factorul {factor} prin încercare.")
                    break

            if factor is None:
                log(f"Nu am putut factoriza {current}. Îl considerăm prim.")
                factors.append(current)
                continue

        log(f"Am factorizat {current} = {factor} × {current // factor}")
        queue.append(factor)
        queue.append(current // factor)

    factors.sort()
    return factors


def is_prime(n):
    """Verifică dacă un număr este prim"""
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


def trace_pollard_example(n, x0=2, log_callback=None):
    """
    Recreează exemplul de urmărire din imagine pentru algoritmul Pollard-rho

    Args:
        n: numărul de factorizat (455459 în exemplu)
        x0: valoarea inițială (2 în exemplu)
        log_callback: funcție pentru logare
    """

    def log(message):
        if log_callback:
            log_callback(message)

    # Definim funcția f(x) = x² + 1 mod n
    def f(x):
        return (x ** 2 + 1) % n

    # Inițializăm valorile x și y
    x = x0
    y = x0

    log(f"Exemplu: Considerăm n = {n}, f(x) = x² + 1 și x₀ = y₀ = {x0}")
    log(f"Definim xₖ₊₁ = f(xₖ) și yₖ₊₁ = f(f(yₖ)) pentru k ≥ 0. Obținem:")

    # Afișăm valorile inițiale
    x_values = [x]
    y_values = [y]

    # Calculăm primele 9 iterații (ca în exemplu)
    for i in range(1, 10):
        # Calculăm următoarele valori
        x = f(x)
        y = f(f(y))

        x_values.append(x)
        y_values.append(y)

        # Calculăm diferența și GCD
        diff = abs(y - x)
        d = gcd(diff, n)

        log(f"x₍{i}₎ = {x}, \ty₍{i}₎ = {y} (mod {n}), \t(y₍{i}₎ - x₍{i}₎, n) = {d};")

    # Verificăm rezultatul final
    if d > 1 and d < n:
        factor1 = d
        factor2 = n // d
        log(f"\nDeci, {d} este un divizor netrivial al lui {n}. Obținem {n} = {factor1} × {factor2}.")
    else:
        log(f"\nÎn acest exemplu, algoritmul nu a găsit un divizor netrivial după 9 iterații.")


# Interfața grafică
class PollardRhoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Algoritm Pollard-rho")
        master.geometry("700x600")
        master.configure(bg="#e6f3ff")

        # Titlu
        self.title_label = tk.Label(master, text="Algoritm Pollard-rho",
                                    font=("Arial", 16, "bold"), bg="#e6f3ff")
        self.title_label.pack(pady=10)

        # Frame pentru input
        self.input_frame = tk.Frame(master, bg="#e6f3ff")
        self.input_frame.pack(pady=10)

        # Label și input pentru număr
        self.number_label = tk.Label(self.input_frame, text="Introduceți numărul:",
                                     font=("Arial", 12), bg="#e6f3ff")
        self.number_label.grid(row=0, column=0, padx=5, pady=10)

        self.number_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=15)
        self.number_entry.grid(row=0, column=1, padx=5, pady=10)

        # Label și input pentru iterații
        self.iterations_label = tk.Label(self.input_frame, text="Număr de iterații:",
                                         font=("Arial", 12), bg="#e6f3ff")
        self.iterations_label.grid(row=1, column=0, padx=5, pady=10)

        self.iterations_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=15)
        self.iterations_entry.grid(row=1, column=1, padx=5, pady=10)
        self.iterations_entry.insert(0, "1000")  # Valoare implicită

        # Frame pentru butoane
        self.button_frame = tk.Frame(master, bg="#e6f3ff")
        self.button_frame.pack(pady=5)

        # Buton pentru factorizare
        self.factor_button = tk.Button(self.button_frame, text="Factorizează",
                                       font=("Arial", 12, "bold"),
                                       command=self.factorize,
                                       bg="#4a7abc", fg="white",
                                       padx=10, pady=5)
        self.factor_button.grid(row=0, column=0, padx=10)

        # Buton pentru exemplu
        self.example_button = tk.Button(self.button_frame, text="Exemplu (455459)",
                                        font=("Arial", 12),
                                        command=self.run_example,
                                        bg="#5cb85c", fg="white",
                                        padx=10, pady=5)
        self.example_button.grid(row=0, column=1, padx=10)

        # Frame pentru rezultat
        self.result_frame = tk.Frame(master, bg="#e6f3ff")
        self.result_frame.pack(pady=10, fill=tk.X, padx=20)

        # Etichetă pentru rezultat
        self.result_label = tk.Label(self.result_frame,
                                     text="Rezultatul va apărea aici",
                                     font=("Arial", 12, "bold"),
                                     bg="#f0f7ff", width=40, height=2)
        self.result_label.pack(fill=tk.X)

        # Zonă de text cu scroll pentru a afișa pașii
        self.log_label = tk.Label(master, text="Pașii algoritmului:",
                                  font=("Arial", 12, "bold"), bg="#e6f3ff")
        self.log_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.log_text = scrolledtext.ScrolledText(master, width=80, height=15,
                                                  font=("Consolas", 10))
        self.log_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # Buton pentru a șterge conținutul
        self.clear_button = tk.Button(master, text="Șterge tot",
                                      font=("Arial", 10),
                                      command=self.clear_all,
                                      bg="#d9534f", fg="white")
        self.clear_button.pack(pady=10)

    def log(self, message):
        """Adaugă un mesaj în zona de log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Derulează automat în jos

    def clear_all(self):
        """Șterge conținutul din toate câmpurile"""
        self.number_entry.delete(0, tk.END)
        self.iterations_entry.delete(0, tk.END)
        self.iterations_entry.insert(0, "1000")
        self.log_text.delete(1.0, tk.END)
        self.result_label.config(text="Rezultatul va apărea aici")

    def factorize(self):
        try:
            self.log_text.delete(1.0, tk.END)  # Șterge logurile anterioare

            n = int(self.number_entry.get())

            if n <= 2:
                messagebox.showerror("Eroare", "Introduceți un număr > 2!")
                return

            try:
                iterations = int(self.iterations_entry.get())
                if iterations <= 0:
                    iterations = 1000  # Valoare implicită
            except:
                iterations = 1000

            # Formatăm titlul cu datele de input
            self.log(f"Aplicăm algoritmul Pollard-rho pentru:\n")
            self.log(f"INPUT: n = {n} (număr compus > 2, care nu este putere a unui număr prim)")
            self.log(f"OUTPUT: un divizor propriu al lui n\n")
            self.log("-" * 60)

            # Verificăm dacă numărul este prim
            if is_prime(n):
                self.log(f"{n} este un număr prim!")
                self.result_label.config(text=f"{n} este un număr prim!")
                return

            # Rulăm algoritmul
            factor = pollard_rho(n, iterations, self.log)

            if factor:
                other_factor = n // factor
                self.result_label.config(text=f"Factor găsit: {factor} (cu {n} = {factor} × {other_factor})")
                self.log(f"\nREZULTAT FINAL: Am găsit factorul {factor}, deci {n} = {factor} × {other_factor}")

                # Verificăm dacă factorii sunt primi
                if is_prime(factor):
                    self.log(f"{factor} este un număr prim.")
                else:
                    self.log(f"{factor} nu este prim, poate fi factorizat în continuare.")

                if is_prime(other_factor):
                    self.log(f"{other_factor} este un număr prim.")
                else:
                    self.log(f"{other_factor} nu este prim, poate fi factorizat în continuare.")
            else:
                self.result_label.config(text=f"Algoritmul nu a găsit un factor pentru {n}")
                self.log(f"\nREZULTAT FINAL: Algoritmul nu a găsit un factor pentru {n} în {iterations} iterații.")
                self.log("Încercați să creșteți numărul de iterații sau să folosiți alt algoritm.")

        except ValueError:
            messagebox.showerror("Eroare", "Introduceți un număr valid!")

    def run_example(self):
        """Rulează exemplul din imagine pentru n = 455459"""
        self.log_text.delete(1.0, tk.END)  # Șterge logurile anterioare
        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, "455459")

        self.log("EXEMPLU DIN IMAGINE\n")
        self.log("-" * 60)

        # Rulăm exemplul exact ca în imagine
        trace_pollard_example(455459, 2, self.log)

        # Afișăm rezultatul final
        self.result_label.config(text="Exemplu: 455459 = 743 × 613")


# Funcție pentru a rula aplicația
def run_app():
    root = tk.Tk()
    app = PollardRhoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()