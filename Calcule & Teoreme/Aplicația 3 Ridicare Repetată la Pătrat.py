import tkinter as tk
from tkinter import ttk, messagebox

def decimal_to_binary(n):
    """Convertește un număr din baza 10 în baza 2"""
    if n == 0:
        return "0"

    binary = ""
    while n > 0:
        binary = str(n % 2) + binary
        n //= 2

    return binary

def modular_exponentiation(b, n, m):
    """
    Calculează b^n mod m folosind metoda ridicării repetate la pătrat
    și reducerii modulo m
    """
    if m == 1:
        return 0  # Orice număr mod 1 este 0

    # Convertim exponentul în binar
    binary_n = decimal_to_binary(n)

    # Inițializăm variabilele
    N = 1
    A = b % m
    steps = []

    # Pentru fiecare bit din reprezentarea binară
    for j, bit in enumerate(binary_n):
        if j == 0 and bit == '1':
            N = b % m
            steps.append({
                'j': j,
                'bit': bit,
                'A': A,
                'N': N,
                'explanation': f"Inițializăm N = b mod m = {b} mod {m} = {N}"
            })
        elif j == 0:
            steps.append({
                'j': j,
                'bit': bit,
                'A': A,
                'N': N,
                'explanation': f"Inițializăm N = 1"
            })
        else:
            # Ridicăm A la pătrat
            A = (A * A) % m

            # Dacă bitul curent este 1, actualizăm N
            if bit == '1':
                N = (A * N) % m
                steps.append({
                    'j': j,
                    'bit': bit,
                    'A': A,
                    'N': N,
                    'explanation': f"A = A^2 mod m = {A}, N = A * N mod m = {N}"
                })
            else:
                steps.append({
                    'j': j,
                    'bit': bit,
                    'A': A,
                    'N': N,
                    'explanation': f"A = A^2 mod m = {A}, N rămâne neschimbat"
                })

    return N, steps

def calculate_exponentiation():
    try:
        b = int(entry_b.get())
        n = int(entry_n.get())
        m = int(entry_m.get())

        if n < 0:
            messagebox.showerror("Eroare", "Exponentul trebuie să fie un număr natural.")
            return

        if m < 1:
            messagebox.showerror("Eroare", "Modulul trebuie să fie cel puțin 1.")
            return

        result, steps = modular_exponentiation(b, n, m)

        # Afișăm procesul de calcul
        result_text.delete(1.0, tk.END)

        result_text.insert(tk.END, f"Calculăm {b}^{n} mod {m} folosind metoda ridicării repetate la pătrat\n\n")

        # Afișăm reprezentarea binară a lui n
        binary_n = decimal_to_binary(n)
        result_text.insert(tk.END, f"Exponentul {n} în binar este {binary_n}\n\n")

        # Explicăm metoda
        result_text.insert(tk.END, "Metoda se bazează pe descompunerea exponentului în puteri de 2:\n")
        result_text.insert(tk.END, f"{n} = ")

        # Construim reprezentarea sumei puterilor
        powers = []
        for j, bit in enumerate(reversed(binary_n)):
            if bit == '1':
                powers.append(f"2^{j}")

        result_text.insert(tk.END, " + ".join(powers) + "\n\n")

        result_text.insert(tk.END, f"Astfel, {b}^{n} = ")
        powers_expression = []
        for j, bit in enumerate(reversed(binary_n)):
            if bit == '1':
                powers_expression.append(f"{b}^{2**j}")

        result_text.insert(tk.END, " × ".join(powers_expression) + "\n\n")

        # Afișăm pașii de calcul
        result_text.insert(tk.END, "Pașii de calcul:\n")
        result_text.insert(tk.END, "Inițializăm N = 1 și A = b mod m\n\n")

        for step in steps:
            j = step['j']
            bit = step['bit']
            A = step['A']
            N = step['N']

            result_text.insert(tk.END, f"Pasul {j+1} (bit {j} = {bit}):\n")
            result_text.insert(tk.END, f"  {step['explanation']}\n")
            result_text.insert(tk.END, f"  Acum A = {A} și N = {N}\n\n")

        # Afișăm rezultatul final
        result_text.insert(tk.END, f"Rezultat final: {b}^{n} mod {m} = {result}")

    except ValueError:
        messagebox.showerror("Eroare", "Introduceți valori întregi valide pentru b, n și m.")

def deselect_text(event=None):
    """Elimină selecția textului din câmpul de rezultat"""
    # Verificăm dacă există o selecție
    if result_text.tag_ranges(tk.SEL):
        # Eliminăm selecția
        result_text.tag_remove(tk.SEL, "sel.first", "sel.last")
        # Dezactivăm evidențierea vizuală a selecției
        result_text.mark_unset(tk.SEL_FIRST)
        result_text.mark_unset(tk.SEL_LAST)

# Crearea interfeței grafice
root = tk.Tk()
root.title("Ridicare Repetată la Pătrat")
root.geometry("700x600")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Titlu
ttk.Label(main_frame, text="Calculul b^n mod m prin Ridicare Repetată la Pătrat", font=("Arial", 16, "bold")).pack(pady=10)

# Descriere
ttk.Label(main_frame, text="Această aplicație calculează b^n mod m folosind metoda ridicării repetate la pătrat,\n"
                         "o metodă eficientă pentru valori mari ale lui n și m.").pack(pady=5)

# Frame pentru inputs
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="b =").grid(row=0, column=0, padx=5, pady=5)
entry_b = ttk.Entry(input_frame, width=10)
entry_b.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="n =").grid(row=0, column=2, padx=5, pady=5)
entry_n = ttk.Entry(input_frame, width=10)
entry_n.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(input_frame, text="m =").grid(row=0, column=4, padx=5, pady=5)
entry_m = ttk.Entry(input_frame, width=10)
entry_m.grid(row=0, column=5, padx=5, pady=5)

# Buton de calcul
ttk.Button(main_frame, text="Calculează b^n mod m", command=calculate_exponentiation).pack(pady=10)

# Buton de eliminare a selecției
ttk.Button(main_frame, text="Elimină selecția", command=deselect_text).pack(pady=10)

# Text pentru rezultat
result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

ttk.Label(result_frame, text="Rezultat:").pack(anchor="w")
result_text = tk.Text(result_frame, height=20, width=70, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True)

# Scrollbar pentru rezultat
scrollbar = ttk.Scrollbar(result_text, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Asocierea tastei Escape cu funcția deselect_text
root.bind("<Escape>", deselect_text)

root.mainloop()