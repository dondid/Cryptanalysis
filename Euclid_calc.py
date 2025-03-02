import tkinter as tk
from tkinter import ttk, scrolledtext
from math import isqrt
import threading


class AplicatieMatematica:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicație Matematică")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Stilizare
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", font=("Arial", 10), background="#4CAF50")
        style.configure("TLabel", font=("Arial", 10), background="#f0f0f0")
        style.configure("Header.TLabel", font=("Arial", 12, "bold"), background="#f0f0f0")

        # Creare frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Creare frame pentru selectare program
        self.program_frame = ttk.Frame(self.main_frame)
        self.program_frame.pack(fill=tk.X, pady=5)

        # Etichetă pentru program
        ttk.Label(self.program_frame, text="Selectați programul:", style="Header.TLabel").pack(side=tk.LEFT, padx=5)

        # Combobox pentru selecție program
        self.program_var = tk.StringVar()
        self.program_combo = ttk.Combobox(self.program_frame, textvariable=self.program_var, width=40)
        self.program_combo['values'] = (
            "1. Verificare număr prim",
            "2. Algoritmul lui Euclid",
            "3. Algoritmul lui Euclid extins",
            "4. Rezolvarea ecuației liniare diofantice",
            "5. Analiza factorilor și divizorilor"
        )
        self.program_combo.current(4)  # Setăm implicit la program 5
        self.program_combo.pack(side=tk.LEFT, padx=5)
        self.program_combo.bind("<<ComboboxSelected>>", self.on_program_change)

        # Creare frame pentru input
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=10)

        # Frame pentru rezultate
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Zona de rezultate
        ttk.Label(self.result_frame, text="Rezultate:", style="Header.TLabel").pack(anchor=tk.W, padx=5)

        self.result_text = scrolledtext.ScrolledText(self.result_frame, wrap=tk.WORD, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.config(state=tk.DISABLED)

        # Statusbar
        self.status_var = tk.StringVar()
        self.status_var.set("Gata")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Inițializare interfață pentru programul 5 (implicit)
        self.on_program_change(None)

    def on_program_change(self, event):
        # Curățăm frame-ul de input
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        program = self.program_combo.current() + 1

        if program == 1:  # Verificare număr prim
            ttk.Label(self.input_frame, text="Introduceți numărul:").grid(row=0, column=0, padx=5, pady=5)
            self.number_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.number_var).grid(row=0, column=1, padx=5, pady=5)
            ttk.Button(self.input_frame, text="Verifică", command=self.run_program).grid(row=0, column=2, padx=5,
                                                                                         pady=5)

        elif program == 2:  # Algoritmul lui Euclid
            ttk.Label(self.input_frame, text="a:").grid(row=0, column=0, padx=5, pady=5)
            self.a_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.a_var).grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(self.input_frame, text="b:").grid(row=1, column=0, padx=5, pady=5)
            self.b_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.b_var).grid(row=1, column=1, padx=5, pady=5)

            ttk.Button(self.input_frame, text="Calculează", command=self.run_program).grid(row=1, column=2, padx=5,
                                                                                           pady=5)

        elif program == 3:  # Algoritmul lui Euclid extins
            ttk.Label(self.input_frame, text="a:").grid(row=0, column=0, padx=5, pady=5)
            self.a_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.a_var).grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(self.input_frame, text="b:").grid(row=1, column=0, padx=5, pady=5)
            self.b_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.b_var).grid(row=1, column=1, padx=5, pady=5)

            ttk.Button(self.input_frame, text="Calculează", command=self.run_program).grid(row=1, column=2, padx=5,
                                                                                           pady=5)

        elif program == 4:  # Rezolvarea ecuației liniare diofantice
            ttk.Label(self.input_frame, text="a:").grid(row=0, column=0, padx=5, pady=5)
            self.a_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.a_var).grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(self.input_frame, text="b:").grid(row=1, column=0, padx=5, pady=5)
            self.b_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.b_var).grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(self.input_frame, text="c:").grid(row=2, column=0, padx=5, pady=5)
            self.c_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.c_var).grid(row=2, column=1, padx=5, pady=5)

            ttk.Button(self.input_frame, text="Calculează", command=self.run_program).grid(row=2, column=2, padx=5,
                                                                                           pady=5)

        elif program == 5:  # Analiza factorilor și divizorilor
            ttk.Label(self.input_frame, text="Introduceți un număr natural n > 1:").grid(row=0, column=0, padx=5,
                                                                                         pady=5)
            self.n_var = tk.StringVar()
            ttk.Entry(self.input_frame, textvariable=self.n_var).grid(row=0, column=1, padx=5, pady=5)
            ttk.Button(self.input_frame, text="Analizează", command=self.run_program).grid(row=0, column=2, padx=5,
                                                                                           pady=5)

    def run_program(self):
        # Rulează programul în thread separat pentru a nu bloca UI
        program = self.program_combo.current() + 1

        # Resetează zona de rezultate
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

        # Setează statusul
        self.status_var.set("Procesare...")

        # Creează thread pentru procesare
        thread = threading.Thread(target=self.execute_program, args=(program,))
        thread.daemon = True
        thread.start()

    def execute_program(self, program):
        try:
            if program == 1:  # Verificare număr prim
                numar = int(self.number_var.get())
                self.verify_prime(numar)

            elif program == 2:  # Algoritmul lui Euclid
                a = int(self.a_var.get())
                b = int(self.b_var.get())
                self.euclidean_algorithm(a, b)

            elif program == 3:  # Algoritmul lui Euclid extins
                a = int(self.a_var.get())
                b = int(self.b_var.get())
                self.extended_euclidean_algorithm(a, b)

            elif program == 4:  # Rezolvarea ecuației liniare diofantice
                a = int(self.a_var.get())
                b = int(self.b_var.get())
                c = int(self.c_var.get())
                self.solve_diophantine(a, b, c)

            elif program == 5:  # Analiza factorilor și divizorilor
                n = int(self.n_var.get())
                if n <= 1:
                    self.append_result("Vă rugăm să introduceți un număr natural n > 1.")
                    return
                self.analyze_factors_divisors(n)

            self.status_var.set("Gata")

        except ValueError as e:
            self.append_result(f"Eroare: Vă rugăm să introduceți numere valide.")
            self.status_var.set("Eroare")
        except Exception as e:
            self.append_result(f"Eroare: {str(e)}")
            self.status_var.set("Eroare")

    def append_result(self, text):
        # Adaugă text în zona de rezultate
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)

    # IMPLEMENTĂRI ALE FUNCȚIILOR MATEMATICE
    def factorial(self, n):
        fact = 1
        for i in range(1, n):
            fact *= i
        return fact

    def algoritm_euclidian_extins(self, a, b):
        if a == 0:
            return b, 0, 1

        w, x1, y1 = self.algoritm_euclidian_extins(b % a, a)

        x = y1 - int(b / a) * x1
        y = x1

        return w, x, y

    def factorizare_in_numere_prime(self, n):
        factori = {}
        # Împarte cu 2 de câte ori este posibil
        while n % 2 == 0:
            factori[2] = factori.get(2, 0) + 1
            n //= 2

        # Verifică pentru numere impare de la 3 până la sqrt(n)
        factor = 3
        while factor * factor <= n:
            while n % factor == 0:
                factori[factor] = factori.get(factor, 0) + 1
                n //= factor
            factor += 2

        if n > 1:
            factori[n] = 1

        return factori

    def numar_si_suma_divizorilor(self, n, factori=None):
        if factori is None:
            factori = self.factorizare_in_numere_prime(n)

        numar_div = 1
        suma_div = 1
        for p, exp in factori.items():
            numar_div *= (exp + 1)
            suma_div *= (p ** (exp + 1) - 1) // (p - 1)
        return numar_div, suma_div

    def functia_totient_euler(self, n, factori=None):
        if factori is None:
            factori = self.factorizare_in_numere_prime(n)
        phi = n
        for p in factori.keys():
            phi = phi * (p - 1) // p
        return phi

    def obtine_divizorii(self, n):
        divizori = set()
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                divizori.add(i)
                divizori.add(n // i)
        return sorted(divizori)

    def verifica_numar_interesant_deductibil(self, n):
        rezultate = []
        factori = self.factorizare_in_numere_prime(n)
        divizori = self.obtine_divizorii(n)

        # Verificare număr Harshad
        suma_cifre = sum(int(cifra) for cifra in str(n))
        if n % suma_cifre == 0:
            rezultate.append(f"{n} este un număr Harshad (divizibil cu suma cifrelor sale {suma_cifre}).")

        # Verificare dacă suma divizorilor proprii este un număr prim
        divizori_proprii = divizori[:-1]  # Excludem numărul n
        suma_divizori_proprii = sum(divizori_proprii)
        este_suma_prima = True
        if suma_divizori_proprii > 1:
            for i in range(2, isqrt(suma_divizori_proprii) + 1):
                if suma_divizori_proprii % i == 0:
                    este_suma_prima = False
                    break
            if este_suma_prima:
                rezultate.append(f"Suma divizorilor proprii ({suma_divizori_proprii}) este un număr prim.")

        # Verificare proprietăți prin factorizare
        num_factors = len(factori)
        if num_factors == 1 and list(factori.keys())[0] > 1:
            rezultate.append(f"{n} este un număr prim.")
        elif num_factors == 2:
            keys = list(factori.keys())
            if factori[keys[0]] == 1 and factori[keys[1]] == 1:
                rezultate.append(f"{n} = {keys[0]} × {keys[1]} este produsul a două numere prime distincte.")

        # Verificare numere perfecte
        numar_div, suma_div = self.numar_si_suma_divizorilor(n, factori)
        if suma_div == 2 * n:
            rezultate.append(f"{n} este un număr perfect.")

        # Verificare numere abundente/deficiente
        suma_divizori_proprii = suma_div - n
        if suma_divizori_proprii > n:
            rezultate.append(f"{n} este un număr abundant (suma divizorilor proprii > n).")
        elif suma_divizori_proprii < n:
            rezultate.append(f"{n} este un număr deficient (suma divizorilor proprii < n).")

        # Proprietăți deductibile
        phi = self.functia_totient_euler(n, factori)
        if n % phi == 0:
            rezultate.append(f"{n} este divizibil cu valoarea funcției φ(n) = {phi}.")

        return rezultate

    # IMPLEMENTĂRI ALE APLICAȚIILOR
    def verify_prime(self, numar):
        self.append_result(f"Verificare dacă {numar} este prim:")
        if numar <= 1:
            self.append_result("Numerele mai mici sau egale cu 1 nu sunt considerate prime.")
            return

        if numar == 2:
            self.append_result("2 este un număr prim.")
            return

        if numar % 2 == 0:
            self.append_result(f"{numar} nu este prim, deoarece este divizibil cu 2.")
            return

        for i in range(3, isqrt(numar) + 1, 2):
            if numar % i == 0:
                self.append_result(f"{numar} nu este prim, deoarece este divizibil cu {i}.")
                return

        self.append_result(f"{numar} este un număr prim.")

    def euclidean_algorithm(self, a, b):
        self.append_result(f"Calculul CMMDC({a}, {b}) folosind algoritmul lui Euclid:")

        if a == 0 or b == 0:
            result = max(abs(a), abs(b))
            self.append_result(f"CMMDC({a}, {b}) = {result}")
            return

        # Salvează valorile inițiale
        orig_a, orig_b = a, b

        # Pași intermediari
        steps = []
        r = a % b
        steps.append(f"{a} = {b} × {a // b} + {r}")

        while r != 0:
            a = b
            b = r
            r = a % b
            if r != 0:
                steps.append(f"{a} = {b} × {a // b} + {r}")
            else:
                steps.append(f"{a} = {b} × {a // b} + {r}")

        # Afișează pași
        self.append_result("Pași:")
        for step in steps:
            self.append_result(step)

        self.append_result(f"CMMDC({orig_a}, {orig_b}) = {b}")

    def extended_euclidean_algorithm(self, a, b):
        self.append_result(f"Calculul CMMDC({a}, {b}) și a coeficienților x, y folosind algoritmul lui Euclid extins:")

        g, x, y = self.algoritm_euclidian_extins(a, b)

        self.append_result(f"CMMDC({a}, {b}) = {g}")
        self.append_result(f"Coeficienții Bézout: x = {x}, y = {y}")
        self.append_result(f"Verificare: {a} × {x} + {b} × {y} = {a * x + b * y}")

    def solve_diophantine(self, a, b, c):
        self.append_result(f"Rezolvarea ecuației diofantice: {a}x + {b}y = {c}")

        d, x, y = self.algoritm_euclidian_extins(a, b)

        if c % d != 0:
            self.append_result(
                f"Ecuația nu are soluții întregi deoarece {c} nu este divizibil cu CMMDC({a}, {b}) = {d}")
            return

        # Calculăm soluția particulară
        x0 = x * (c // d)
        y0 = y * (c // d)

        self.append_result(f"CMMDC({a}, {b}) = {d}")
        self.append_result(f"O soluție particulară: x0 = {x0}, y0 = {y0}")

        # Formulă generală
        self.append_result(
            f"Formula generală a soluțiilor: x = {x0} + {b // d}·t, y = {y0} - {a // d}·t, unde t este un întreg arbitrar")

        # Verificare soluție
        self.append_result(f"Verificare: {a} × {x0} + {b} × {y0} = {a * x0 + b * y0}")

    def analyze_factors_divisors(self, n):
        # Factorizarea în numere prime
        factori = self.factorizare_in_numere_prime(n)
        self.append_result(f"Analiza numărului {n}:")

        self.append_result("\n1. Factorizarea în numere prime:")
        factorizare = " × ".join([f"{p}^{exp}" if exp > 1 else str(p) for p, exp in factori.items()])
        self.append_result(f"{n} = {factorizare}")

        # Calcularea numărului și sumei divizorilor
        numar_div, suma_div = self.numar_si_suma_divizorilor(n, factori)
        divizori = self.obtine_divizorii(n)

        self.append_result(f"\n2. Divizorii lui {n}:")
        self.append_result(f"Numărul de divizori: {numar_div}")
        self.append_result(f"Divizorii: {', '.join(map(str, divizori))}")
        self.append_result(f"Suma divizorilor: {suma_div}")

        # Verificare dacă n este un număr perfect
        self.append_result(f"\n3. Proprietăți ale numărului:")
        if suma_div - n == n:
            self.append_result(f"{n} este un număr perfect (suma divizorilor proprii = {n}).")
        elif suma_div - n > n:
            self.append_result(f"{n} este un număr abundant (suma divizorilor proprii = {suma_div - n} > {n}).")
        else:
            self.append_result(f"{n} este un număr deficient (suma divizorilor proprii = {suma_div - n} < {n}).")

        # Funcția totientă a lui Euler
        phi = self.functia_totient_euler(n, factori)
        self.append_result(f"\n4. Funcția totientă a lui Euler:")
        self.append_result(f"φ({n}) = {phi} (numărul de numere mai mici ca {n} și prime cu {n})")

        # Proprietăți interesante și deductibile
        self.append_result(f"\n5. Proprietăți interesante și deductibile:")
        proprietati = self.verifica_numar_interesant_deductibil(n)
        if proprietati:
            for prop in proprietati:
                self.append_result(f"- {prop}")
        else:
            self.append_result("Nu s-au identificat proprietăți speciale pentru acest număr.")


# Rulare aplicație
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicatieMatematica(root)
    root.mainloop()