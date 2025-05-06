import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import math
import time
from sympy import isprime, factorint
from matplotlib.animation import FuncAnimation


class GeneratorGrupCiclicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generator Grup Ciclic")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        self.setup_ui()

        # Variabile pentru animație
        self.animation = None
        self.current_generator = None
        self.animation_speed = 1000  # ms între frame-uri

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Secțiunea de input
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="Introduceți ordinul grupului (n):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.n_entry = ttk.Entry(input_frame, width=20)
        self.n_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.n_entry.insert(0, "7")  # Valoare implicită

        ttk.Button(input_frame, text="Calculează", command=self.calculate).grid(row=0, column=2, padx=10)
        ttk.Button(input_frame, text="Explică Algoritmul", command=self.explain_algorithm).grid(row=0, column=3,
                                                                                                padx=10)

        # Buton pentru animație
        ttk.Button(input_frame, text="Animează Procesul", command=self.animate_generation).grid(row=0, column=4,
                                                                                                padx=10)

        # Control pentru viteza animației
        ttk.Label(input_frame, text="Viteză animație:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.speed_scale = ttk.Scale(input_frame, from_=100, to=2000, orient=tk.HORIZONTAL, length=200)
        self.speed_scale.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.speed_scale.set(1000)  # Valoare implicită

        # Etichetă pentru viteza curentă
        self.speed_label = ttk.Label(input_frame, text="1000 ms")
        self.speed_label.grid(row=1, column=3, sticky=tk.W, pady=5)

        # Actualizare etichetă când se schimbă viteza
        self.speed_scale.config(command=self.update_speed_label)

        # Secțiunea de rezultate
        result_frame = ttk.LabelFrame(main_frame, text="Rezultate", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame pentru output textual
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Textbox pentru afișarea pașilor
        ttk.Label(text_frame, text="Pașii algoritumului:").pack(anchor=tk.W)
        self.steps_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=50, height=20)
        self.steps_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Frame pentru vizualizare
        viz_frame = ttk.Frame(result_frame)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Canvas pentru grafic
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Indicator pentru animație
        self.status_label = ttk.Label(viz_frame, text="")
        self.status_label.pack(pady=5)

    def calculate(self):
        try:
            n = int(self.n_entry.get())
            if n <= 0:
                messagebox.showerror("Eroare", "Ordinul grupului trebuie să fie un număr pozitiv.")
                return

            self.steps_text.delete(1.0, tk.END)
            self.ax.clear()

            # Reset animație
            if self.animation:
                self.animation.event_source.stop()
                self.animation = None

            # Factorizarea lui n
            self.steps_text.insert(tk.END, f"Pasul 1: Factorizăm numărul n = {n}\n")

            if isprime(n):
                factors = {n: 1}
                self.steps_text.insert(tk.END, f"n = {n} este prim, deci factorizarea este: {n}^1\n\n")
            else:
                factors = factorint(n)
                factorization = " × ".join([f"{p}^{a}" for p, a in factors.items()])
                self.steps_text.insert(tk.END, f"n = {factorization}\n\n")

            # Găsirea unui generator
            self.steps_text.insert(tk.END, "Pasul 2: Căutăm un generator pentru grupul Z*_{" + str(n) + "}\n")

            # Calculăm phi(n) - indicator Euler
            phi_n = 1
            for p, a in factors.items():
                phi_n *= (p ** (a - 1)) * (p - 1)

            self.steps_text.insert(tk.END, f"Indicatorul lui Euler φ(n) = {phi_n}\n\n")

            # Găsim toți divizorii primi ai lui phi(n)
            phi_factors = factorint(phi_n)
            prime_divisors = list(phi_factors.keys())

            self.steps_text.insert(tk.END, f"Divizorii primi ai lui φ(n) sunt: {prime_divisors}\n\n")

            # Testăm elemente pentru a găsi un generator
            self.steps_text.insert(tk.END, "Pasul 3: Testăm elemente pentru a găsi un generator\n")

            # Elementele relativ prime cu n
            relatively_prime = []
            for a in range(1, n):
                if math.gcd(a, n) == 1:
                    relatively_prime.append(a)

            self.steps_text.insert(tk.END, f"Elementele relativ prime cu {n} sunt: {relatively_prime}\n\n")

            # Algoritmul din imagine
            self.current_generator = None  # Reset generator
            generators = []

            for a in relatively_prime:
                self.steps_text.insert(tk.END, f"\nTestăm a = {a}:\n")

                is_generator = True

                for i, p in enumerate(prime_divisors):
                    power = phi_n // p
                    b = pow(a, power, n)

                    self.steps_text.insert(tk.END, f"  Calculăm b = a^(φ(n)/{p}) = {a}^{power} mod {n} = {b}\n")

                    if b == 1:
                        self.steps_text.insert(tk.END, f"  Deoarece b = 1, {a} nu este generator.\n")
                        is_generator = False
                        break

                if is_generator:
                    self.steps_text.insert(tk.END, f"  {a} este generator al grupului ciclic Z*_{n}!\n")
                    generators.append(a)

                    # Arătăm ordinele tuturor elementelor pentru generatorul găsit
                    self.steps_text.insert(tk.END, "\nDemonstrație că este generator (generează toate elementele):\n")
                    generated = {}
                    for power in range(1, phi_n + 1):
                        val = pow(a, power, n)
                        generated[power] = val
                        self.steps_text.insert(tk.END, f"  {a}^{power} mod {n} = {val}\n")

                    # Verificăm dacă toate elementele din grup au fost generate
                    if set(generated.values()) == set(relatively_prime):
                        self.steps_text.insert(tk.END, f"\n{a} generează toate cele {phi_n} elemente ale grupului!\n")

                    break

            if not generators:
                self.steps_text.insert(tk.END, "\nNu s-a găsit niciun generator!")
                messagebox.showinfo("Informație", "Nu s-a găsit niciun generator pentru acest grup.")
            else:
                # Salvăm generatorul și alte date necesare pentru animație
                self.current_generator = generators[0]
                self.current_n = n
                self.relatively_prime = relatively_prime
                self.phi_n = phi_n

                # Vizualizarea grupului ciclic pe un cerc
                self.visualize_cyclic_group(n, generators[0], relatively_prime)

                # Actualizăm statusul
                self.status_label.config(text=f"Generator găsit: {self.current_generator}")

        except ValueError:
            messagebox.showerror("Eroare", "Introduceți un număr valid pentru ordinul grupului.")
        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")

    def visualize_cyclic_group(self, n, generator, elements, highlight_index=None):
        self.ax.clear()

        # Desenăm cercul
        circle = plt.Circle((0, 0), 1, fill=False, color='black')
        self.ax.add_patch(circle)

        # Plasăm elementele pe cerc
        angles = np.linspace(0, 2 * np.pi, len(elements), endpoint=False)

        # Coordonatele elementelor pe cerc
        x = np.cos(angles)
        y = np.sin(angles)

        # Plasăm elementele în ordinea generată de generator
        generated_order = []
        generated_values = []
        for power in range(1, len(elements) + 1):
            val = pow(generator, power, n)
            if val in elements:  # Doar elementele din grup
                idx = elements.index(val)
                generated_order.append(idx)
                generated_values.append(val)

        # Culorile punctelor - toate albastre inițial
        colors = ['blue'] * len(elements)
        sizes = [100] * len(elements)

        # Evidențierea punctului curent în animație
        if highlight_index is not None and highlight_index < len(generated_order):
            idx = generated_order[highlight_index]
            colors[idx] = 'red'
            sizes[idx] = 150

        # Desenăm punctele
        self.ax.scatter(x, y, s=sizes, c=colors, zorder=5)

        # Adăugăm etichete
        for i, element in enumerate(elements):
            self.ax.annotate(str(element), (x[i], y[i]),
                             xytext=(x[i] * 1.1, y[i] * 1.1),
                             ha='center', va='center',
                             fontsize=12)

        # Desenăm săgețile între elementele consecutive generate
        if highlight_index is not None:
            for i in range(min(highlight_index, len(generated_order) - 1)):
                idx1 = generated_order[i]
                idx2 = generated_order[i + 1]
                self.ax.arrow(x[idx1], y[idx1],
                              x[idx2] - x[idx1], y[idx2] - y[idx1],
                              head_width=0.05, head_length=0.1,
                              fc='green', ec='green', zorder=1,
                              length_includes_head=True, alpha=0.6)

            # Desenăm săgeata curentă în roșu dacă nu suntem la ultimul element
            if highlight_index < len(generated_order) - 1:
                idx1 = generated_order[highlight_index]
                idx2 = generated_order[highlight_index + 1]
                self.ax.arrow(x[idx1], y[idx1],
                              x[idx2] - x[idx1], y[idx2] - y[idx1],
                              head_width=0.05, head_length=0.1,
                              fc='red', ec='red', zorder=2,
                              length_includes_head=True)
        else:
            # Desenăm toate săgețile dacă nu facem animație
            for i in range(len(generated_order) - 1):
                idx1 = generated_order[i]
                idx2 = generated_order[i + 1]
                self.ax.arrow(x[idx1], y[idx1],
                              x[idx2] - x[idx1], y[idx2] - y[idx1],
                              head_width=0.05, head_length=0.1,
                              fc='green', ec='green', zorder=1,
                              length_includes_head=True, alpha=0.6)

            # Conectăm ultimul element cu primul pentru a închide ciclul
            idx1 = generated_order[-1]
            idx2 = generated_order[0]
            self.ax.arrow(x[idx1], y[idx1],
                          x[idx2] - x[idx1], y[idx2] - y[idx1],
                          head_width=0.05, head_length=0.1,
                          fc='green', ec='green', zorder=1,
                          length_includes_head=True, alpha=0.6)

        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_aspect('equal')

        # Actualizăm titlul pentru a include informații despre pasul curent
        if highlight_index is not None and highlight_index < len(generated_values):
            power = highlight_index + 1
            current_val = generated_values[highlight_index]
            self.ax.set_title(f"Generator {generator}: {generator}^{power} mod {n} = {current_val}")
        else:
            self.ax.set_title(f"Vizualizare grup ciclic Z*_{n} cu generator {generator}")

        self.ax.axis('off')
        self.canvas.draw()

    def update_speed_label(self, value):
        speed = int(float(value))
        self.speed_label.config(text=f"{speed} ms")
        self.animation_speed = speed

    def animate_generation(self):
        try:
            # Verificăm dacă avem un generator valid
            if self.current_generator is None:
                messagebox.showinfo("Informație", "Rulați mai întâi 'Calculează' pentru a găsi un generator.")
                return

            # Oprim animația existentă dacă există
            if self.animation:
                self.animation.event_source.stop()

            # Pregătim datele pentru animație
            n = int(self.n_entry.get())
            generator = self.current_generator

            # Elementele relativ prime cu n
            elements = []
            for a in range(1, n):
                if math.gcd(a, n) == 1:
                    elements.append(a)

            # Calculăm indicatorul lui Euler
            phi_n = len(elements)

            # Determinăm ordinea generată de generator
            generated_order = []
            generated_values = []
            for power in range(1, phi_n + 1):
                val = pow(generator, power, n)
                if val in elements:
                    generated_order.append(elements.index(val))
                    generated_values.append(val)

            # Funcția pentru actualizarea animației
            frame_count = len(generated_order)

            def update(frame):
                self.visualize_cyclic_group(n, generator, elements, frame)

                # Actualizăm textul de status
                if frame < len(generated_values):
                    power = frame + 1
                    val = generated_values[frame]
                    self.status_label.config(text=f"Pasul {power}/{phi_n}: {generator}^{power} mod {n} = {val}")

                    # Evidențiem și în textul explicativ
                    self.steps_text.see("1.0")  # Derulează la început
                    self.steps_text.tag_remove("highlight", "1.0", tk.END)

                    # Găsim și evidențiem linia corespunzătoare
                    text_content = self.steps_text.get("1.0", tk.END)
                    search_text = f"{generator}^{power} mod {n} = {val}"
                    start_pos = text_content.find(search_text)

                    if start_pos != -1:
                        end_pos = start_pos + len(search_text)
                        start_line = "1.0 + %d chars" % start_pos
                        end_line = "1.0 + %d chars" % end_pos
                        self.steps_text.tag_add("highlight", start_line, end_line)
                        self.steps_text.tag_config("highlight", background="yellow")

                        # Derulează la poziția text
                        self.steps_text.see(start_line)

            # Creăm animația
            self.animation = FuncAnimation(
                self.fig,
                update,
                frames=frame_count,
                interval=self.animation_speed,
                repeat=False
            )

            # Actualizăm canvas-ul
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare în timpul animației: {str(e)}")

    def explain_algorithm(self):
        explanation = """
Algoritmul pentru găsirea unui generator al unui grup ciclic:

1. Factorizăm ordinul grupului n în factori primi: n = p₁^α₁ · p₂^α₂ · ... · pᵣ^αᵣ

2. Calculăm indicatorul lui Euler φ(n) care reprezintă numărul de elemente din grupul multiplicativ Z*_n:
   - Pentru n = p^k (p prim): φ(n) = p^(k-1) · (p-1)
   - Pentru n = p₁^α₁ · p₂^α₂ · ... · pᵣ^αᵣ: φ(n) = φ(p₁^α₁) · φ(p₂^α₂) · ... · φ(pᵣ^αᵣ)

3. Factorizăm φ(n) în factori primi: φ(n) = q₁^β₁ · q₂^β₂ · ... · qₛ^βₛ

4. Pentru fiecare element a din Z*_n, verificăm dacă este generator:
   - Pentru fiecare factor prim qi al lui φ(n), calculăm b = a^(φ(n)/qi) mod n
   - Dacă pentru orice qi, b ≠ 1, atunci a este generator

5. Dacă a este generator, atunci orice a^k unde gcd(k, φ(n)) = 1 este de asemenea generator.

Un element a este generator al grupului ciclic dacă și numai dacă ordinul său în grup este egal cu φ(n).
        """

        explanation_window = tk.Toplevel(self.root)
        explanation_window.title("Explicație Algoritm")
        explanation_window.geometry("600x500")

        text = scrolledtext.ScrolledText(explanation_window, wrap=tk.WORD, width=70, height=25)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, explanation)
        text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneratorGrupCiclicApp(root)
    root.mainloop()