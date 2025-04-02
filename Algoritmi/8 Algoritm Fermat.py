import tkinter as tk
from tkinter import messagebox
import random


def fermat_test(n, t):
    steps = []
    is_composite = False
    steps.append(f"1. Numărul de intrare: n = {n}, t = {t}")

    for i in range(1, t + 1):
        b = random.randint(2, n - 2)
        steps.append(f"{i + 1}. Test #{i}: Aleg aleator b = {b}")
        r = pow(b, n - 1, n)
        steps.append(f"  - Calculez: {b}^({n}-1) mod {n} = {r}")
        if r != 1:
            steps.append(f"  - r ≠ 1 -> n este compus.")
            is_composite = True
            break
        else:
            steps.append(f"  - r = 1 -> Continuăm testul.")

    if not is_composite:
        steps.append(f"{len(steps) + 1}. Toate testele au trecut -> n este probabil prim.")

    return "Prim" if not is_composite else "Compus", steps


def compute_fermat():
    try:
        n = int(entry_n.get())
        t = int(entry_t.get())
        if n <= 2 or n % 2 == 0:
            messagebox.showerror("Eroare", "Introduceți un n valid (impar și mai mare decât 2).")
        elif t < 1:
            messagebox.showerror("Eroare", "Introduceți un t valid (mai mare decât 0).")
        else:
            result, steps = fermat_test(n, t)
            fermat_text.delete(1.0, tk.END)
            fermat_text.insert(tk.END, "\n".join(steps))
            messagebox.showinfo("Rezultat", f"Rezultatul testului Fermat: {result}")
    except ValueError:
        messagebox.showerror("Eroare", "Introduceți valori numerice valide.")


def generate_test_data_fermat():
    n = random.choice([11, 13, 17, 19, 23, 29, 31])  # Numere prime posibile
    t = random.randint(2, 5)  # Număr de teste
    entry_n.delete(0, tk.END)
    entry_n.insert(0, str(n))
    entry_t.delete(0, tk.END)
    entry_t.insert(0, str(t))
    messagebox.showinfo("Date de Test", f"Datele generate: n={n}, t={t}")


# Interfața grafică
root = tk.Tk()
root.title("Testul Fermat pentru Primalitate")

# Design culori
root.configure(bg="#f5f5f5")
style_label_bg = "#f08080"
style_label_fg = "#800000"
style_button_bg = "#ff6347"
style_button_fg = "white"

# Input utilizator
tk.Label(root, text="n (număr de testat):", bg=style_label_bg, fg=style_label_fg).grid(row=0, column=0, padx=5, pady=5)
entry_n = tk.Entry(root)
entry_n.grid(row=0, column=1)

tk.Label(root, text="t (număr teste):", bg=style_label_bg, fg=style_label_fg).grid(row=1, column=0, padx=5, pady=5)
entry_t = tk.Entry(root)
entry_t.grid(row=1, column=1)

compute_button = tk.Button(root, text="Calculează Fermat", command=compute_fermat, bg=style_button_bg,
                           fg=style_button_fg)
compute_button.grid(row=2, column=0, padx=5, pady=5)

generate_button = tk.Button(root, text="Generați Date de Test", command=generate_test_data_fermat, bg=style_button_bg,
                            fg=style_button_fg)
generate_button.grid(row=2, column=1, padx=5, pady=5)

# Afișare calcule pas cu pas
tk.Label(root, text="Pași Testul Fermat:", bg=style_label_bg, fg=style_label_fg).grid(row=3, column=0, columnspan=2,
                                                                                      padx=5, pady=5)
fermat_text = tk.Text(root, height=20, width=80, bg="#ffe4e1")
fermat_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
