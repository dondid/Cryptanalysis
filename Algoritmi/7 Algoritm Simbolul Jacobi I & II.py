import tkinter as tk
from tkinter import messagebox
import random


def calc_jacobi(a, n):
    steps1 = []
    steps2 = []

    if n <= 0 or n % 2 == 0:
        return None, steps1, steps2

    result = 1
    a = a % n
    steps1.append("1. Calcul: a = {} (mod {})".format(a, n))

    step_num = 2
    while a != 0:
        while a % 2 == 0:
            a = a // 2
            if n % 8 in [3, 5]:
                result = -result
                steps1.append(
                    "{}. Paritate: a este par -> a = {}, n mod 8 = {}, Rezultat intermediar = {}".format(step_num, a,
                                                                                                         n % 8, result))
            else:
                steps1.append(
                    "{}. Paritate: a este par -> a = {}, n mod 8 = {}, Fără schimbare".format(step_num, a, n % 8))
            step_num += 1

        a, n = n, a
        steps2.append("{}. Schimbare: a = {}, n = {}".format(step_num, a, n))

        if a % 4 == 3 and n % 4 == 3:
            result = -result
            steps2.append(
                "{}. Schimbare de semn: a mod 4 = {}, n mod 4 = {}, Rezultat intermediar = {}".format(step_num, a % 4,
                                                                                                      n % 4, result))
        else:
            steps2.append("{}. Fără schimbare de semn: a mod 4 = {}, n mod 4 = {}".format(step_num, a % 4, n % 4))
        step_num += 1

        a = a % n
        steps2.append("{}. Reducție: a = {} (mod {})".format(step_num, a, n))
        step_num += 1

    return (result if n == 1 else 0), steps1, steps2


def compute():
    try:
        a = int(entry_a.get())
        n = int(entry_n.get())
        result, steps1, steps2 = calc_jacobi(a, n)
        if result is None:
            messagebox.showerror("Eroare", "Introduceți un n valid (impar și pozitiv).")
        else:
            jacobi1_text.delete(1.0, tk.END)
            jacobi2_text.delete(1.0, tk.END)
            jacobi1_text.insert(tk.END, "\n".join(steps1))
            jacobi2_text.insert(tk.END, "\n".join(steps2))
            messagebox.showinfo("Rezultat", f"Simbolul Jacobi ({a}/{n}) este: {result}")
    except ValueError:
        messagebox.showerror("Eroare", "Introduceți valori numerice valide.")


def generate_test_data():
    a = random.randint(1, 100)
    n = random.choice([3, 5, 7, 11, 13, 17, 19, 23])  # Numere impare pozitive
    entry_a.delete(0, tk.END)
    entry_a.insert(0, str(a))
    entry_n.delete(0, tk.END)
    entry_n.insert(0, str(n))
    messagebox.showinfo("Date de Test", f"Datele generate: a={a}, n={n}")


# Interfața grafică
root = tk.Tk()
root.title("Calcul Simbolul Jacobi și Fermat")

# Design culori
root.configure(bg="#f0f8ff")
style_label_bg = "#add8e6"
style_label_fg = "#000080"
style_button_bg = "#4682b4"
style_button_fg = "white"

# Input utilizator
tk.Label(root, text="a:", bg=style_label_bg, fg=style_label_fg).grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

tk.Label(root, text="n:", bg=style_label_bg, fg=style_label_fg).grid(row=1, column=0, padx=5, pady=5)
entry_n = tk.Entry(root)
entry_n.grid(row=1, column=1)

compute_button = tk.Button(root, text="Calculează", command=compute, bg=style_button_bg, fg=style_button_fg)
compute_button.grid(row=2, column=0, padx=5, pady=5)

generate_button = tk.Button(root, text="Generați Date de Test", command=generate_test_data, bg=style_button_bg,
                            fg=style_button_fg)
generate_button.grid(row=2, column=1, padx=5, pady=5)

# Afișare calcule pas cu pas
tk.Label(root, text="Jacobi 1:", bg=style_label_bg, fg=style_label_fg).grid(row=3, column=0, padx=5, pady=5)
jacobi1_text = tk.Text(root, height=10, width=40, bg="#e6e6fa")
jacobi1_text.grid(row=4, column=0, padx=5, pady=5)

tk.Label(root, text="Jacobi 2:", bg=style_label_bg, fg=style_label_fg).grid(row=3, column=1, padx=5, pady=5)
jacobi2_text = tk.Text(root, height=10, width=40, bg="#e6e6fa")
jacobi2_text.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
