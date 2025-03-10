import tkinter as tk
from tkinter import ttk, scrolledtext
import numpy as np
import math

from sympy import Symbol, solve, gcd, mod_inverse


class CryptographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Exercises Solver")
        self.root.geometry("900x700")

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs for each exercise
        self.tabs = []
        for i in range(6):
            tab = ttk.Frame(self.notebook)
            self.tabs.append(tab)
            self.notebook.add(tab, text=f"Exercise {i + 1}")

        # Setup each exercise tab
        self.setup_exercise1()
        self.setup_exercise2()
        self.setup_exercise3()
        self.setup_exercise4()
        self.setup_exercise5()
        self.setup_exercise6()

    def setup_exercise1(self):
        tab = self.tabs[0]

        # Description frame
        desc_frame = ttk.LabelFrame(tab, text="Description")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)

        description = ttk.Label(desc_frame,
                                text="Să se cifreze mesajul folosind cifrul lui Cezar cu cheia de cifrare k.")
        description.pack(padx=10, pady=5)

        # Input frame
        input_frame = ttk.LabelFrame(tab, text="Input")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        input_grid = ttk.Frame(input_frame)
        input_grid.pack(padx=10, pady=5)

        ttk.Label(input_grid, text="Text:").grid(row=0, column=0, padx=5, pady=5)
        self.ex1_text = ttk.Entry(input_grid, width=30)
        self.ex1_text.grid(row=0, column=1, padx=5, pady=5)
        self.ex1_text.insert(0, "CRIPTOGRAFIE")

        ttk.Label(input_grid, text="Cheie (k):").grid(row=0, column=2, padx=5, pady=5)
        self.ex1_key = ttk.Entry(input_grid, width=5)
        self.ex1_key.grid(row=0, column=3, padx=5, pady=5)
        self.ex1_key.insert(0, "5")

        # Results area
        result_frame = ttk.LabelFrame(tab, text="Solution")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.exercise1_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.exercise1_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Solve button
        solve_button = ttk.Button(tab, text="Solve", command=self.solve_exercise1)
        solve_button.pack(pady=10)

    def setup_exercise2(self):
        tab = self.tabs[1]

        # Description frame
        desc_frame = ttk.LabelFrame(tab, text="Description")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)

        description = ttk.Label(desc_frame,
                                text="Să se decripteze mesajul folosind cifrul lui Cezar. Indicați cheia de cifrare.")
        description.pack(padx=10, pady=5)

        # Input frame
        input_frame = ttk.LabelFrame(tab, text="Input")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        input_grid = ttk.Frame(input_frame)
        input_grid.pack(padx=10, pady=5)

        ttk.Label(input_grid, text="Text cifrat:").grid(row=0, column=0, padx=5, pady=5)
        self.ex2_text = ttk.Entry(input_grid, width=50)
        self.ex2_text.grid(row=0, column=1, padx=5, pady=5)
        self.ex2_text.insert(0, "JAJSN SHJWDU YTQTL DXNQJ SHJNX LTQJJ SXXXX")

        # Results area
        result_frame = ttk.LabelFrame(tab, text="Solution")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.exercise2_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.exercise2_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Solve button
        solve_button = ttk.Button(tab, text="Solve", command=self.solve_exercise2)
        solve_button.pack(pady=10)

    def setup_exercise3(self):
        tab = self.tabs[2]

        # Description frame
        desc_frame = ttk.LabelFrame(tab, text="Description")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)

        description = ttk.Label(desc_frame, text="Să se codifice textul folosind un criptosistem afin cu cheia (a,b).")
        description.pack(padx=10, pady=5)

        # Input frame
        input_frame = ttk.LabelFrame(tab, text="Input")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        input_grid = ttk.Frame(input_frame)
        input_grid.pack(padx=10, pady=5)

        ttk.Label(input_grid, text="Text:").grid(row=0, column=0, padx=5, pady=5)
        self.ex3_text = ttk.Entry(input_grid, width=30)
        self.ex3_text.grid(row=0, column=1, padx=5, pady=5)
        self.ex3_text.insert(0, "CRIPTARE")

        ttk.Label(input_grid, text="a:").grid(row=0, column=2, padx=5, pady=5)
        self.ex3_a = ttk.Entry(input_grid, width=5)
        self.ex3_a.grid(row=0, column=3, padx=5, pady=5)
        self.ex3_a.insert(0, "5")

        ttk.Label(input_grid, text="b:").grid(row=0, column=4, padx=5, pady=5)
        self.ex3_b = ttk.Entry(input_grid, width=5)
        self.ex3_b.grid(row=0, column=5, padx=5, pady=5)
        self.ex3_b.insert(0, "2")

        # Results area
        result_frame = ttk.LabelFrame(tab, text="Solution")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.exercise3_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.exercise3_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Solve button
        solve_button = ttk.Button(tab, text="Solve", command=self.solve_exercise3)
        solve_button.pack(pady=10)

    def setup_exercise4(self):
        tab = self.tabs[3]

        # Description frame
        desc_frame = ttk.LabelFrame(tab, text="Description")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)

        description = ttk.Label(desc_frame, text="Rezolvare sistem de două congruențe")
        description.pack(padx=10, pady=5)

        # Input frame
        input_frame = ttk.LabelFrame(tab, text="Input")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Grid for inputs
        input_grid = ttk.Frame(input_frame)
        input_grid.pack(padx=10, pady=5)

        ttk.Label(input_grid, text="a:").grid(row=0, column=0, padx=5, pady=5)
        self.ex4_a = ttk.Entry(input_grid, width=5)
        self.ex4_a.grid(row=0, column=1, padx=5, pady=5)
        self.ex4_a.insert(0, "2")

        ttk.Label(input_grid, text="b:").grid(row=0, column=2, padx=5, pady=5)
        self.ex4_b = ttk.Entry(input_grid, width=5)
        self.ex4_b.grid(row=0, column=3, padx=5, pady=5)
        self.ex4_b.insert(0, "3")

        ttk.Label(input_grid, text="c:").grid(row=0, column=4, padx=5, pady=5)
        self.ex4_c = ttk.Entry(input_grid, width=5)
        self.ex4_c.grid(row=0, column=5, padx=5, pady=5)
        self.ex4_c.insert(0, "4")

        ttk.Label(input_grid, text="d:").grid(row=1, column=0, padx=5, pady=5)
        self.ex4_d = ttk.Entry(input_grid, width=5)
        self.ex4_d.grid(row=1, column=1, padx=5, pady=5)
        self.ex4_d.insert(0, "5")

        ttk.Label(input_grid, text="e:").grid(row=1, column=2, padx=5, pady=5)
        self.ex4_e = ttk.Entry(input_grid, width=5)
        self.ex4_e.grid(row=1, column=3, padx=5, pady=5)
        self.ex4_e.insert(0, "6")

        ttk.Label(input_grid, text="f:").grid(row=1, column=4, padx=5, pady=5)
        self.ex4_f = ttk.Entry(input_grid, width=5)
        self.ex4_f.grid(row=1, column=5, padx=5, pady=5)
        self.ex4_f.insert(0, "7")

        ttk.Label(input_grid, text="m:").grid(row=1, column=6, padx=5, pady=5)
        self.ex4_m = ttk.Entry(input_grid, width=5)
        self.ex4_m.grid(row=1, column=7, padx=5, pady=5)
        self.ex4_m.insert(0, "11")

        # Results area
        result_frame = ttk.LabelFrame(tab, text="Solution")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.exercise4_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.exercise4_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Solve button
        solve_button = ttk.Button(tab, text="Solve", command=self.solve_exercise4)
        solve_button.pack(pady=10)

    def setup_exercise5(self):
        tab = self.tabs[4]

        # Description frame
        desc_frame = ttk.LabelFrame(tab, text="Description")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)

        description = ttk.Label(desc_frame, text="Să se codeze cuvântul folosind matricea A și vectorul b.")
        description.pack(padx=10, pady=5)

        # Input frame
        input_frame = ttk.LabelFrame(tab, text="Input")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        input_grid = ttk.Frame(input_frame)
        input_grid.pack(padx=10, pady=5)

        ttk.Label(input_grid, text="Text:").grid(row=0, column=0, padx=5, pady=5)
        self.ex5_text = ttk.Entry(input_grid, width=30)
        self.ex5_text.grid(row=0, column=1, padx=5, pady=5)
        self.ex5_text.insert(0, "ATTACK")

        # Matrix A inputs
        ttk.Label(input_grid, text="Matrice A:").grid(row=1, column=0, padx=5, pady=5)

        matrix_frame = ttk.Frame(input_grid)
        matrix_frame.grid(row=1, column=1, padx=5, pady=5)

        self.ex5_a11 = ttk.Entry(matrix_frame, width=5)
        self.ex5_a11.grid(row=0, column=0, padx=2, pady=2)
        self.ex5_a11.insert(0, "3")

        self.ex5_a12 = ttk.Entry(matrix_frame, width=5)
        self.ex5_a12.grid(row=0, column=1, padx=2, pady=2)
        self.ex5_a12.insert(0, "5")

        self.ex5_a21 = ttk.Entry(matrix_frame, width=5)
        self.ex5_a21.grid(row=1, column=0, padx=2, pady=2)
        self.ex5_a21.insert(0, "1")

        self.ex5_a22 = ttk.Entry(matrix_frame, width=5)
        self.ex5_a22.grid(row=1, column=1, padx=2, pady=2)
        self.ex5_a22.insert(0, "2")

        # Vector b inputs
        ttk.Label(input_grid, text="Vector b:").grid(row=1, column=2, padx=5, pady=5)

        vector_frame = ttk.Frame(input_grid)
        vector_frame.grid(row=1, column=3, padx=5, pady=5)

        self.ex5_b1 = ttk.Entry(vector_frame, width=5)
        self.ex5_b1.grid(row=0, column=0, padx=2, pady=2)
        self.ex5_b1.insert(0, "2")

        self.ex5_b2 = ttk.Entry(vector_frame, width=5)
        self.ex5_b2.grid(row=1, column=0, padx=2, pady=2)
        self.ex5_b2.insert(0, "2")

        # Results area
        result_frame = ttk.LabelFrame(tab, text="Solution")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.exercise5_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.exercise5_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Solve button
        solve_button = ttk.Button(tab, text="Solve", command=self.solve_exercise5)
        solve_button.pack(pady=10)

    def setup_exercise6(self):
        tab = self.tabs[5]

        # Description frame
        desc_frame = ttk.LabelFrame(tab, text="Description")
        desc_frame.pack(fill=tk.X, padx=10, pady=5)

        description = ttk.Label(desc_frame, text="Folosind matricea A să se codifice mesajul.")
        description.pack(padx=10, pady=5)

        # Input frame
        input_frame = ttk.LabelFrame(tab, text="Input")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        input_grid = ttk.Frame(input_frame)
        input_grid.pack(padx=10, pady=5)

        ttk.Label(input_grid, text="Text:").grid(row=0, column=0, padx=5, pady=5)
        self.ex6_text = ttk.Entry(input_grid, width=30)
        self.ex6_text.grid(row=0, column=1, padx=5, pady=5)
        self.ex6_text.insert(0, "CRIPTOGRAFIE")

        # Matrix A inputs
        ttk.Label(input_grid, text="Matrice A:").grid(row=1, column=0, padx=5, pady=5)

        matrix_frame = ttk.Frame(input_grid)
        matrix_frame.grid(row=1, column=1, padx=5, pady=5)

        self.ex6_a11 = ttk.Entry(matrix_frame, width=5)
        self.ex6_a11.grid(row=0, column=0, padx=2, pady=2)
        self.ex6_a11.insert(0, "2")

        self.ex6_a12 = ttk.Entry(matrix_frame, width=5)
        self.ex6_a12.grid(row=0, column=1, padx=2, pady=2)
        self.ex6_a12.insert(0, "5")

        self.ex6_a21 = ttk.Entry(matrix_frame, width=5)
        self.ex6_a21.grid(row=1, column=0, padx=2, pady=2)
        self.ex6_a21.insert(0, "1")

        self.ex6_a22 = ttk.Entry(matrix_frame, width=5)
        self.ex6_a22.grid(row=1, column=1, padx=2, pady=2)
        self.ex6_a22.insert(0, "3")

        # Results area
        result_frame = ttk.LabelFrame(tab, text="Solution")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.exercise6_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.exercise6_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Solve button
        solve_button = ttk.Button(tab, text="Solve", command=self.solve_exercise6)
        solve_button.pack(pady=10)

    def solve_exercise1(self):
        try:
            plaintext = self.ex1_text.get()
            k = int(self.ex1_key.get())
            result = ""

            result += f"Exercițiul 1: Cifrarea mesajului '{plaintext}' folosind cifrul lui Cezar cu k = {k}\n\n"
            result += "Formula pentru cifrarea Cezar: E(x) = (x + k) mod 26\n"
            result += "unde x este poziția literei în alfabet (A=0, B=1, ..., Z=25) și k este cheia de cifrare.\n\n"

            result += "Cifrare pas cu pas:\n"
            ciphertext = ""

            for i, char in enumerate(plaintext):
                if char.isalpha():
                    # Convert to number (0-25)
                    num = ord(char.upper()) - ord('A')
                    # Apply Caesar cipher
                    encrypted_num = (num + k) % 26
                    # Convert back to letter
                    encrypted_char = chr(encrypted_num + ord('A'))

                    ciphertext += encrypted_char
                    result += f"{char} → poziția {num} → ({num} + {k}) mod 26 = {encrypted_num} → {encrypted_char}\n"
                else:
                    ciphertext += char
                    result += f"{char} (se păstrează neschimbat)\n"

            result += f"\nTextul cifrat: {ciphertext}"

        except ValueError:
            result = "Eroare: Cheia trebuie să fie un număr întreg."
        except Exception as e:
            result = f"Eroare: {str(e)}"

        self.exercise1_result.delete(1.0, tk.END)
        self.exercise1_result.insert(tk.END, result)

    def solve_exercise2(self):
        try:
            ciphertext = self.ex2_text.get()
            result = ""

            result += f"Exercițiul 2: Decriptarea mesajului cifrat cu cifrul lui Cezar\n\n"
            result += "Formula pentru decriptarea Cezar: D(y) = (y - k) mod 26\n"
            result += "unde y este poziția literei cifrate în alfabet și k este cheia de cifrare.\n\n"

            result += "Pentru a afla cheia, vom încerca toate valorile posibile de la 1 la 25:\n\n"

            most_likely_key = 0
            most_likely_text = ""
            best_score = -1

            # Common letter frequencies in Romanian
            letter_freq = {
                'A': 10.5, 'I': 9.8, 'E': 9.7, 'R': 6.6, 'N': 5.3, 'T': 5.0, 'U': 4.8,
                'L': 4.5, 'C': 4.4, 'S': 4.2, 'O': 3.7, 'P': 3.2, 'D': 3.0, 'M': 2.9,
                'V': 2.2, 'F': 1.7, 'B': 1.5, 'G': 1.3, 'H': 1.2, 'Z': 0.9, 'J': 0.2,
                'X': 0.1, 'K': 0.1, 'W': 0.1, 'Y': 0.1, 'Q': 0.1
            }

            for k in range(1, 26):
                plaintext = ""

                for char in ciphertext:
                    if char.isalpha():
                        # Convert to number (0-25)
                        num = ord(char.upper()) - ord('A')
                        # Apply Caesar decryption
                        decrypted_num = (num - k) % 26
                        # Convert back to letter
                        decrypted_char = chr(decrypted_num + ord('A'))
                        plaintext += decrypted_char
                    else:
                        plaintext += char

                # Calculate score based on letter frequency
                score = 0
                for char in plaintext:
                    if char.upper() in letter_freq:
                        score += letter_freq[char.upper()]

                result += f"Cheia k={k}: {plaintext}\n"

                if score > best_score:
                    best_score = score
                    most_likely_key = k
                    most_likely_text = plaintext

            result += f"\nCea mai probabilă cheie este k={most_likely_key}, rezultând textul:\n{most_likely_text}\n"
            result += f"\nFormula aplicată: D(y) = (y - {most_likely_key}) mod 26"

        except Exception as e:
            result = f"Eroare: {str(e)}"

        self.exercise2_result.delete(1.0, tk.END)
        self.exercise2_result.insert(tk.END, result)

    def solve_exercise3(self):
        try:
            plaintext = self.ex3_text.get()
            a = int(self.ex3_a.get())
            b = int(self.ex3_b.get())
            result = ""

            result += f"Exercițiul 3: Codificarea textului '{plaintext}' folosind un criptosistem afin cu cheia ({a},{b})\n\n"
            result += "Formula pentru cifrarea afină: E(x) = (a·x + b) mod 26\n"
            result += f"unde a={a}, b={b} și x este poziția literei în alfabet (A=0, B=1, ..., Z=25).\n\n"

            # Check if 'a' is valid (gcd(a, 26) = 1)
            if math.gcd(a, 26) != 1:
                result += f"EROARE: Valoarea a={a} nu este validă pentru cifrul afin.\n"
                result += "Pentru cifrarea afină, a trebuie să fie relativ prim cu 26 (gcd(a, 26) = 1).\n"
            else:
                result += "Pentru ca cifrul afin să fie valid, gcd(a, 26) trebuie să fie 1.\n"
                result += f"gcd({a}, 26) = {math.gcd(a, 26)}, deci cheia este validă.\n\n"

                result += "Cifrare pas cu pas:\n"
                ciphertext = ""

                for i, char in enumerate(plaintext):
                    if char.isalpha():
                        # Convert to number (0-25)
                        num = ord(char.upper()) - ord('A')

                        # Apply affine cipher
                        encrypted_num = (a * num + b) % 26

                        # Convert back to letter
                        encrypted_char = chr(encrypted_num + ord('A'))

                        ciphertext += encrypted_char
                        result += f"{char} → poziția {num} → ({a}·{num} + {b}) mod 26 = {encrypted_num} → {encrypted_char}\n"
                    else:
                        ciphertext += char
                        result += f"{char} (se păstrează neschimbat)\n"

                result += f"\nTextul cifrat: {ciphertext}"

        except ValueError:
            result = "Eroare: Valorile a și b trebuie să fie numere întregi."
        except Exception as e:
            result = f"Eroare: {str(e)}"

        self.exercise3_result.delete(1.0, tk.END)
        self.exercise3_result.insert(tk.END, result)

    # In the solve_exercise4 method, fix the else block
    def solve_exercise4(self):
        try:
            a = int(self.ex4_a.get())
            b = int(self.ex4_b.get())
            c = int(self.ex4_c.get())
            d = int(self.ex4_d.get())
            e = int(self.ex4_e.get())
            f = int(self.ex4_f.get())
            m = int(self.ex4_m.get())

            result = ""
            result += "Exercițiul 4: Rezolvare sistem de două congruențe\n\n"
            result += "Sistemul de congruențe:\n"
            result += f"ax + by ≡ c (mod m)\n"
            result += f"dx + ey ≡ f (mod m)\n\n"
            result += f"Cu valorile: a={a}, b={b}, c={c}, d={d}, e={e}, f={f}, m={m}\n\n"

            # Step 1: Calculate Δ = ad - bc
            delta = a * e - b * d
            result += f"Pasul 1: Calculăm Δ = a·e - b·d = {a}·{e} - {b}·{d} = {delta}\n\n"

            # Step 2: Check if gcd(Δ, m) = 1
            delta_m_gcd = math.gcd(delta, m)
            result += f"Pasul 2: Verificăm dacă gcd(Δ, m) = 1\n"
            result += f"gcd({delta}, {m}) = {delta_m_gcd}\n\n"

            if delta_m_gcd == 1:
                # Step 3: Calculate delta_inverse modulo m
                delta_inv = pow(delta, -1, m)
                result += f"Pasul 3: Calculăm inversul lui Δ modulo m\n"
                result += f"Δ⁻¹ mod {m} = {delta_inv}\n\n"

                # Step 4: Calculate x and y
                x = (delta_inv * (e * c - b * f)) % m
                y = (delta_inv * (a * f - d * c)) % m

                result += f"Pasul 4: Calculăm x și y\n"
                result += f"x = Δ⁻¹·(e·c - b·f) mod m = {delta_inv}·({e}·{c} - {b}·{f}) mod {m} = {x}\n"
                result += f"y = Δ⁻¹·(a·f - d·c) mod m = {delta_inv}·({a}·{f} - {d}·{c}) mod {m} = {y}\n\n"

                result += f"Soluția sistemului: x = {x}, y = {y}\n"

                # Verification
                result += "\nVerificare:\n"
                eq1 = (a * x + b * y) % m
                eq2 = (d * x + e * y) % m
                result += f"a·x + b·y ≡ {a}·{x} + {b}·{y} ≡ {eq1} ≡ {c} (mod {m})\n"
                result += f"d·x + e·y ≡ {d}·{x} + {e}·{y} ≡ {eq2} ≡ {f} (mod {m})\n"
            else:
                result += "Sistemul nu are soluție unică deoarece gcd(Δ, m) ≠ 1.\n"

                # Check if the system has any solutions
                if delta_m_gcd != 0 and (c % delta_m_gcd == 0) and (f % delta_m_gcd == 0):
                    result += "Sistemul are multiple soluții.\n"

                    # Solve the reduced system
                    a_prime = a // delta_m_gcd
                    b_prime = b // delta_m_gcd
                    c_prime = c // delta_m_gcd
                    d_prime = d // delta_m_gcd
                    e_prime = e // delta_m_gcd
                    f_prime = f // delta_m_gcd
                    m_prime = m // delta_m_gcd

                    result += f"Rezolvăm sistemul redus cu: a'={a_prime}, b'={b_prime}, c'={c_prime}, d'={d_prime}, e'={e_prime}, f'={f_prime}, m'={m_prime}\n"
                else:
                    result += "Sistemul nu are soluții deoarece valorile c și f nu sunt divizibile cu gcd(Δ, m).\n"

        except ValueError:
            result = "Eroare: Valorile trebuie să fie numere întregi."
        except Exception as e:
            result = f"Eroare: {str(e)}"

        self.exercise4_result.delete(1.0, tk.END)
        self.exercise4_result.insert(tk.END, result)

    def solve_exercise5(self):
        try:
            plaintext = self.ex5_text.get().upper()

            # Get matrix A values
            a11 = int(self.ex5_a11.get())
            a12 = int(self.ex5_a12.get())
            a21 = int(self.ex5_a21.get())
            a22 = int(self.ex5_a22.get())

            # Get vector b values
            b1 = int(self.ex5_b1.get())
            b2 = int(self.ex5_b2.get())

            result = ""
            result += f"Exercițiul 5: Codarea cuvântului '{plaintext}' folosind matricea A și vectorul b\n\n"

            # Define matrix A and vector b
            A = np.array([[a11, a12], [a21, a22]])
            b = np.array([b1, b2])

            result += "Matricea A:\n"
            result += f"A = [{a11} {a12}]\n"
            result += f"    [{a21} {a22}]\n\n"

            result += f"Vectorul b = [{b1}, {b2}]\n\n"

            # If odd length, add padding
            if len(plaintext) % 2 != 0:
                plaintext += 'X'
                result += "Adăugăm un 'X' pentru a avea un număr par de caractere.\n\n"

            result += "Codare pas cu pas:\n"
            ciphertext = ""

            for i in range(0, len(plaintext), 2):
                if i + 1 < len(plaintext):
                    # Convert pair of letters to numbers (0-25)
                    x1 = ord(plaintext[i]) - ord('A')
                    x2 = ord(plaintext[i + 1]) - ord('A')

                    x = np.array([x1, x2])

                    # Apply Hill cipher formula: y = Ax + b mod 26
                    y = (np.dot(A, x) + b) % 26

                    # Convert back to letters
                    y1_char = chr(int(y[0]) + ord('A'))
                    y2_char = chr(int(y[1]) + ord('A'))

                    ciphertext += y1_char + y2_char

                    result += f"Perechea '{plaintext[i]}{plaintext[i + 1]}' → [{x1}, {x2}]\n"
                    result += f"y = A·x + b = [{a11} {a12}]·[{x1}] + [{b1}] mod 26 = "
                    result += f"[{int(y[0])}] → {y1_char}\n"
                    result += f"              [{a21} {a22}] [{x2}]   [{b2}]        "
                    result += f"[{int(y[1])}] → {y2_char}\n\n"

            result += f"Textul cifrat: {ciphertext}"

        except ValueError:
            result = "Eroare: Valorile matricei și vectorului trebuie să fie numere întregi."
        except Exception as e:
            result = f"Eroare: {str(e)}"

        self.exercise5_result.delete(1.0, tk.END)
        self.exercise5_result.insert(tk.END, result)

    def solve_exercise6(self):
        try:
            plaintext = self.ex6_text.get().upper()

            # Get matrix A values
            a11 = int(self.ex6_a11.get())
            a12 = int(self.ex6_a12.get())
            a21 = int(self.ex6_a21.get())
            a22 = int(self.ex6_a22.get())

            result = ""
            result += f"Exercițiul 6: Codarea mesajului '{plaintext}' folosind matricea A\n\n"

            # Define matrix A
            A = np.array([[a11, a12], [a21, a22]])

            result += "Matricea A:\n"
            result += f"A = [{a11} {a12}]\n"
            result += f"    [{a21} {a22}]\n\n"

            # Check if matrix is invertible (det != 0 mod 26)
            det = (a11 * a22 - a12 * a21) % 26
            if math.gcd(det, 26) != 1:
                result += f"AVERTISMENT: Matricea A nu este invertibilă modulo 26 (det(A) = {det}, gcd({det}, 26) ≠ 1).\n"
                result += "Acest lucru va face imposibilă decriptarea corectă.\n\n"

            # If odd length, add padding
            if len(plaintext) % 2 != 0:
                plaintext += 'X'
                result += "Adăugăm un 'X' pentru a avea un număr par de caractere.\n\n"

            result += "Codare pas cu pas:\n"
            ciphertext = ""

            for i in range(0, len(plaintext), 2):
                if i + 1 < len(plaintext):
                    # Convert pair of letters to numbers (0-25)
                    x1 = ord(plaintext[i]) - ord('A')
                    x2 = ord(plaintext[i + 1]) - ord('A')

                    x = np.array([x1, x2])

                    # Apply Hill cipher formula: y = Ax mod 26
                    y = np.dot(A, x) % 26

                    # Convert back to letters
                    y1_char = chr(int(y[0]) + ord('A'))
                    y2_char = chr(int(y[1]) + ord('A'))

                    ciphertext += y1_char + y2_char

                    result += f"Perechea '{plaintext[i]}{plaintext[i + 1]}' → [{x1}, {x2}]\n"
                    result += f"y = A·x = [{a11} {a12}]·[{x1}] mod 26 = "
                    result += f"[{int(y[0])}] → {y1_char}\n"
                    result += f"         [{a21} {a22}] [{x2}]           "
                    result += f"[{int(y[1])}] → {y2_char}\n\n"

            result += f"Textul cifrat: {ciphertext}"

        except ValueError:
            result = "Eroare: Valorile matricei trebuie să fie numere întregi."
        except Exception as e:
            result = f"Eroare: {str(e)}"

        self.exercise6_result.delete(1.0, tk.END)
        self.exercise6_result.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptographyApp(root)  # This line uses the class
    root.mainloop()
