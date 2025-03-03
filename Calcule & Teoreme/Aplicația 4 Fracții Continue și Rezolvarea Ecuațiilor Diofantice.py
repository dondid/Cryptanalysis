import tkinter as tk
from tkinter import ttk, messagebox


def gcd(a, b):
    steps = []
    while b:
        steps.append(f"{a} = {b} * {a // b} + {a % b}")
        a, b = b, a % b
    return a, steps


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y


def solve_diophantine(a, b, c):
    gcd_val, gcd_steps = gcd(abs(a), abs(b))
    if c % gcd_val != 0:
        return "Nu există soluții", gcd_steps, []

    a, b, c = a // gcd_val, b // gcd_val, c // gcd_val
    gcd_val, x0, y0 = extended_gcd(a, b)
    x0 *= c
    y0 *= c

    solution_steps = [
        f"Împărțim ecuația prin CMMDC ({gcd_val}): {a}x + {b}y = {c}",
        f"Folosim Algoritmul Euclid Extins pentru a găsi soluția particulară:",
        f"x0 = {x0}, y0 = {y0}",
        f"Forma generală: x = {x0} + {b}k, y = {y0} - {a}k"
    ]
    return (x0, y0), gcd_steps, solution_steps


def on_solve():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        c = int(entry_c.get())

        result, gcd_steps, solution_steps = solve_diophantine(a, b, c)
        result_text.delete(1.0, tk.END)

        result_text.insert(tk.END, "CMMDC calculat prin Algoritmul lui Euclid:\n")
        result_text.insert(tk.END, "\n".join(gcd_steps) + "\n\n")

        if isinstance(result, tuple):
            result_text.insert(tk.END, "Rezolvarea ecuației:\n")
            result_text.insert(tk.END, "\n".join(solution_steps) + "\n")
        else:
            result_text.insert(tk.END, result)
    except ValueError:
        messagebox.showerror("Eroare", "Introduceți numere întregi valide!")


# Crearea interfeței grafice
root = tk.Tk()
root.title("Rezolvator Ecuații Diofantice")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

# Titlu
ttk.Label(main_frame, text="Rezolvarea Ecuațiilor Diofantice liniare", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=6, pady=10)

# Descriere
ttk.Label(main_frame, text="Această aplicație rezolvă ecuații diofantice de forma ax + by = c,\n"
                         "unde a, b și c sunt numere întregi.").grid(row=1, column=0, columnspan=6, pady=5)

ttk.Label(main_frame, text="a =").grid(row=2, column=0, padx=5, pady=5)
entry_a = ttk.Entry(main_frame, width=10)
entry_a.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="b =").grid(row=2, column=2, padx=5, pady=5)
entry_b = ttk.Entry(main_frame, width=10)
entry_b.grid(row=2, column=3, padx=5, pady=5)

ttk.Label(main_frame, text="c =").grid(row=2, column=4, padx=5, pady=5)
entry_c = ttk.Entry(main_frame, width=10)
entry_c.grid(row=2, column=5, padx=5, pady=5)

ttk.Button(main_frame, text="Rezolvă Ecuația", command=on_solve).grid(row=3, column=0, columnspan=6, pady=10)

result_text = tk.Text(main_frame, height=20, width=70, wrap=tk.WORD)
result_text.grid(row=4, column=0, columnspan=6, pady=10)

scrollbar = ttk.Scrollbar(main_frame, command=result_text.yview)
scrollbar.grid(row=4, column=6, sticky='ns')
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
