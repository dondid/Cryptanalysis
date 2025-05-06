import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import sympy
import matplotlib

matplotlib.use('TkAgg')  # Setăm backend-ul pentru Matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'  # Setăm fontul pentru a afișa corect caracterele speciale


class DLPVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Problema Logaritmului Discret (DLP) - Vizualizator")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")
        self.iconbitmap(default='')  # Prevenim eroarea iconului lipsă

        # Stil pentru aplicație
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', background='#4CAF50', foreground='black', font=('Arial', 10, 'bold'))
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 11))
        style.configure('Header.TLabel', background='#f0f0f0', font=('Arial', 14, 'bold'))

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame pentru input
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Titlu
        title_label = ttk.Label(input_frame, text="Problema Logaritmului Discret (DLP)", style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=6, pady=10)

        # Input pentru numărul prim p
        p_label = ttk.Label(input_frame, text="Număr prim p:")
        p_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.p_entry = ttk.Entry(input_frame, width=10)
        self.p_entry.grid(row=1, column=1, padx=5, pady=5)
        self.p_entry.insert(0, "17")

        # Input pentru generatorul g
        g_label = ttk.Label(input_frame, text="Generator g:")
        g_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.g_entry = ttk.Entry(input_frame, width=10)
        self.g_entry.grid(row=1, column=3, padx=5, pady=5)
        self.g_entry.insert(0, "3")

        # Input pentru elementul b
        b_label = ttk.Label(input_frame, text="Element b:")
        b_label.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        self.b_entry = ttk.Entry(input_frame, width=10)
        self.b_entry.grid(row=1, column=5, padx=5, pady=5)
        self.b_entry.insert(0, "12")

        # Butoane pentru algoritmi
        algo_frame = ttk.Frame(main_frame)
        algo_frame.pack(fill=tk.X, padx=5, pady=5)

        # Descriere
        desc_label = ttk.Label(algo_frame, text="Selectați algoritmul pentru rezolvarea DLP:")
        desc_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=tk.W)

        # Buton pentru Căutare Exhaustivă (Brute Force)
        bf_button = ttk.Button(algo_frame, text="Căutare Exhaustivă", command=self.brute_force)
        bf_button.grid(row=1, column=0, padx=5, pady=5)

        # Buton pentru Algoritmul Baby-step Giant-step
        bsgs_button = ttk.Button(algo_frame, text="Baby-step Giant-step", command=self.baby_step_giant_step)
        bsgs_button.grid(row=1, column=1, padx=5, pady=5)

        # Buton pentru Algoritmul Pollard's Rho
        rho_button = ttk.Button(algo_frame, text="Pollard's Rho", command=self.pollard_rho)
        rho_button.grid(row=1, column=2, padx=5, pady=5)

        # Buton pentru Algoritmul Pohlig-Hellman
        ph_button = ttk.Button(algo_frame, text="Pohlig-Hellman", command=self.pohlig_hellman)
        ph_button.grid(row=1, column=3, padx=5, pady=5)

        # Frame pentru vizualizare
        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Creare notebook pentru tab-uri
        self.notebook = ttk.Notebook(viz_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab pentru text/pași matematici
        self.math_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.math_frame, text='Pași Matematici')

        # Zona de text pentru output matematic
        self.math_output = scrolledtext.ScrolledText(self.math_frame, wrap=tk.WORD, font=('Consolas', 11))
        self.math_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tab pentru vizualizare grafică
        self.graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text='Vizualizare Grafică')

        # Figura pentru plot
        self.fig = plt.Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def validate_inputs(self):
        try:
            p = int(self.p_entry.get())
            g = int(self.g_entry.get())
            b = int(self.b_entry.get())

            # Verificare dacă p este prim
            if not sympy.isprime(p):
                messagebox.showerror("Eroare", f"{p} nu este un număr prim!")
                return None, None, None

            # Verificare dacă g este generator pentru Zp*
            if not self.is_generator(g, p):
                messagebox.showerror("Eroare", f"{g} nu este un generator pentru Z{p}*!")
                return None, None, None

            # Verificare dacă b aparține Zp*
            if b <= 0 or b >= p or math.gcd(b, p) != 1:
                messagebox.showerror("Eroare", f"{b} nu aparține grupului Z{p}*!")
                return None, None, None

            return p, g, b
        except ValueError:
            messagebox.showerror("Eroare", "Introduceți numere întregi valide!")
            return None, None, None

    def is_generator(self, g, p):
        # Verifică dacă g este generator pentru Zp*
        if g <= 0 or g >= p or math.gcd(g, p) != 1:
            return False

        # Calculează phi(p)
        phi = p - 1

        # Găsește factorii primi ai lui phi
        factors = set()
        n = phi
        i = 2
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.add(i)
        if n > 1:
            factors.add(n)

        # Verifică dacă g este generator
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                return False
        return True

    def clear_outputs(self):
        # Curăță output-ul matematic
        self.math_output.delete('1.0', tk.END)

        # Curăță graficele
        self.fig.clear()

    def brute_force(self):
        self.clear_outputs()
        p, g, b = self.validate_inputs()
        if None in (p, g, b):
            return

        self.math_output.insert(tk.END, "Rezolvarea DLP folosind Căutarea Exhaustivă (Brute Force):\n\n")
        self.math_output.insert(tk.END, f"Parametri: p = {p}, g = {g}, b = {b}\n")
        self.math_output.insert(tk.END, f"Problema: Găsim x astfel încât g^x ≡ b (mod p)\n")
        self.math_output.insert(tk.END, f"         {g}^x ≡ {b} (mod {p})\n\n")

        # Pasul 1: Factorizăm p-1
        phi = p - 1
        self.math_output.insert(tk.END, f"Pasul 1: Factorizăm p-1 = {phi} în factori primi:\n")

        # Găsim factorizarea lui p-1
        factors = {}
        n = phi
        i = 2
        while i * i <= n:
            if n % i:
                i += 1
            else:
                count = 0
                while n % i == 0:
                    n //= i
                    count += 1
                factors[i] = count
        if n > 1:
            factors[n] = 1

        # Afisăm factorizarea
        factor_str = " × ".join([f"{f}^{e}" for f, e in factors.items()])
        self.math_output.insert(tk.END, f"{phi} = {factor_str}\n\n")

        if len(factors) == 1 and list(factors.values())[0] == 1:
            self.math_output.insert(tk.END,
                                    f"Întrucât p-1 = {phi} este un număr prim, putem folosi direct algoritmul baby-step giant-step.\n")
            self.baby_step_giant_step()
            return

        self.math_output.insert(tk.END,
                                "Pasul 2: Pentru fiecare factor prim q cu exponentul e din factorizarea lui p-1:\n")

        # Pentru a stoca congruențele
        congruences = []
        moduli = []

        # Pentru vizualizare
        prime_results = []

        for q, e in factors.items():
            q_e = q ** e
            self.math_output.insert(tk.END,
                                    f"\n--- Pentru factorul prim q = {q} cu exponentul e = {e} (q^e = {q_e}) ---\n")

            # Calculăm elementele pentru sub-problemă
            g_q = pow(g, phi // q_e, p)
            self.math_output.insert(tk.END, f"g_q = g^(phi/q^e) mod p = {g}^({phi}/{q_e}) mod {p} = {g_q}\n")

            # Rezolvăm sub-problemele pentru fiecare factor prim
            x_q = 0

            for j in range(e):
                # Calculăm b_j
                temp = pow(g, x_q, p)
                b_inv = pow(temp, p - 2, p)
                b_j = (b * b_inv) % p
                b_j = pow(b_j, phi // (q ** (j + 1)), p)

                self.math_output.insert(tk.END, f"  Pasul 2.{j + 1}: Pentru j = {j}:\n")
                self.math_output.insert(tk.END, f"    b_j = (b * g^(-x_q))^(phi/q^(j+1)) mod p = {b_j}\n")

                # Rezolvăm DLP pentru sub-problemă folosind căutare simplă
                g_qj = pow(g_q, q ** j, p)
                d_j = None

                self.math_output.insert(tk.END, f"    Căutăm d_j astfel încât (g_q)^(q^j * d_j) ≡ b_j (mod p):\n")

                for d in range(q):
                    val = pow(g_qj, d, p)
                    if val == b_j:
                        d_j = d
                        self.math_output.insert(tk.END, f"      d = {d}: {g_qj}^{d} mod {p} = {val} = {b_j} ✓\n")
                        break
                    else:
                        self.math_output.insert(tk.END, f"      d = {d}: {g_qj}^{d} mod {p} = {val} != {b_j}\n")

                if d_j is not None:
                    x_q += d_j * (q ** j)
                    self.math_output.insert(tk.END, f"    Am găsit d_j = {d_j}\n")
                    self.math_output.insert(tk.END,
                                            f"    x_q = x_q + d_j * q^j = {x_q - d_j * (q ** j)} + {d_j} * {q}^{j} = {x_q}\n")
                else:
                    self.math_output.insert(tk.END, f"    Nu am găsit d_j. Algoritmul eșuează.\n")
                    return

            self.math_output.insert(tk.END, f"\n  Soluția pentru sub-problema q = {q}: x ≡ {x_q} (mod {q_e})\n")
            congruences.append(x_q)
            moduli.append(q_e)
            prime_results.append((q, e, x_q))

        # Pasul 3: Aplicăm Teorema Chinezească a Resturilor
        self.math_output.insert(tk.END,
                                "\nPasul 3: Aplicăm Teorema Chinezească a Resturilor pentru a combina congruențele:\n")
        for i, (x_i, mod_i) in enumerate(zip(congruences, moduli)):
            self.math_output.insert(tk.END, f"  x ≡ {x_i} (mod {mod_i})\n")

        # Implementăm TCR
        result = 0
        for i in range(len(congruences)):
            a_i = congruences[i]
            m_i = moduli[i]
            M = phi // m_i
            M_i_inv = pow(M, m_i - 2, m_i)  # Invers modular
            result = (result + a_i * M * M_i_inv) % phi

        self.math_output.insert(tk.END, f"\nSoluția finală este x = {result}\n")
        self.math_output.insert(tk.END, f"Verificare: {g}^{result} mod {p} = {pow(g, result, p)}")

        if pow(g, result, p) == b:
            self.math_output.insert(tk.END, f" = {b} ✓\n")
        else:
            self.math_output.insert(tk.END, f" != {b} ✗\n")

        # Vizualizare grafică pentru Pohlig-Hellman
        ax1 = self.fig.add_subplot(121)
        ax1.set_title("Factorizarea lui p-1")

        # Creăm un pie chart pentru factorii primi
        labels = [f"$q={q}^{e}={q ** e}$" for q, e in factors.items()]
        sizes = [q ** e for q, e in factors.items()]
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')

        # Vizualizăm soluțiile parțiale
        ax2 = self.fig.add_subplot(122)
        ax2.set_title("Soluții pentru sub-probleme")

        q_vals = [f"q={pr[0]}^{pr[1]}" for pr in prime_results]
        x_q_vals = [pr[2] for pr in prime_results]

        ax2.bar(q_vals, x_q_vals)
        ax2.set_xlabel('Factor prim q^e')
        ax2.set_ylabel('Soluție parțială x_q')

        for i, v in enumerate(x_q_vals):
            ax2.text(i, v + 0.1, str(v), ha='center')

        self.fig.tight_layout()
        self.canvas.draw()

        # Selectează tab-ul cu pașii matematici
        self.notebook.select(0)
        self.math_output.insert(tk.END, f"         {g}^x ≡ {b} (mod {p})\n\n")

        # Algoritmul de căutare exhaustivă
        self.math_output.insert(tk.END, "Calculăm g^x mod p pentru fiecare x de la 1 la p-1:\n\n")

        result = None
        powers = []

        for x in range(1, p):
            power = pow(g, x, p)
            powers.append((x, power))
            self.math_output.insert(tk.END, f"x = {x}: {g}^{x} mod {p} = {power}")

            if power == b:
                self.math_output.insert(tk.END, " ✓ GĂSIT!\n")
                result = x
                break
            else:
                self.math_output.insert(tk.END, "\n")

        if result is not None:
            self.math_output.insert(tk.END, f"\nSoluția este x = {result}\n")
            self.math_output.insert(tk.END, f"Verificare: {g}^{result} mod {p} = {pow(g, result, p)} = {b} ✓\n")
        else:
            self.math_output.insert(tk.END, "\nNu s-a găsit nicio soluție!\n")

        # Vizualizare grafică
        ax1 = self.fig.add_subplot(121)
        ax1.set_title(f"Valorile lui g^x mod p pentru x de la 1 la {p - 1}")
        x_vals = [p[0] for p in powers]
        y_vals = [p[1] for p in powers]
        ax1.plot(x_vals, y_vals, 'bo-', markersize=5)
        ax1.axhline(y=b, color='r', linestyle='--', label=f'b = {b}')
        ax1.set_xlabel('x')
        ax1.set_ylabel('g^x mod p')
        ax1.grid(True)
        ax1.legend()

        # Vizualizare circulară
        ax2 = self.fig.add_subplot(122, polar=True)
        ax2.set_title(f"Reprezentare ciclică a g^x mod p")

        theta = [2 * np.pi * val / p for val in [p[1] for p in powers]]
        r = [1] * len(powers)

        scatter = ax2.scatter(theta, r, c=range(len(powers)), cmap='hsv', s=100, alpha=0.7)

        # Adăugăm o bară de culoare pentru a înțelege corespondența cu valorile lui x
        cbar = plt.colorbar(scatter, ax=ax2, orientation='vertical', pad=0.1)
        cbar.set_label('Valoarea exponentului x')

        # Evidențiază b
        b_theta = 2 * np.pi * b / p
        ax2.scatter([b_theta], [1], c='red', s=150, marker='*', label=f'b = {b}')

        ax2.set_rticks([])  # Eliminare marcaje pe axa radială
        ax2.set_rlabel_position(0)
        ax2.set_xticks([2 * np.pi * i / p for i in range(0, p, max(1, p // 8))])
        ax2.set_xticklabels([str(i) for i in range(0, p, max(1, p // 8))])
        ax2.legend()

        self.fig.tight_layout()
        self.canvas.draw()

        # Selectează tab-ul cu pașii matematici
        self.notebook.select(0)

    def baby_step_giant_step(self):
        self.clear_outputs()
        p, g, b = self.validate_inputs()
        if None in (p, g, b):
            return

        self.math_output.insert(tk.END, "Rezolvarea DLP folosind Algoritmul Baby-step Giant-step:\n\n")
        self.math_output.insert(tk.END, f"Parametri: p = {p}, g = {g}, b = {b}\n")
        self.math_output.insert(tk.END, f"Problema: Găsim x astfel încât g^x ≡ b (mod p)\n")
        self.math_output.insert(tk.END, f"         {g}^x ≡ {b} (mod {p})\n\n")

        # Algoritmul Baby-step Giant-step
        m = int(math.ceil(math.sqrt(p - 1)))
        self.math_output.insert(tk.END, f"Pasul 1: Calculăm m = ⌈√(p-1)⌉ = ⌈√{p - 1}⌉ = {m}\n\n")

        self.math_output.insert(tk.END, "Pasul 2: Calculăm și stocăm valorile pentru 'baby steps':\n")
        self.math_output.insert(tk.END, "Calculăm g^j mod p pentru j de la 0 la m-1:\n\n")

        # Baby steps: calculăm g^j pentru j=0,1,...,m-1
        baby_steps = {}
        baby_vals = []

        for j in range(m):
            value = pow(g, j, p)
            baby_steps[value] = j
            baby_vals.append((j, value))
            self.math_output.insert(tk.END, f"j = {j}: g^{j} mod {p} = {value}\n")

        self.math_output.insert(tk.END, "\nPasul 3: Calculăm valorile pentru 'giant steps':\n")
        self.math_output.insert(tk.END, f"Calculăm b * (g^(-m))^i mod p pentru i de la 0 la m:\n\n")

        # Calculăm g^(-m) mod p
        g_inv = pow(g, p - 2, p)  # Invers modular prin teorema lui Fermat
        g_m_inv = pow(g_inv, m, p)
        self.math_output.insert(tk.END, f"g^(-m) mod {p} = {g_m_inv}\n\n")

        # Giant steps: calculăm b * (g^(-m))^i pentru i=0,1,...,m
        giant_vals = []
        result = None

        for i in range(m + 1):
            value = (b * pow(g_m_inv, i, p)) % p
            giant_vals.append((i, value))

            self.math_output.insert(tk.END, f"i = {i}: b * (g^(-m))^{i} mod {p} = {value}")

            if value in baby_steps:
                j = baby_steps[value]
                result = i * m + j
                self.math_output.insert(tk.END, f" ✓ GĂSIT! (coliziune cu j = {j})\n")
                break
            else:
                self.math_output.insert(tk.END, "\n")

        if result is not None:
            self.math_output.insert(tk.END, f"\nSoluția este x = i*m + j = {i}*{m} + {j} = {result}\n")
            self.math_output.insert(tk.END, f"Verificare: {g}^{result} mod {p} = {pow(g, result, p)} = {b} ✓\n")
        else:
            self.math_output.insert(tk.END, "\nNu s-a găsit nicio soluție!\n")

        # Vizualizare grafică
        ax1 = self.fig.add_subplot(121)
        ax1.set_title("Baby Steps și Giant Steps")

        # Plot pentru baby steps
        baby_x = [p[0] for p in baby_vals]
        baby_y = [p[1] for p in baby_vals]
        ax1.scatter(baby_x, baby_y, c='blue', label='Baby Steps (g^j)')

        # Plot pentru giant steps
        giant_x = [p[0] for p in giant_vals]
        giant_y = [p[1] for p in giant_vals]
        ax1.scatter(giant_x, giant_y, c='red', marker='x', label='Giant Steps (b*(g^(-m))^i)')

        # Dacă s-a găsit o coliziune, o evidențiem
        if result is not None:
            collision_y = baby_steps[giant_vals[i][1]]
            ax1.scatter([j], [giant_vals[i][1]], c='green', s=150, marker='*', label='Coliziune')

        ax1.set_xlabel('Indice (j pentru baby, i pentru giant)')
        ax1.set_ylabel('Valoare mod p')
        ax1.grid(True)
        ax1.legend()

        # Vizualizare pe cercul modular
        ax2 = self.fig.add_subplot(122, polar=True)
        ax2.set_title(f"Reprezentare ciclică a valorilor mod {p}")

        # Baby steps pe cerc
        theta_baby = [2 * np.pi * val / p for val in baby_y]
        r_baby = [0.7] * len(baby_y)  # Raza mai mică pentru baby steps
        ax2.scatter(theta_baby, r_baby, c='blue', s=60, alpha=0.7, label='Baby Steps')

        # Giant steps pe cerc
        theta_giant = [2 * np.pi * val / p for val in giant_y]
        r_giant = [1.0] * len(giant_y)  # Raza mai mare pentru giant steps
        ax2.scatter(theta_giant, r_giant, c='red', s=60, marker='x', alpha=0.7, label='Giant Steps')

        # Evidențiază coliziunea
        if result is not None:
            collision_theta = 2 * np.pi * giant_vals[i][1] / p
            ax2.scatter([collision_theta], [0.85], c='green', s=150, marker='*', label='Coliziune')

        ax2.set_rticks([])  # Eliminare marcaje pe axa radială
        ax2.set_xticks([2 * np.pi * i / p for i in range(0, p, max(1, p // 8))])
        ax2.set_xticklabels([str(i) for i in range(0, p, max(1, p // 8))])
        ax2.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))

        self.fig.tight_layout()
        self.canvas.draw()

        # Selectează tab-ul cu pașii matematici
        self.notebook.select(0)

    def pollard_rho(self):
        self.clear_outputs()
        p, g, b = self.validate_inputs()
        if None in (p, g, b):
            return

        self.math_output.insert(tk.END, "Rezolvarea DLP folosind Algoritmul Pollard's Rho:\n\n")
        self.math_output.insert(tk.END, f"Parametri: p = {p}, g = {g}, b = {b}\n")
        self.math_output.insert(tk.END, f"Problema: Găsim x astfel încât g^x ≡ b (mod p)\n")
        self.math_output.insert(tk.END, f"         {g}^x ≡ {b} (mod {p})\n\n")

        # Definim funcția f pentru algoritmul Pollard's Rho
        def f(x_i, a_i, b_i):
            subset = x_i % 3
            if subset == 0:  # S_0
                return (b * x_i) % p, a_i, (b_i + 1) % (p - 1)
            elif subset == 1:  # S_1
                return (x_i * x_i) % p, (2 * a_i) % (p - 1), (2 * b_i) % (p - 1)
            else:  # S_2
                return (g * x_i) % p, (a_i + 1) % (p - 1), b_i

        self.math_output.insert(tk.END,
                                "Pasul 1: Definim funcția f(x_i, a_i, b_i) care împarte Zp* în trei subseturi:\n")
        self.math_output.insert(tk.END,
                                "  - Pentru x_i ∈ S_0 (x_i % 3 = 0): f(x_i, a_i, b_i) = (b·x_i mod p, a_i, b_i+1 mod (p-1))\n")
        self.math_output.insert(tk.END,
                                "  - Pentru x_i ∈ S_1 (x_i % 3 = 1): f(x_i, a_i, b_i) = (x_i² mod p, 2·a_i mod (p-1), 2·b_i mod (p-1))\n")
        self.math_output.insert(tk.END,
                                "  - Pentru x_i ∈ S_2 (x_i % 3 = 2): f(x_i, a_i, b_i) = (g·x_i mod p, a_i+1 mod (p-1), b_i)\n\n")

        self.math_output.insert(tk.END, "Pasul 2: Inițializăm valorile de start și aplicăm algoritmul:\n")
        self.math_output.insert(tk.END, "  x_0 = 1, a_0 = 0, b_0 = 0\n\n")

        # Valorile inițiale
        x_slow, a_slow, b_slow = 1, 0, 0
        x_fast, a_fast, b_fast = 1, 0, 0

        # Pentru vizualizare
        points = [(0, 1)]  # (iterație, valoare x)
        a_vals = [0]
        b_vals = [0]
        iterations = 0
        max_iterations = p  # Evităm bucle infinite

        self.math_output.insert(tk.END, "Iterații:\n")
        self.math_output.insert(tk.END, f"i = 0: x_0 = 1, a_0 = 0, b_0 = 0\n")

        result = None

        while iterations < max_iterations:
            iterations += 1

            # Mișcăm pointerul lent o dată
            x_slow, a_slow, b_slow = f(x_slow, a_slow, b_slow)

            # Mișcăm pointerul rapid de două ori
            x_fast, a_fast, b_fast = f(x_fast, a_fast, b_fast)
            x_fast, a_fast, b_fast = f(x_fast, a_fast, b_fast)

            points.append((iterations, x_slow))
            a_vals.append(a_slow)
            b_vals.append(b_slow)

            self.math_output.insert(tk.END, f"i = {iterations}:\n")
            self.math_output.insert(tk.END,
                                    f"  - Pointer lent: x_{iterations} = {x_slow}, a_{iterations} = {a_slow}, b_{iterations} = {b_slow}\n")
            self.math_output.insert(tk.END,
                                    f"  - Pointer rapid: x_{iterations}' = {x_fast}, a_{iterations}' = {a_fast}, b_{iterations}' = {b_fast}\n")

            # Verificăm dacă am găsit o coliziune
            if x_slow == x_fast:
                self.math_output.insert(tk.END, f"  → Coliziune găsită la iterația {iterations}!\n\n")

                # Rezolvăm ecuația modulară pentru a găsi x
                if b_slow == b_fast:
                    self.math_output.insert(tk.END, "Nu putem determina soluția deoarece b_lent = b_rapid.\n")
                    self.math_output.insert(tk.END, "Reluați algoritumul cu alte valori inițiale.\n")
                    break

                # b_slow - b_fast nu trebuie să fie divizibil cu p-1
                diff = (b_slow - b_fast) % (p - 1)
                if math.gcd(diff, p - 1) != 1:
                    self.math_output.insert(tk.END, f"GCDN(b_lent - b_rapid, p-1) = GCDN({diff}, {p - 1}) != 1\n")
                    self.math_output.insert(tk.END,
                                            "Nu putem determina soluția direct. Reluați cu alte valori inițiale.\n")
                    break

                # Calculăm x = (a_fast - a_slow) * (b_slow - b_fast)^(-1) mod (p-1)
                diff_a = (a_fast - a_slow) % (p - 1)
                diff_b_inv = pow(diff, p - 3, p - 1)  # Inversul modular prin teorema lui Fermat
                result = (diff_a * diff_b_inv) % (p - 1)

                self.math_output.insert(tk.END, "Pasul 3: Rezolvăm pentru x:\n")
                self.math_output.insert(tk.END, f"x = (a_rapid - a_lent) * (b_lent - b_rapid)^(-1) mod (p-1)\n")
                self.math_output.insert(tk.END, f"x = ({a_fast} - {a_slow}) * ({diff})^(-1) mod {p - 1}\n")
                self.math_output.insert(tk.END, f"x = {diff_a} * {diff_b_inv} mod {p - 1}\n")
                self.math_output.insert(tk.END, f"x = {result}\n\n")

                self.math_output.insert(tk.END, f"Verificare: {g}^{result} mod {p} = {pow(g, result, p)}")
                if pow(g, result, p) == b:
                    self.math_output.insert(tk.END, f" = {b} ✓\n")
                else:
                    self.math_output.insert(tk.END, f" != {b} ✗\n")
                    self.math_output.insert(tk.END, "Soluția nu este corectă. Reluați algoritmul.\n")
                    result = None

                break

        if iterations >= max_iterations:
            self.math_output.insert(tk.END, "\nNumărul maxim de iterații a fost atins fără a găsi o coliziune.\n")

        # Vizualizare grafică
        ax1 = self.fig.add_subplot(121)
        ax1.set_title("Traiectoria valorilor x_i (Pollard's Rho)")

        iter_vals = [p[0] for p in points]
        x_vals = [p[1] for p in points]

        ax1.plot(iter_vals, x_vals, 'bo-', markersize=5)
        ax1.set_xlabel('Iterație')
        ax1.set_ylabel('Valoare x_i')
        ax1.grid(True)

        # Vizualizare valori a_i și b_i
        ax2 = self.fig.add_subplot(122)
        ax2.set_title("Valorile a_i și b_i de-a lungul iterațiilor")

        ax2.plot(iter_vals, a_vals, 'ro-', label='a_i')
        ax2.plot(iter_vals, b_vals, 'go-', label='b_i')
        ax2.set_xlabel('Iterație')
        ax2.set_ylabel('Valoare')
        ax2.grid(True)
        ax2.legend()

        self.fig.tight_layout()
        self.canvas.draw()

        # Selectează tab-ul cu pașii matematici
        self.notebook.select(0)

    def pohlig_hellman(self):
        self.clear_outputs()
        p, g, b = self.validate_inputs()
        if None in (p, g, b):
            return

        self.math_output.insert(tk.END, "Rezolvarea DLP folosind Algoritmul Pohlig-Hellman:\n\n")
        self.math_output.insert(tk.END, f"Parametri: p = {p}, g = {g}, b = {b}\n")
        self.math_output.insert(tk.END, f"Problema: Găsim x astfel încât g^x ≡ b (mod p)\n")

if __name__ == "__main__":
    app = DLPVisualizer()
    app.mainloop()