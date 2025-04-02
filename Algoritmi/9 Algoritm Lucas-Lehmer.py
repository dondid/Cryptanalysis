import tkinter as tk
from tkinter import messagebox
import random


def lucas_lehmer_test(n):
    if n < 3:
        return None, ["n trebuie să fie mai mare sau egal cu 3."]

    M_n = 2 ** n - 1
    steps = [f"1. Calculăm numărul Mersenne: M_n = 2^{n} - 1 = {M_n}"]

    s = 4
    steps.append(f"2. Inițializăm șirul: s_0 = 4")

    for k in range(1, n - 1):
        s = (s ** 2 - 2) % M_n
        steps.append(f"{k + 2}. Calculăm: s_{k} = (s_{k - 1}^2 - 2) mod M_n = {s}")

    if s == 0:
        steps.append(f"{len(steps) + 1}. Ultima valoare: s_{n - 2} = 0 -> M_n este prim.")
        return "Prim", steps
    else:
        steps.append(f"{len(steps) + 1}. Ultima valoare: s_{n - 2} ≠ 0 -> M_n este compus.")
        return "Compus", steps


def compute_lucas_lehmer():
    try:
        n = int(entry_n.get())
        result, steps = lucas_lehmer_test(n)
        if result is None:
            messagebox.showerror("Eroare", "Introduceți un n valid (mai mare sau egal cu 3).")
        else:
            lucas_text.delete(1.0, tk.END)
            lucas_text.insert(tk.END, "\n".join(steps))
            messagebox.showinfo("Rezultat", f"Rezultatul testului Lucas-Lehmer: {result}")
    except ValueError:
        messagebox.showerror("Eroare", "Introduceți valori numerice valide.")


def generate_test_data_lucas():
    n = random.choice([3, 5, 7, 13, 17])  # Numere prime pentru n
    entry_n.delete(0, tk.END)
    entry_n.insert(0, str(n))
    messagebox.showinfo("Date de Test", f"Datele generate: n={n}")


# Interfața grafică
root = tk.Tk()
root.title("Testul Lucas-Lehmer pentru Primalitatea Numerelor Mersenne")

# Design culori
root.configure(bg="#e6f7ff")
style_label_bg = "#87ceeb"
style_label_fg = "#000080"
style_button_bg = "#4682b4"
style_button_fg = "white"

# Input utilizator
tk.Label(root, text="n (exponentul Mersenne):", bg=style_label_bg, fg=style_label_fg).grid(row=0, column=0, padx=5,
                                                                                           pady=5)
entry_n = tk.Entry(root)
entry_n.grid(row=0, column=1)

compute_button = tk.Button(root, text="Calculează Lucas-Lehmer", command=compute_lucas_lehmer, bg=style_button_bg,
                           fg=style_button_fg)
compute_button.grid(row=2, column=0, padx=5, pady=5)

generate_button = tk.Button(root, text="Generați Date de Test", command=generate_test_data_lucas, bg=style_button_bg,
                            fg=style_button_fg)
generate_button.grid(row=2, column=1, padx=5, pady=5)

# Afișare calcule pas cu pas
tk.Label(root, text="Pași Testul Lucas-Lehmer:", bg=style_label_bg, fg=style_label_fg).grid(row=3, column=0,
                                                                                            columnspan=2, padx=5,
                                                                                            pady=5)
lucas_text = tk.Text(root, height=20, width=80, bg="#f0f8ff")
lucas_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
