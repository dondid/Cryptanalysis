import tkinter as tk
from tkinter import ttk, messagebox
import math

def extended_euclidean(a, b):
    """
    Implementează algoritmul lui Euclid extins pentru a calcula
    coeficienții u și v astfel încât au + bv = cmmdc(a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, v, u = extended_euclidean(b % a, a)
        return (g, u - (b // a) * v, v)

def find_modular_inverse(a, m):
    """
    Calculează inversul lui a modulo m
    """
    g, u, v = extended_euclidean(a, m)
    if g != 1:
        return None  # Inversul nu există dacă a și m nu sunt prime între ele
    else:
        return (u % m + m) % m  # Asigură că rezultatul este pozitiv

def calculate_inverse():
    try:
        a = int(entry_a.get())
        m = int(entry_m.get())
        
        # Verificăm dacă m este cel puțin 2
        if m < 2:
            messagebox.showerror("Eroare", "Modulul m trebuie să fie cel puțin 2.")
            return
        
        # Găsim inversul modular
        inverse = find_modular_inverse(a, m)
        
        # Afișăm procesul de calcul
        g, u, v = extended_euclidean(a, m)
        
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Calculăm inversul lui {a} modulo {m}:\n\n")
        
        # Afișăm pașii algoritmului lui Euclid extins
        result_text.insert(tk.END, "Pașii algoritmului lui Euclid extins:\n")
        
        # Recalculăm pentru a afișa pașii
        a_orig, m_orig = a, m
        steps = []
        while a != 0:
            steps.append((m, a, m // a, m % a))
            m, a = a, m % a
        
        for step in steps:
            result_text.insert(tk.END, f"{step[0]} = {step[1]} × {step[2]} + {step[3]}\n")
        
        if g != 1:
            result_text.insert(tk.END, f"\nCMMDC({a_orig}, {m_orig}) = {g} ≠ 1\n")
            result_text.insert(tk.END, "Inversul modular nu există deoarece numerele nu sunt prime între ele.")
        else:
            result_text.insert(tk.END, f"\nCMMDC({a_orig}, {m_orig}) = 1\n\n")
            result_text.insert(tk.END, f"Din algoritmul Euclid extins avem:\n{g} = {a_orig}·({u}) + {m_orig}·({v})\n\n")
            result_text.insert(tk.END, f"Trecând la congruența modulo {m_orig}:\n")
            result_text.insert(tk.END, f"1 ≡ {a_orig}·({u}) (mod {m_orig})\n\n")
            result_text.insert(tk.END, f"Deci inversul lui {a_orig} modulo {m_orig} este {inverse}")
            
            # Verificare
            verification = (a_orig * inverse) % m_orig
            result_text.insert(tk.END, f"\n\nVerificare: {a_orig} × {inverse} ≡ {verification} (mod {m_orig})")
    except ValueError:
        messagebox.showerror("Eroare", "Introduceți valori întregi valide pentru a și m.")

# Crearea interfeței grafice
root = tk.Tk()
root.title("Inversul Modulo m")
root.geometry("600x500")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Titlu
ttk.Label(main_frame, text="Calculul Inversului Modular", font=("Arial", 16, "bold")).pack(pady=10)

# Descriere
ttk.Label(main_frame, text="Această aplicație calculează inversul lui a modulo m,\nsatisfăcând congruența a·x ≡ 1 (mod m)").pack(pady=5)

# Frame pentru inputs
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="a =").grid(row=0, column=0, padx=5, pady=5)
entry_a = ttk.Entry(input_frame, width=10)
entry_a.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="m =").grid(row=0, column=2, padx=5, pady=5)
entry_m = ttk.Entry(input_frame, width=10)
entry_m.grid(row=0, column=3, padx=5, pady=5)

# Buton de calcul
ttk.Button(main_frame, text="Calculează Inversul", command=calculate_inverse).pack(pady=10)

# Text pentru rezultat
result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

ttk.Label(result_frame, text="Rezultat:").pack(anchor="w")
result_text = tk.Text(result_frame, height=15, width=60, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True)

# Scrollbar pentru rezultat
scrollbar = ttk.Scrollbar(result_text, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()