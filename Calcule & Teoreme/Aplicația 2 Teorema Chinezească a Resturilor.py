import tkinter as tk
from tkinter import ttk, messagebox
import math
from functools import reduce

def extended_gcd(a, b):
    """
    Implementează algoritmul lui Euclid extins pentru a calcula
    coeficienții u și v astfel încât au + bv = cmmdc(a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, v, u = extended_gcd(b % a, a)
        return (g, u - (b // a) * v, v)

def mod_inverse(a, m):
    """
    Calculează inversul lui a modulo m
    """
    g, u, v = extended_gcd(a, m)
    if g != 1:
        return None  # Inversul nu există dacă a și m nu sunt prime între ele
    else:
        return (u % m + m) % m  # Asigură că rezultatul este pozitiv

def are_coprime(numbers):
    """
    Verifică dacă toate numerele din listă sunt două câte două prime între ele
    """
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            if math.gcd(numbers[i], numbers[j]) != 1:
                return False, (numbers[i], numbers[j])
    return True, None

def chinese_remainder_theorem(modulii, remainders):
    """
    Implementează Teorema Chinezească a Resturilor pentru a rezolva sistemul de congruențe
    x ≡ remainders[i] (mod modulii[i]) pentru toate i
    """
    # Verificăm dacă modulii sunt doi câte doi primi între ei
    coprime_check, non_coprime_pair = are_coprime(modulii)
    if not coprime_check:
        return None, f"Modulii {non_coprime_pair[0]} și {non_coprime_pair[1]} nu sunt primi între ei"
    
    # Calculăm produsul tuturor modulilor
    M = reduce(lambda a, b: a * b, modulii)
    
    # Calculăm soluția
    result = 0
    steps = []
    
    for i in range(len(modulii)):
        Mi = M // modulii[i]
        Mi_inv = mod_inverse(Mi, modulii[i])
        term = remainders[i] * Mi * Mi_inv
        result += term
        steps.append({
            'b_i': remainders[i],
            'm_i': modulii[i],
            'n_i': Mi,
            'inverse': Mi_inv,
            'term': term,
            'accumulated': result % M
        })
    
    return result % M, steps

def add_modulus_remainder():
    try:
        modulus = int(entry_modulus.get())
        remainder = int(entry_remainder.get())
        
        if modulus < 2:
            messagebox.showerror("Eroare", "Modulul trebuie să fie cel puțin 2.")
            return
        
        list_modulii.insert(tk.END, modulus)
        list_remainders.insert(tk.END, remainder)
        
        entry_modulus.delete(0, tk.END)
        entry_remainder.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Eroare", "Introduceți valori întregi valide.")

def remove_selected():
    selected_indices = list_modulii.curselection()
    if not selected_indices:
        return
    
    # Convertim la listă pentru a putea modifica
    indices = list(selected_indices)
    indices.sort(reverse=True)  # Sortăm descrescător pentru a șterge de la sfârșit
    
    for index in indices:
        list_modulii.delete(index)
        list_remainders.delete(index)

def solve_system():
    modulii = list(map(int, list_modulii.get(0, tk.END)))
    remainders = list(map(int, list_remainders.get(0, tk.END)))
    
    if not modulii:
        messagebox.showerror("Eroare", "Adăugați cel puțin o ecuație în sistem.")
        return
    
    result, steps_or_error = chinese_remainder_theorem(modulii, remainders)
    
    result_text.delete(1.0, tk.END)
    
    if result is None:
        result_text.insert(tk.END, f"Eroare: {steps_or_error}")
        return
    
    # Afișăm sistemul de congruențe
    result_text.insert(tk.END, "Sistemul de congruențe:\n")
    for i in range(len(modulii)):
        result_text.insert(tk.END, f"x ≡ {remainders[i]} (mod {modulii[i]})\n")
    
    # Calculăm produsul modulilor
    M = reduce(lambda a, b: a * b, modulii)
    result_text.insert(tk.END, f"\nProdusul tuturor modulilor: M = {M}\n\n")
    
    # Afișăm pașii de rezolvare
    result_text.insert(tk.END, "Pașii de rezolvare:\n")
    for i, step in enumerate(steps_or_error):
        result_text.insert(tk.END, f"Pasul {i+1}: Pentru x ≡ {step['b_i']} (mod {step['m_i']})\n")
        result_text.insert(tk.END, f"  Calculăm n_{i+1} = M / m_{i+1} = {M} / {step['m_i']} = {step['n_i']}\n")
        result_text.insert(tk.END, f"  Calculăm inversul lui {step['n_i']} modulo {step['m_i']}: {step['inverse']}\n")
        result_text.insert(tk.END, f"  Termen: {step['b_i']} × {step['n_i']} × {step['inverse']} = {step['term']}\n")
        result_text.insert(tk.END, f"  Suma acumulată: {step['accumulated']} (mod {M})\n\n")
    
    # Afișăm soluția finală
    result_text.insert(tk.END, f"Soluția sistemului este x ≡ {result} (mod {M})\n")
    result_text.insert(tk.END, f"Soluția generală: x = {result} + {M}k, unde k ∈ Z\n\n")
    
    # Verificăm soluția
    result_text.insert(tk.END, "Verificare:\n")
    for i in range(len(modulii)):
        verification = result % modulii[i]
        result_text.insert(tk.END, f"{result} ≡ {verification} (mod {modulii[i]})")
        if verification == remainders[i]:
            result_text.insert(tk.END, " ✓\n")
        else:
            result_text.insert(tk.END, " ✗\n")

# Crearea interfeței grafice
root = tk.Tk()
root.title("Teorema Chinezească a Resturilor")
root.geometry("800x700")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Titlu
ttk.Label(main_frame, text="Teorema Chinezească a Resturilor", font=("Arial", 16, "bold")).pack(pady=10)

# Descriere
ttk.Label(main_frame, text="Această aplicație rezolvă sisteme de congruențe de forma x ≡ b_i (mod m_i)\n"
                         "unde modulii m_i sunt doi câte doi primi între ei.").pack(pady=5)

# Frame pentru adăugarea de congruențe
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="x ≡").grid(row=0, column=0, padx=5, pady=5)
entry_remainder = ttk.Entry(input_frame, width=8)
entry_remainder.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="(mod").grid(row=0, column=2, padx=5, pady=5)
entry_modulus = ttk.Entry(input_frame, width=8)
entry_modulus.grid(row=0, column=3, padx=5, pady=5)
ttk.Label(input_frame, text=")").grid(row=0, column=4, padx=0, pady=5)

ttk.Button(input_frame, text="Adaugă", command=add_modulus_remainder).grid(row=0, column=5, padx=10, pady=5)

# Frame pentru afișarea congruențelor
list_frame = ttk.Frame(main_frame)
list_frame.pack(pady=10, fill=tk.X)

# List box pentru modulii
ttk.Label(list_frame, text="Modulii (m_i)").grid(row=0, column=0, padx=5, pady=5)
list_modulii = tk.Listbox(list_frame, width=15, height=6, selectmode=tk.EXTENDED)
list_modulii.grid(row=1, column=0, padx=5, pady=5)

# List box pentru resturi
ttk.Label(list_frame, text="Resturi (b_i)").grid(row=0, column=1, padx=5, pady=5)
list_remainders = tk.Listbox(list_frame, width=15, height=6, selectmode=tk.EXTENDED)
list_remainders.grid(row=1, column=1, padx=5, pady=5)

# Buton pentru eliminarea selecției
ttk.Button(list_frame, text="Elimină selecția", command=remove_selected).grid(row=2, column=0, columnspan=2, pady=5)

# Buton de rezolvare
ttk.Button(main_frame, text="Rezolvă sistemul", command=solve_system).pack(pady=10)

# Text pentru rezultat
result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

ttk.Label(result_frame, text="Soluție:").pack(anchor="w")
result_text = tk.Text(result_frame, height=15, width=80, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True)

# Scrollbar pentru rezultat
scrollbar = ttk.Scrollbar(result_text, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()