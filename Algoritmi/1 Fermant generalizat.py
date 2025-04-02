import math
import tkinter as tk
from tkinter import messagebox, scrolledtext


def fermat_factorization(n, k=1000, log_callback=None):
    """
    Implementarea algoritmului Fermat generalizat pentru factorizarea numerelor

    Args:
        n: numărul care trebuie factorizat (impar compus)
        k: factor de apropiere (limită pentru căutare)
        log_callback: funcție pentru a înregistra pașii algoritmului

    Returns:
        tuple: (a, b) unde n = a*b, sau None dacă nu găsește factori
    """

    # Funcție pentru a înregistra pașii
    def log(message):
        if log_callback:
            log_callback(message)

    # Verifică dacă n este par
    if n % 2 == 0:
        log(f"Numărul {n} este par. Factori: 2 și {n // 2}")
        return 2, n // 2

    # Pasul 1: Inițializare
    N = int(math.sqrt(k * n))
    i = 1
    t = 0

    log(f"PASUL 1: N ← ⌊√(k·n)⌋ = ⌊√({k}·{n})⌋ = {N}, i ← 1, t ← 0")

    # Pasul 2: Caută o valoare a lui y care este un număr întreg
    log(f"\nPASUL 2: Cât timp i ≤ N și t = 0, efectuează:")

    iterations_shown = 0
    max_iterations_to_show = 10  # Pentru a limita numărul de iterații afișate

    while i <= N and t == 0:
        y_squared = (N + i) ** 2 - k * n
        y = math.sqrt(y_squared) if y_squared >= 0 else float('nan')
        y_int = int(y)

        # Afișează doar primele câteva iterații pentru a nu încărca prea mult interfața
        if iterations_shown < max_iterations_to_show:
            log(f"  Iterația {i}:")
            log(f"    2.1. y ← √((N + i)² - k·n) = √(({N} + {i})² - {k}·{n}) = √{y_squared} = {y:.4f}")

            if y == y_int:
                log(f"    2.2. Dacă y = ⌊y⌋ = {y_int}, atunci x ← N + i = {N} + {i} = {N + i}, t ← 1")
            else:
                log(f"    2.2. y ≠ ⌊y⌋ ({y:.4f} ≠ {y_int}), continuă")

            log(f"    2.3. i ← i + 1 = {i} + 1 = {i + 1}")
            iterations_shown += 1
        elif iterations_shown == max_iterations_to_show:
            log(f"  ... (se afișează doar primele {max_iterations_to_show} iterații) ...")
            iterations_shown += 1

        # Verifică dacă y este un număr întreg
        if y == y_int:
            x = N + i
            t = 1

        i += 1

    # Pasul 3: Calculăm factorii dacă am găsit o soluție
    if t == 1:
        a = (x + y_int)
        b = n // a
        log(f"\nPASUL 3: Dacă t = 1, atunci returnează a = (x + y, n) = {a}, b = n/a = {n}/{a} = {b}")
        return int(a), int(b)
    else:
        log(f"\nPASUL 3: Nu s-a găsit nicio soluție în limitele date (t = {t})")

    # Pasul 4: Dacă nu găsim o soluție, verificăm dacă numărul este prim
    if is_prime(n):
        log(f"\nPASUL 4: Numărul {n} pare a fi prim.")
        return None

    # Dacă metoda Fermat eșuează, încearcă metoda clasică
    log("\nMetoda Fermat generalizată a eșuat. Încercăm metoda clasică de factorizare:")
    limit = int(math.sqrt(n)) + 1
    for i in range(3, min(limit, 1000), 2):  # Limităm și aici numărul de iterații
        if n % i == 0:
            log(f"  Am găsit factorul {i} prin metoda clasică. {n} = {i} × {n // i}")
            return i, n // i

    log(f"Nu s-au găsit factori pentru {n} în limitele specificate.")
    return None


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


# Interfața grafică
class FermatFactorizationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Algoritm de Factorizare Fermat")
        master.geometry("700x600")
        master.configure(bg="#e6f3ff")

        # Titlu
        self.title_label = tk.Label(master, text="Algoritm Fermat Generalizat",
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

        # Label și input pentru factorul k
        self.k_label = tk.Label(self.input_frame, text="Factor de apropiere (k):",
                                font=("Arial", 12), bg="#e6f3ff")
        self.k_label.grid(row=1, column=0, padx=5, pady=10)

        self.k_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=15)
        self.k_entry.grid(row=1, column=1, padx=5, pady=10)
        self.k_entry.insert(0, "1000")  # Valoare implicită

        # Buton de factorizare
        self.factor_button = tk.Button(master, text="Factorizează",
                                       font=("Arial", 12, "bold"),
                                       command=self.factorize,
                                       bg="#4a7abc", fg="white",
                                       padx=10, pady=5)
        self.factor_button.pack(pady=15)

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
        self.k_entry.delete(0, tk.END)
        self.k_entry.insert(0, "1000")
        self.log_text.delete(1.0, tk.END)
        self.result_label.config(text="Rezultatul va apărea aici")

    def factorize(self):
        try:
            self.log_text.delete(1.0, tk.END)  # Șterge logurile anterioare

            n = int(self.number_entry.get())

            if n <= 0:
                messagebox.showerror("Eroare", "Introduceți un număr pozitiv!")
                return

            try:
                k = int(self.k_entry.get())
                if k <= 0:
                    k = 1000  # Valoare implicită dacă k este invalid
            except:
                k = 1000

            # Formatăm titlul cu datele de input
            self.log(f"Aplicăm algoritmul Fermat generalizat pentru:\n")
            self.log(f"INPUT: n = {n} (număr de factorizat), k = {k} (factor de apropiere)")
            self.log(f"OUTPUT: doi factori a,b cu n = a·b\n")
            self.log("-" * 60)

            # Rulăm algoritmul cu callback pentru log
            factors = fermat_factorization(n, k, self.log)

            if factors:
                a, b = factors
                self.result_label.config(text=f"{n} = {a} × {b}")
                self.log(f"\nREZULTAT FINAL: {n} = {a} × {b}")
            else:
                if is_prime(n):
                    self.result_label.config(text=f"{n} este un număr prim!")
                    self.log(f"\nREZULTAT FINAL: {n} este un număr prim!")
                else:
                    self.result_label.config(text=f"Nu s-au găsit factori pentru {n}")
                    self.log(f"\nREZULTAT FINAL: Nu s-au găsit factori pentru {n} în limitele date")

        except ValueError:
            messagebox.showerror("Eroare", "Introduceți un număr valid!")


# Funcție pentru a rula aplicația
def run_app():
    root = tk.Tk()
    app = FermatFactorizationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()