import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy
import random
from math import gcd


class ElGamalSignature:
    def __init__(self):
        self.p = 0
        self.alpha = 0
        self.beta = 0
        self.a = 0
        self.k = 0
        self.steps_log = []

    def reset_log(self):
        self.steps_log = []

    def log_step(self, step_description):
        self.steps_log.append(step_description)

    def is_primitive_root(self, g, p):
        """Verifică dacă g este rădăcină primitivă modulo p"""
        if g <= 1 or g >= p:
            return False

        # Calculăm factorizarea lui p-1
        factors = []
        phi = p - 1

        # Găsim factorii primi ai lui p-1
        for i in range(2, int(phi ** 0.5) + 1):
            if phi % i == 0:
                factors.append(i)
                while phi % i == 0:
                    phi //= i

        if phi > 1:
            factors.append(phi)

        # Verificăm condițiile pentru rădăcină primitivă
        for factor in factors:
            if pow(g, (p - 1) // factor, p) == 1:
                return False

        return True

    def find_primitive_root(self, p):
        """Găsește o rădăcină primitivă modulo p"""
        if p == 2:
            return 1

        for g in range(2, p):
            if self.is_primitive_root(g, p):
                return g

        return None

    def extended_gcd(self, a, b):
        """Algoritmul extins Euclid pentru a găsi inversul modular"""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def mod_inverse(self, a, m):
        """Calculează inversul modular al lui a modulo m"""
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise Exception('Inversul modular nu există')
        else:
            return x % m

    def generate_keys(self, p, alpha, a):
        """Generează cheile pentru algoritmul ElGamal"""
        self.p = p
        self.alpha = alpha
        self.a = a

        # Verificăm dacă p este prim
        if not sympy.isprime(p):
            self.log_step(f"EROARE: {p} nu este un număr prim!")
            return False

        # Verificăm dacă alpha este rădăcină primitivă modulo p
        if not self.is_primitive_root(alpha, p):
            self.log_step(f"EROARE: {alpha} nu este rădăcină primitivă modulo {p}!")
            return False

        # Verificăm dacă a este valid
        if a <= 0 or a >= p - 1:
            self.log_step(f"EROARE: Cheia privată a={a} trebuie să fie între 1 și {p - 2}!")
            return False

        # Calculăm cheia publică beta = alpha^a mod p
        self.beta = pow(alpha, a, p)

        self.log_step(f"Parametrii generați:")
        self.log_step(f"  p = {p} (număr prim)")
        self.log_step(f"  alpha = {alpha} (rădăcină primitivă modulo p)")
        self.log_step(f"  a = {a} (cheia privată)")
        self.log_step(f"  beta = alpha^a mod p = {alpha}^{a} mod {p} = {self.beta}")

        return True

    def sign(self, x, k):
        """Semnează mesajul x folosind cheia privată k"""
        self.k = k

        # Verificăm dacă k este valid (gcd(k, p-1) = 1)
        if gcd(k, self.p - 1) != 1:
            self.log_step(f"EROARE: k={k} trebuie să fie relativ prim cu p-1={self.p - 1}!")
            return None, None

        # Calculăm γ = alpha^k mod p
        gamma = pow(self.alpha, k, self.p)

        # Calculăm inversul lui k mod (p-1)
        k_inv = self.mod_inverse(k, self.p - 1)

        # Calculăm δ = (x - a*γ)*k^(-1) mod (p-1)
        delta = ((x - self.a * gamma) * k_inv) % (self.p - 1)

        self.log_step(f"Semnare mesaj x = {x}:")
        self.log_step(f"  k = {k} (număr aleator)")
        self.log_step(f"  γ = alpha^k mod p = {self.alpha}^{k} mod {self.p} = {gamma}")
        self.log_step(f"  k^(-1) mod (p-1) = {k_inv}")
        self.log_step(f"  δ = (x - a*γ)*k^(-1) mod (p-1)")
        self.log_step(f"    = ({x} - {self.a}*{gamma})*{k_inv} mod {self.p - 1}")
        self.log_step(f"    = ({x} - {self.a * gamma})*{k_inv} mod {self.p - 1}")
        self.log_step(f"    = {x - self.a * gamma}*{k_inv} mod {self.p - 1}")
        self.log_step(f"    = {(x - self.a * gamma) * k_inv} mod {self.p - 1}")
        self.log_step(f"    = {delta}")

        self.log_step(f"Semnătura mesajului x = {x} este (γ,δ) = ({gamma},{delta})")

        return gamma, delta

    def verify(self, x, gamma, delta):
        """Verifică semnătura (gamma, delta) pentru mesajul x"""
        # Verificare γ ∈ Zp*
        if gamma <= 0 or gamma >= self.p:
            self.log_step(f"EROARE: γ={gamma} nu este element valid în Zp*!")
            return False

        # Verificare δ ∈ Zp-1*
        if delta <= 0 or delta >= self.p - 1:
            self.log_step(f"EROARE: δ={delta} nu este element valid în Zp-1*!")
            return False

        # Calculăm β^γ * γ^δ mod p
        left_side = (pow(self.beta, gamma, self.p) * pow(gamma, delta, self.p)) % self.p

        # Calculăm α^x mod p
        right_side = pow(self.alpha, x, self.p)

        self.log_step(f"Verificare semnătură (γ,δ) = ({gamma},{delta}) pentru mesajul x = {x}:")
        self.log_step(f"  Calculăm β^γ * γ^δ mod p:")
        self.log_step(f"    β^γ = {self.beta}^{gamma} mod {self.p} = {pow(self.beta, gamma, self.p)}")
        self.log_step(f"    γ^δ = {gamma}^{delta} mod {self.p} = {pow(gamma, delta, self.p)}")
        self.log_step(
            f"    β^γ * γ^δ mod p = {pow(self.beta, gamma, self.p)} * {pow(gamma, delta, self.p)} mod {self.p} = {left_side}")

        self.log_step(f"  Calculăm α^x mod p:")
        self.log_step(f"    α^x = {self.alpha}^{x} mod {self.p} = {right_side}")

        result = (left_side == right_side)

        if result:
            self.log_step(f"  Verificare REUȘITĂ: {left_side} = {right_side}")
        else:
            self.log_step(f"  Verificare EȘUATĂ: {left_side} ≠ {right_side}")

        return result

    def verify_equation(self, x, gamma, delta):
        """Verifică ecuația β^γ * γ^δ ≡ α^x (mod p)"""
        # Verificăm dacă β^γ * γ^δ ≡ α^x (mod p)
        left = (pow(self.beta, gamma, self.p) * pow(gamma, delta, self.p)) % self.p
        right = pow(self.alpha, x, self.p)

        self.log_step(f"Verificarea ecuației: β^γ * γ^δ ≡ α^x (mod p)")
        self.log_step(f"  Stânga: {self.beta}^{gamma} * {gamma}^{delta} mod {self.p} = {left}")
        self.log_step(f"  Dreapta: {self.alpha}^{x} mod {self.p} = {right}")

        if left == right:
            self.log_step(f"  ✓ Ecuație validă: {left} ≡ {right} (mod {self.p})")
            return True
        else:
            self.log_step(f"  ✗ Ecuație invalidă: {left} ≢ {right} (mod {self.p})")
            return False

    def is_valid_signature(self, x, gamma, delta):
        """Verifică dacă (gamma, delta) este o semnătură validă pentru mesajul x"""
        return self.verify_equation(x, gamma, delta)

    def get_steps_log(self):
        """Returnează jurnalul de pași"""
        return self.steps_log


class ElGamalSignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritm ElGamal pentru Semnături Digitale")
        self.root.geometry("1200x800")

        self.elgamal = ElGamalSignature()

        # Frame-uri principale
        self.left_frame = ttk.Frame(root, padding="10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = ttk.Frame(root, padding="10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame pentru generarea de chei
        self.key_frame = ttk.LabelFrame(self.left_frame, text="Generare Chei", padding="10")
        self.key_frame.pack(fill=tk.X, pady=10)

        ttk.Label(self.key_frame, text="p (număr prim):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.p_entry = ttk.Entry(self.key_frame, width=10)
        self.p_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.p_entry.insert(0, "467")

        ttk.Label(self.key_frame, text="α (rădăcină primitivă):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.alpha_entry = ttk.Entry(self.key_frame, width=10)
        self.alpha_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.alpha_entry.insert(0, "2")

        ttk.Label(self.key_frame, text="a (cheie privată):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.a_entry = ttk.Entry(self.key_frame, width=10)
        self.a_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.a_entry.insert(0, "127")

        self.generate_button = ttk.Button(self.key_frame, text="Generează Chei", command=self.generate_keys)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame pentru semnare
        self.sign_frame = ttk.LabelFrame(self.left_frame, text="Semnare Mesaj", padding="10")
        self.sign_frame.pack(fill=tk.X, pady=10)

        ttk.Label(self.sign_frame, text="Mesaj (x):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.message_entry = ttk.Entry(self.sign_frame, width=10)
        self.message_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.message_entry.insert(0, "100")

        ttk.Label(self.sign_frame, text="Valoare k:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.k_entry = ttk.Entry(self.sign_frame, width=10)
        self.k_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.k_entry.insert(0, "213")

        self.sign_button = ttk.Button(self.sign_frame, text="Semnează Mesaj", command=self.sign_message)
        self.sign_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame pentru verificare
        self.verify_frame = ttk.LabelFrame(self.left_frame, text="Verificare Semnătură", padding="10")
        self.verify_frame.pack(fill=tk.X, pady=10)

        ttk.Label(self.verify_frame, text="Mesaj (x):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.verify_message_entry = ttk.Entry(self.verify_frame, width=10)
        self.verify_message_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(self.verify_frame, text="γ:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.gamma_entry = ttk.Entry(self.verify_frame, width=10)
        self.gamma_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(self.verify_frame, text="δ:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.delta_entry = ttk.Entry(self.verify_frame, width=10)
        self.delta_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        self.verify_button = ttk.Button(self.verify_frame, text="Verifică Semnătura", command=self.verify_signature)
        self.verify_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame pentru aplicația ElGamal din exemplu
        self.example_frame = ttk.LabelFrame(self.left_frame, text="Exemplu din Cerință", padding="10")
        self.example_frame.pack(fill=tk.X, pady=10)

        self.example1_button = ttk.Button(self.example_frame, text="Exemplul 1 (p=467, α=2, a=127)",
                                          command=self.load_example1)
        self.example1_button.pack(fill=tk.X, pady=5)

        self.example2_button = ttk.Button(self.example_frame, text="Aplicație (p=131, α=7, a=19, k=17)",
                                          command=self.load_example2)
        self.example2_button.pack(fill=tk.X, pady=5)

        # Frame pentru jurnal de pași
        self.log_frame = ttk.LabelFrame(self.right_frame, text="Jurnal de Pași", padding="10")
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, width=60, height=30)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Frame pentru vizualizare grafică
        self.graph_frame = ttk.LabelFrame(self.right_frame, text="Vizualizare", padding="10")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Inițializare
        self.update_log("Bine ați venit la demonstrația algoritmului ElGamal pentru semnături digitale.")
        self.update_log("Selectați parametrii și generați cheile pentru a începe.")

        # Desenăm diagrama inițială
        self.update_graph()

    def update_log(self, text):
        """Actualizează jurnalul de pași"""
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def clear_log(self):
        """Șterge jurnalul de pași"""
        self.log_text.delete('1.0', tk.END)

    def generate_keys(self):
        """Generează cheile pentru algoritmul ElGamal"""
        try:
            p = int(self.p_entry.get())
            alpha = int(self.alpha_entry.get())
            a = int(self.a_entry.get())

            self.clear_log()
            self.elgamal.reset_log()

            if self.elgamal.generate_keys(p, alpha, a):
                self.update_log("Generarea cheilor a avut succes!")

                # Actualizăm jurnalul
                for step in self.elgamal.get_steps_log():
                    self.update_log(step)

                # Actualizăm vizualizarea
                self.update_graph()
            else:
                for step in self.elgamal.get_steps_log():
                    self.update_log(step)
        except ValueError:
            messagebox.showerror("Eroare", "Valorile introduse trebuie să fie numere întregi!")

    def sign_message(self):
        """Semnează un mesaj folosind algoritmul ElGamal"""
        try:
            x = int(self.message_entry.get())
            k = int(self.k_entry.get())

            self.clear_log()
            self.elgamal.reset_log()

            gamma, delta = self.elgamal.sign(x, k)

            if gamma is not None and delta is not None:
                self.update_log("Semnarea mesajului a avut succes!")

                # Actualizăm valorile în interfață
                self.verify_message_entry.delete(0, tk.END)
                self.verify_message_entry.insert(0, str(x))

                self.gamma_entry.delete(0, tk.END)
                self.gamma_entry.insert(0, str(gamma))

                self.delta_entry.delete(0, tk.END)
                self.delta_entry.insert(0, str(delta))

                # Actualizăm jurnalul
                for step in self.elgamal.get_steps_log():
                    self.update_log(step)

                # Actualizăm vizualizarea
                self.update_graph()
            else:
                for step in self.elgamal.get_steps_log():
                    self.update_log(step)
        except ValueError:
            messagebox.showerror("Eroare", "Valorile introduse trebuie să fie numere întregi!")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def verify_signature(self):
        """Verifică o semnătură folosind algoritmul ElGamal"""
        try:
            x = int(self.verify_message_entry.get())
            gamma = int(self.gamma_entry.get())
            delta = int(self.delta_entry.get())

            self.clear_log()
            self.elgamal.reset_log()

            valid = self.elgamal.verify(x, gamma, delta)

            # Actualizăm jurnalul
            for step in self.elgamal.get_steps_log():
                self.update_log(step)

            # Actualizăm vizualizarea
            self.update_graph()

            if valid:
                messagebox.showinfo("Verificare", "Semnătura este VALIDĂ!")
            else:
                messagebox.showwarning("Verificare", "Semnătura NU este validă!")
        except ValueError:
            messagebox.showerror("Eroare", "Valorile introduse trebuie să fie numere întregi!")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def load_example1(self):
        """Încarcă exemplul 1 din cerință"""
        self.p_entry.delete(0, tk.END)
        self.p_entry.insert(0, "467")

        self.alpha_entry.delete(0, tk.END)
        self.alpha_entry.insert(0, "2")

        self.a_entry.delete(0, tk.END)
        self.a_entry.insert(0, "127")

        self.message_entry.delete(0, tk.END)
        self.message_entry.insert(0, "100")

        self.k_entry.delete(0, tk.END)
        self.k_entry.insert(0, "213")

        self.clear_log()
        self.update_log("Exemplul 1 a fost încărcat.")
        self.update_log("Generați cheile și apoi semnați mesajul pentru a vedea pașii de calcul.")

    def load_example2(self):
        """Încarcă exemplul 2 din cerință"""
        self.p_entry.delete(0, tk.END)
        self.p_entry.insert(0, "131")

        self.alpha_entry.delete(0, tk.END)
        self.alpha_entry.insert(0, "7")

        self.a_entry.delete(0, tk.END)
        self.a_entry.insert(0, "19")

        self.message_entry.delete(0, tk.END)
        self.message_entry.insert(0, "78")

        self.k_entry.delete(0, tk.END)
        self.k_entry.insert(0, "17")

        self.clear_log()
        self.update_log("Aplicația din cerință a fost încărcată.")
        self.update_log("Generați cheile și apoi semnați mesajul pentru a vedea pașii de calcul.")

    def update_graph(self):
        """Actualizează vizualizarea grafică"""
        self.ax.clear()

        # Desenăm diagrama ElGamal
        if hasattr(self.elgamal, 'p') and self.elgamal.p > 0:
            p = self.elgamal.p
            alpha = self.elgamal.alpha
            beta = self.elgamal.beta
            a = self.elgamal.a

            # Creăm o diagramă simplă a procesului
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)
            self.ax.axis('off')

            # Titlu
            self.ax.text(5, 9.5, "Algoritm ElGamal pentru Semnături Digitale",
                         fontsize=12, ha='center', fontweight='bold')

            # Parametrii
            self.ax.text(1, 8.5, f"Parametri Publici:", fontsize=10, fontweight='bold')
            self.ax.text(1, 8, f"p = {p} (mod)", fontsize=10)
            self.ax.text(1, 7.5, f"α = {alpha} (generator)", fontsize=10)
            self.ax.text(1, 7, f"β = {beta} (cheia publică)", fontsize=10)

            self.ax.text(1, 6, f"Parametri Privați:", fontsize=10, fontweight='bold')
            self.ax.text(1, 5.5, f"a = {a} (cheia privată)", fontsize=10)

            # Schema de semnare
            self.ax.add_patch(plt.Rectangle((0.5, 2.5), 4, 2, fill=False, edgecolor='blue'))
            self.ax.text(2.5, 4, "Semnare", fontsize=10, ha='center', fontweight='bold')
            self.ax.text(2.5, 3.5, "1. Alege k aleator", fontsize=9, ha='center')
            self.ax.text(2.5, 3, "2. Calculează γ = α^k mod p", fontsize=9, ha='center')
            self.ax.text(2.5, 2.5, "3. Calculează δ = (x-a*γ)*k^(-1) mod (p-1)", fontsize=9, ha='center')

            # Schema de verificare
            self.ax.add_patch(plt.Rectangle((5.5, 2.5), 4, 2, fill=False, edgecolor='green'))
            self.ax.text(7.5, 4, "Verificare", fontsize=10, ha='center', fontweight='bold')
            self.ax.text(7.5, 3.5, "1. Calculează β^γ * γ^δ mod p", fontsize=9, ha='center')
            self.ax.text(7.5, 3, "2. Calculează α^x mod p", fontsize=9, ha='center')
            self.ax.text(7.5, 2.5, "3. Verifică dacă cele două valori sunt egale", fontsize=9, ha='center')

            # Săgeți
            self.ax.arrow(4.5, 3.5, 1, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')

            # Semnătură
            if hasattr(self.elgamal, 'k') and self.elgamal.k > 0:
                self.ax.text(5, 1.5, f"Semnătură pentru mesajul x:", fontsize=10, ha='center', fontweight='bold')

                # Încercăm să obținem valorile semnăturii
                try:
                    x = int(self.message_entry.get())
                    k = int(self.k_entry.get())
                    gamma, delta = self.elgamal.sign(x, k)

                    if gamma is not None and delta is not None:
                        self.ax.text(5, 1, f"(γ,δ) = ({gamma},{delta})", fontsize=10, ha='center')
                except:
                    pass

        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElGamalSignatureApp(root)
    root.mainloop()