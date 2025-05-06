import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy
import math


class ElGamalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritm ElGamal")
        self.root.geometry("1200x800")

        # Creare notebook cu tab-uri
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab pentru explicații teoretice
        self.theory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.theory_tab, text="Teorie ElGamal")

        # Tab pentru aplicația 1
        self.app1_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.app1_tab, text="Cifrare")

        # Tab pentru aplicația 2
        self.app2_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.app2_tab, text="Descifrare")

        # Construiește interfața pentru fiecare tab
        self.build_theory_tab()
        self.build_app1_tab()
        self.build_app2_tab()

        # Focus pe primul tab
        self.notebook.select(0)

    def build_theory_tab(self):
        """Construiește tab-ul cu explicații teoretice"""
        frame = ttk.Frame(self.theory_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        ttk.Label(frame, text="Algoritmul ElGamal", font=("Arial", 18, "bold")).pack(pady=10)

        # Text explicativ
        explanation = """
        Algoritmul ElGamal este un algoritm de criptografie cu cheie publică bazat pe problema logaritmului discret.

        GENERAREA CHEILOR:
        1. Se alege un număr prim p (modulus)
        2. Se alege un generator α al grupului multiplicativ Z*p (1 < α < p)
        3. Se alege un număr secret a (1 < a < p-1)
        4. Se calculează β = α^a mod p
        5. Cheia publică este (p, α, β), iar cheia privată este a

        CIFRAREA unui mesaj x:
        1. Se alege un număr aleator k (1 < k < p-1)
        2. Se calculează γ = α^k mod p
        3. Se calculează δ = x·β^k mod p
        4. Mesajul cifrat este perechea (γ, δ)

        DESCIFRAREA unui mesaj cifrat (γ, δ):
        1. Se calculează γ^a mod p
        2. Se calculează (γ^a)^(-1) mod p = γ^(-a) mod p
        3. Se recuperează mesajul original x = δ·γ^(-a) mod p
        """

        text_widget = tk.Text(frame, wrap=tk.WORD, height=20, width=80)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        text_widget.insert(tk.END, explanation)
        text_widget.config(state=tk.DISABLED)

        # Imagine explicativă
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title("Vizualizare algoritm ElGamal")

        # Desenare imagine conceptuală
        ax.text(0.05, 0.9, "CIFRARE:", fontsize=12, fontweight='bold')
        ax.text(0.1, 0.75, "Mesaj (x) → Cifrare cu (p, α, β, k) → Ciphertext (γ, δ)", fontsize=10)

        ax.text(0.05, 0.5, "DESCIFRARE:", fontsize=12, fontweight='bold')
        ax.text(0.1, 0.35, "Ciphertext (γ, δ) → Descifrare cu a → Mesaj (x)", fontsize=10)

        ax.text(0.1, 0.1, "Securitatea se bazează pe dificultatea calculării logaritmului discret.", fontsize=10,
                style='italic')

        ax.axis('off')

        # Adăugare imagine în interfață
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def build_app1_tab(self):
        """Construiește tab-ul pentru cifrare cu input de la utilizator"""
        frame = ttk.Frame(self.app1_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        ttk.Label(frame, text="Cifrare ElGamal", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame pentru parametri
        param_frame = ttk.LabelFrame(frame, text="Introduceți parametrii", padding=10)
        param_frame.pack(fill=tk.X, pady=10)

        # Parametri pentru cifrare
        ttk.Label(param_frame, text="Număr prim (p):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.p1_entry = ttk.Entry(param_frame, width=10)
        self.p1_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.p1_entry.insert(0, "17")  # Valoare implicită

        ttk.Label(param_frame, text="Generator (α):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.alpha1_entry = ttk.Entry(param_frame, width=10)
        self.alpha1_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.alpha1_entry.insert(0, "14")  # Valoare implicită

        ttk.Label(param_frame, text="Cheie privată (a):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.a1_entry = ttk.Entry(param_frame, width=10)
        self.a1_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.a1_entry.insert(0, "2")  # Valoare implicită

        ttk.Label(param_frame, text="Mesaj de cifrat (x):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.x_entry = ttk.Entry(param_frame, width=10)
        self.x_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.x_entry.insert(0, "8")  # Valoare implicită

        ttk.Label(param_frame, text="Valoare k:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.k_entry = ttk.Entry(param_frame, width=10)
        self.k_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.k_entry.insert(0, "3")  # Valoare implicită

        # Buton pentru calcul
        ttk.Button(frame, text="Calculează cifrarea", command=self.run_app1).pack(pady=10)

        # Zonă pentru rezultate
        self.app1_result_frame = ttk.LabelFrame(frame, text="Rezultate calcul", padding=10)
        self.app1_result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Text widget pentru afișarea pașilor
        self.app1_steps_text = tk.Text(self.app1_result_frame, wrap=tk.WORD, height=12, width=80)
        self.app1_steps_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas pentru reprezentare vizuală
        self.app1_figure_frame = ttk.Frame(frame)
        self.app1_figure_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.app1_fig = plt.Figure(figsize=(8, 4))
        self.app1_canvas = FigureCanvasTkAgg(self.app1_fig, self.app1_figure_frame)
        self.app1_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def build_app2_tab(self):
        """Construiește tab-ul pentru descifrare cu input de la utilizator"""
        frame = ttk.Frame(self.app2_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        ttk.Label(frame, text="Descifrare ElGamal", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame pentru parametri
        param_frame = ttk.LabelFrame(frame, text="Introduceți parametrii", padding=10)
        param_frame.pack(fill=tk.X, pady=10)

        # Parametri pentru descifrare
        ttk.Label(param_frame, text="Număr prim (p):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.p2_entry = ttk.Entry(param_frame, width=10)
        self.p2_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.p2_entry.insert(0, "23")  # Valoare implicită

        ttk.Label(param_frame, text="Generator (α):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.alpha2_entry = ttk.Entry(param_frame, width=10)
        self.alpha2_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.alpha2_entry.insert(0, "7")  # Valoare implicită

        ttk.Label(param_frame, text="Cheie privată (a):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.a2_entry = ttk.Entry(param_frame, width=10)
        self.a2_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.a2_entry.insert(0, "3")  # Valoare implicită

        ttk.Label(param_frame, text="γ:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.gamma_entry = ttk.Entry(param_frame, width=10)
        self.gamma_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.gamma_entry.insert(0, "21")  # Valoare implicită

        ttk.Label(param_frame, text="δ:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.delta_entry = ttk.Entry(param_frame, width=10)
        self.delta_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.delta_entry.insert(0, "14")  # Valoare implicită

        # Buton pentru calcul
        ttk.Button(frame, text="Calculează descifrarea", command=self.run_app2).pack(pady=10)

        # Zonă pentru rezultate
        self.app2_result_frame = ttk.LabelFrame(frame, text="Rezultate calcul", padding=10)
        self.app2_result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Text widget pentru afișarea pașilor
        self.app2_steps_text = tk.Text(self.app2_result_frame, wrap=tk.WORD, height=12, width=80)
        self.app2_steps_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas pentru reprezentare vizuală
        self.app2_figure_frame = ttk.Frame(frame)
        self.app2_figure_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.app2_fig = plt.Figure(figsize=(8, 4))
        self.app2_canvas = FigureCanvasTkAgg(self.app2_fig, self.app2_figure_frame)
        self.app2_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def power_mod(self, base, exponent, modulus):
        """Calculează (base^exponent) mod modulus eficient"""
        result = 1
        base = base % modulus
        while exponent > 0:
            # Dacă exponentul este impar
            if exponent % 2 == 1:
                result = (result * base) % modulus
            # Exponentul devine jumatate
            exponent = exponent >> 1
            # Baza devine baza^2
            base = (base * base) % modulus
        return result

    def mod_inverse(self, a, m):
        """Calculează inversul modular a^(-1) mod m folosind algoritmul lui Euclid extins"""
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            raise Exception('Inversul modular nu există')
        else:
            return x % m

    def extended_gcd(self, a, b):
        """Implementează algoritmul lui Euclid extins pentru a găsi gcd și coeficienții Bézout"""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x1, y1 = self.extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

    def is_prime(self, n):
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

    def validate_input(self, p, alpha, a, x=None, k=None, gamma=None, delta=None, mode="encrypt"):
        """Validează input-ul pentru cifrare/descifrare"""
        if not self.is_prime(p):
            messagebox.showerror("Eroare", f"{p} nu este un număr prim!")
            return False

        if alpha <= 1 or alpha >= p:
            messagebox.showerror("Eroare", f"Generatorul α trebuie să fie între 1 și {p}!")
            return False

        if a <= 0 or a >= p - 1:
            messagebox.showerror("Eroare", f"Cheia privată 'a' trebuie să fie între 1 și {p - 2}!")
            return False

        if mode == "encrypt":
            if x < 0 or x >= p:
                messagebox.showerror("Eroare", f"Mesajul x trebuie să fie între 0 și {p - 1}!")
                return False

            if k <= 0 or k >= p - 1:
                messagebox.showerror("Eroare", f"Valoarea k trebuie să fie între 1 și {p - 2}!")
                return False
        else:  # mode == "decrypt"
            if gamma <= 0 or gamma >= p:
                messagebox.showerror("Eroare", f"γ trebuie să fie între 1 și {p - 1}!")
                return False

            if delta < 0 or delta >= p:
                messagebox.showerror("Eroare", f"δ trebuie să fie între 0 și {p - 1}!")
                return False

        return True

    def run_app1(self):
        """Execută cifrarea cu parametri de la utilizator"""
        try:
            # Obținem parametrii din inputuri
            p = int(self.p1_entry.get())
            alpha = int(self.alpha1_entry.get())
            a = int(self.a1_entry.get())
            x = int(self.x_entry.get())
            k = int(self.k_entry.get())

            # Validăm input-ul
            if not self.validate_input(p, alpha, a, x, k, mode="encrypt"):
                return

            # Calculul cheii publice (β)
            beta = self.power_mod(alpha, a, p)

            # Cifrare
            gamma = self.power_mod(alpha, k, p)
            delta = (x * self.power_mod(beta, k, p)) % p

            # Actualizare text cu pași
            steps = f"""Cifrarea mesajului x = {x} cu algoritmul ElGamal:

Parametri:
- p = {p} (număr prim)
- α = {alpha} (generator)
- a = {a} (cheie privată)

Pasul 1: Calculăm cheia publică β = α^a mod p = {alpha}^{a} mod {p} = {beta}

Pasul 2: Pentru cifrare, folosim k = {k}

Pasul 3: Calculăm γ = α^k mod p = {alpha}^{k} mod {p} = {gamma}

Pasul 4: Calculăm δ = x·β^k mod p = {x}·{beta}^{k} mod {p} = {x}·{self.power_mod(beta, k, p)} mod {p} = {delta}

Rezultat: Mesajul cifrat este perechea (γ, δ) = ({gamma}, {delta})
"""

            self.app1_steps_text.delete(1.0, tk.END)
            self.app1_steps_text.insert(tk.END, steps)

            # Vizualizare
            self.app1_fig.clear()
            ax = self.app1_fig.add_subplot(111)

            # Crearea unui grafic vizual pentru cifrare
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 3)
            ax.axis('off')

            # Desenare săgeți și text pentru proces
            ax.text(0.5, 2.5, f"Mesaj original\nx = {x}", ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.8))

            ax.text(5, 2.5, f"Cheia publică\n(p={p}, α={alpha}, β={beta})\nk={k}", ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))

            ax.text(9.5, 2.5, f"Mesaj cifrat\n(γ={gamma}, δ={delta})", ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='orange', alpha=0.8))

            # Săgeți
            ax.annotate("", xy=(3.5, 2.5), xytext=(1.5, 2.5),
                        arrowprops=dict(arrowstyle="->", lw=2))

            ax.annotate("", xy=(8.5, 2.5), xytext=(6.5, 2.5),
                        arrowprops=dict(arrowstyle="->", lw=2))

            # Formule
            ax.text(2.5, 2.0, f"γ = α^k mod p\nδ = x·β^k mod p", ha='center', fontsize=10)
            ax.text(7.5, 2.0, f"γ = {gamma}\nδ = {delta}", ha='center', fontsize=10)

            # Operațiile matematice detaliate
            ax.text(5, 1.0,
                    f"Calcule:\n"
                    f"β = α^a mod p = {alpha}^{a} mod {p} = {beta}\n"
                    f"γ = α^k mod p = {alpha}^{k} mod {p} = {gamma}\n"
                    f"δ = x·β^k mod p = {x}·{beta}^{k} mod {p} = {x}·{self.power_mod(beta, k, p)} mod {p} = {delta}",
                    ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))

            self.app1_canvas.draw()

        except ValueError:
            messagebox.showerror("Eroare", "Toate câmpurile trebuie să conțină numere întregi valide!")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))

    def run_app2(self):
        """Execută descifrarea cu parametri de la utilizator"""
        try:
            # Obținem parametrii din inputuri
            p = int(self.p2_entry.get())
            alpha = int(self.alpha2_entry.get())
            a = int(self.a2_entry.get())
            gamma = int(self.gamma_entry.get())
            delta = int(self.delta_entry.get())

            # Validăm input-ul
            if not self.validate_input(p, alpha, a, gamma=gamma, delta=delta, mode="decrypt"):
                return

            # Descifrare
            gamma_a = self.power_mod(gamma, a, p)
            gamma_a_inv = self.mod_inverse(gamma_a, p)
            x = (delta * gamma_a_inv) % p

            # Actualizare text cu pași
            steps = f"""Descifrarea mesajului (γ = {gamma}, δ = {delta}) cu algoritmul ElGamal:

Parametri:
- p = {p} (număr prim)
- α = {alpha} (generator)
- a = {a} (cheie privată)

Pasul 1: Calculăm γ^a mod p = {gamma}^{a} mod {p} = {gamma_a}

Pasul 2: Calculăm inversul modular (γ^a)^(-1) mod p = {gamma_a}^(-1) mod {p} = {gamma_a_inv}

Pasul 3: Recuperăm mesajul original x = δ·(γ^a)^(-1) mod p = {delta}·{gamma_a_inv} mod {p} = {x}

Rezultat: Mesajul original descifrat este x = {x}
"""

            self.app2_steps_text.delete(1.0, tk.END)
            self.app2_steps_text.insert(tk.END, steps)

            # Vizualizare
            self.app2_fig.clear()
            ax = self.app2_fig.add_subplot(111)

            # Crearea unui grafic vizual pentru descifrare
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 3)
            ax.axis('off')

            # Desenare săgeți și text pentru proces
            ax.text(0.5, 2.5, f"Mesaj cifrat\n(γ={gamma}, δ={delta})", ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='orange', alpha=0.8))

            ax.text(5, 2.5, f"Cheia privată\na = {a}", ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='pink', alpha=0.8))

            ax.text(9.5, 2.5, f"Mesaj descifrat\nx = {x}", ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.8))

            # Săgeți
            ax.annotate("", xy=(3.5, 2.5), xytext=(1.5, 2.5),
                        arrowprops=dict(arrowstyle="->", lw=2))

            ax.annotate("", xy=(8.5, 2.5), xytext=(6.5, 2.5),
                        arrowprops=dict(arrowstyle="->", lw=2))

            # Formule
            ax.text(2.5, 2.0, f"Calculăm γ^a mod p", ha='center', fontsize=10)
            ax.text(7.5, 2.0, f"x = δ·(γ^a)^(-1) mod p", ha='center', fontsize=10)

            # Operațiile matematice detaliate
            ax.text(5, 1.0,
                    f"Calcule:\n"
                    f"γ^a mod p = {gamma}^{a} mod {p} = {gamma_a}\n"
                    f"(γ^a)^(-1) mod p = {gamma_a}^(-1) mod {p} = {gamma_a_inv}\n"
                    f"x = δ·(γ^a)^(-1) mod p = {delta}·{gamma_a_inv} mod {p} = {x}",
                    ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))

            self.app2_canvas.draw()

        except ValueError:
            messagebox.showerror("Eroare", "Toate câmpurile trebuie să conțină numere întregi valide!")
        except Exception as e:
            messagebox.showerror("Eroare", str(e))


# Funcție pentru a rula aplicația
def main():
    root = tk.Tk()
    app = ElGamalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()