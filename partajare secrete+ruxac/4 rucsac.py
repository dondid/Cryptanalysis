import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SubsetSumSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Rezolvare Problema Sumei Submulțimii")
        self.root.geometry("800x700")

        # Frame pentru date de intrare
        input_frame = ttk.LabelFrame(root, text="Date de intrare")
        input_frame.pack(padx=10, pady=10, fill="x")

        # Mulțimea de numere
        ttk.Label(input_frame, text="Mulțimea de numere (separate prin virgulă):").grid(row=0, column=0, sticky="w",
                                                                                        padx=5, pady=5)
        self.numbers_entry = ttk.Entry(input_frame, width=50)
        self.numbers_entry.grid(row=0, column=1, padx=5, pady=5)
        self.numbers_entry.insert(0, "7, 3, 2, 5, 8")  # Exemplu presetat

        # Suma dorită
        ttk.Label(input_frame, text="Suma dorită (S):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.target_entry = ttk.Entry(input_frame, width=50)
        self.target_entry.grid(row=1, column=1, padx=5, pady=5)
        self.target_entry.insert(0, "10")  # Exemplu presetat

        # Buton pentru rezolvare
        solve_button = ttk.Button(input_frame, text="Rezolvă problema", command=self.solve)
        solve_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame pentru problemă
        problem_frame = ttk.LabelFrame(root, text="Problema")
        problem_frame.pack(padx=10, pady=5, fill="x")

        problem_text = "Considerăm {a₁, a₂, ..., aₙ} o mulțime de numere naturale\n"
        problem_text += "S un număr natural.\n"
        problem_text += "Să se determine dacă există xᵢ ∈ {0,1}, 1 ≤ i ≤ n, pentru care:\n"
        problem_text += "∑(xᵢ·aᵢ) = S"

        problem_label = ttk.Label(problem_frame, text=problem_text, justify="left")
        problem_label.pack(padx=5, pady=5)

        # Frame pentru output
        output_frame = ttk.LabelFrame(root, text="Rezultat și explicație")
        output_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Text pentru output
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=70, height=15)
        self.output_text.pack(padx=5, pady=5, fill="both", expand=True)

        # Frame pentru vizualizare
        viz_frame = ttk.LabelFrame(root, text="Vizualizare")
        viz_frame.pack(padx=10, pady=5, fill="both")

        # Crearea figurii Matplotlib
        self.figure = Figure(figsize=(6, 2), dpi=100)
        self.subplot = self.figure.add_subplot(111)

        # Canvas pentru grafic
        self.canvas = FigureCanvasTkAgg(self.figure, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Butoane pentru navigare
        nav_frame = ttk.Frame(root)
        nav_frame.pack(padx=10, pady=5, fill="x")

        self.prev_button = ttk.Button(nav_frame, text="Pasul anterior", command=self.prev_step, state="disabled")
        self.prev_button.pack(side="left", padx=5)

        self.next_button = ttk.Button(nav_frame, text="Pasul următor", command=self.next_step, state="disabled")
        self.next_button.pack(side="right", padx=5)

        self.step_label = ttk.Label(nav_frame, text="Pas: 0/0")
        self.step_label.pack(side="top", padx=5)

        # Variabile pentru pași
        self.steps = []
        self.current_step = 0
        self.solution = None

    def solve(self):
        # Curățarea rezultatelor anterioare
        self.output_text.delete(1.0, tk.END)
        self.steps = []
        self.current_step = 0

        # Obținerea datelor de intrare
        try:
            numbers = [int(x.strip()) for x in self.numbers_entry.get().split(",")]
            target = int(self.target_entry.get())

            if any(x <= 0 for x in numbers) or target <= 0:
                self.output_text.insert(tk.END, "Toate numerele trebuie să fie naturale (> 0).\n")
                return
        except ValueError:
            self.output_text.insert(tk.END,
                                    "Date de intrare invalide. Asigură-te că ai introdus numere întregi separate prin virgulă și o valoare întreagă pentru S.\n")
            return

        # Adăugarea pașilor explicativi
        self.steps.append({
            "text": f"Avem mulțimea de numere: {numbers}\nȘi căutăm o submulțime cu suma: {target}\n\n"
                    f"Problema matematică:\nSă se determine dacă există xi ∈ {{0,1}}, pentru care suma ∑(xi·ai) = {target}",
            "solution": None
        })

        self.steps.append({
            "text": "Pentru a rezolva problema, vom folosi programare dinamică.\n\n"
                    "Definim dp[i][j] = TRUE dacă putem obține suma j folosind primele i elemente din mulțime,\n"
                    "și dp[i][j] = FALSE în caz contrar.",
            "solution": None
        })

        # Rezolvarea propriu-zisă folosind programare dinamică
        n = len(numbers)
        # Creăm matricea dp
        dp = np.zeros((n + 1, target + 1), dtype=bool)

        # Cazul de bază: putem forma suma 0 fără să folosim niciun element
        dp[0][0] = True

        # Construirea matricei dp
        for i in range(1, n + 1):
            dp[i][0] = True  # Întotdeauna putem forma suma 0
            for j in range(1, target + 1):
                if j < numbers[i - 1]:
                    # Dacă numărul curent este mai mare decât suma, nu-l putem include
                    dp[i][j] = dp[i - 1][j]
                else:
                    # Putem fie să includem numărul curent, fie să-l excludem
                    dp[i][j] = dp[i - 1][j] or dp[i - 1][j - numbers[i - 1]]

        # Adăugăm pas explicativ pentru construirea tabelului
        self.steps.append({
            "text": "Construim tabelul de programare dinamică:\n"
                    "Fiecare celulă dp[i][j] ne spune dacă putem obține suma j folosind primele i elemente.",
            "solution": {"dp": dp, "numbers": numbers, "target": target}
        })

        # Verificăm dacă există soluție
        if not dp[n][target]:
            self.steps.append({
                "text": f"Nu există o submulțime care să aibă suma {target}.",
                "solution": None
            })
        else:
            # Reconstituim soluția
            solution = [0] * n
            i, j = n, target

            while i > 0 and j > 0:
                if dp[i - 1][j] == False:
                    # Trebuie să folosim elementul i
                    solution[i - 1] = 1
                    j -= numbers[i - 1]
                i -= 1

            # Adăugăm pași explicativi pentru soluție
            selected = [numbers[i] for i in range(n) if solution[i] == 1]

            self.steps.append({
                "text": f"Am găsit o soluție! Putem forma suma {target} folosind submulțimea {selected}.\n\n"
                        f"Verificare: {' + '.join(map(str, selected))} = {sum(selected)}",
                "solution": {"solution": solution, "numbers": numbers, "selected": selected}
            })

            # Interpretare matematică
            interpretation = ' + '.join([f"{solution[i]}×{numbers[i]}" for i in range(n)])
            self.steps.append({
                "text": f"În notația matematică din problemă:\n{interpretation} = {target}\n\n"
                        f"Deci, valorile xi ∈ {{0,1}} care satisfac condiția ∑(xi·ai) = {target} sunt:\n"
                        f"{', '.join([f'x{i + 1} = {solution[i]}' for i in range(n)])}",
                "solution": {"solution": solution, "numbers": numbers, "selected": selected}
            })

            self.solution = solution

        # Afișăm primul pas
        self.show_step(0)

        # Activăm/dezactivăm butoanele de navigare
        self.update_navigation_buttons()

    def show_step(self, step_index):
        if not self.steps or step_index < 0 or step_index >= len(self.steps):
            return

        self.current_step = step_index
        step_data = self.steps[step_index]

        # Actualizăm textul
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, step_data["text"])

        # Curățăm figura existentă
        self.subplot.clear()

        # Vizualizare în funcție de tipul pasului
        if step_data["solution"]:
            if "dp" in step_data["solution"]:
                # Vizualizăm matricea dp
                dp = step_data["solution"]["dp"]
                numbers = step_data["solution"]["numbers"]
                target = step_data["solution"]["target"]

                # Afișăm doar o porțiune relevantă a matricei pentru claritate
                n = len(numbers)
                max_rows = min(n + 1, 10)  # Limităm la 10 rânduri pentru claritate
                max_cols = min(target + 1, 15)  # Limităm la 15 coloane pentru claritate

                # Creăm o imagine a tabelului (o parte din el)
                table = dp[:max_rows, :max_cols]

                # Afișăm tabelul ca o imagine
                im = self.subplot.imshow(table, cmap='coolwarm', interpolation='nearest')

                # Adăugăm etichetele axelor
                row_labels = ["∅"] + [str(numbers[i]) for i in range(min(n, max_rows - 1))]
                col_labels = [str(j) for j in range(max_cols)]

                # Adăugăm etichetele axelor
                self.subplot.set_xticks(range(max_cols))
                self.subplot.set_yticks(range(max_rows))
                self.subplot.set_xticklabels(col_labels)
                self.subplot.set_yticklabels(row_labels)

                # Adăugăm titlul și etichetele axelor
                self.subplot.set_title("Tabel Programare Dinamică (parțial)")
                self.subplot.set_xlabel("Suma j")
                self.subplot.set_ylabel("Primele i elemente")

                # Adăugăm o bară de culoare pentru interpretarea valorilor True/False
                self.figure.colorbar(im, label="True/False", ticks=[0, 1])

            elif "solution" in step_data["solution"]:
                # Vizualizăm soluția
                solution = step_data["solution"]["solution"]
                numbers = step_data["solution"]["numbers"]
                selected = step_data["solution"]["selected"]

                # Creăm un grafic de bare pentru vizualizarea soluției
                x = range(len(numbers))
                self.subplot.bar(x, numbers,
                                 color=['red' if solution[i] == 0 else 'green' for i in range(len(numbers))])

                # Adăugăm etichetele numerelor
                for i, val in enumerate(numbers):
                    color = 'white' if solution[i] == 1 else 'black'
                    self.subplot.text(i, val / 2, str(val), ha='center', va='center', color=color)

                # Adăugăm titlul și etichetele axelor
                self.subplot.set_title(f"Soluție: Submulțime cu suma {sum(selected)}")
                self.subplot.set_xlabel("Indice element")
                self.subplot.set_ylabel("Valoare")
                self.subplot.set_xticks(x)
                self.subplot.set_xticklabels([f"a{i + 1}" for i in range(len(numbers))])

                # Adăugăm o legendă pentru interpretarea culorilor
                from matplotlib.patches import Patch
                legend_elements = [
                    Patch(facecolor='green', label='Selectat (xi=1)'),
                    Patch(facecolor='red', label='Neselectat (xi=0)')
                ]
                self.subplot.legend(handles=legend_elements)

        # Actualizăm canvas-ul
        self.figure.tight_layout()
        self.canvas.draw()

        # Actualizăm eticheta pasului
        self.step_label.config(text=f"Pas: {step_index + 1}/{len(self.steps)}")

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.show_step(self.current_step + 1)
            self.update_navigation_buttons()

    def prev_step(self):
        if self.current_step > 0:
            self.show_step(self.current_step - 1)
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        # Activăm/dezactivăm butoanele de navigare în funcție de pasul curent
        if self.current_step == 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")

        if self.current_step == len(self.steps) - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = SubsetSumSolver(root)
    root.mainloop()