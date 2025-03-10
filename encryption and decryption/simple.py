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
                                text="Să se cifreze mesajul 'CRIPTOGRAFIE' folosind cifrul lui Cezar cu cheia de cifrare k = 5.")
        description.pack(padx=10, pady=5)

        # Input/Output frame
        io_frame = ttk.Frame(tab)
        io_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Results area
        result_frame = ttk.LabelFrame(io_frame, text="Solution")
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
                                text="Să se decripteze mesajul 'JAJSN SHJWDU YTQTL DXNQJ SHJNX LTQJJ SXXXX' folosind cifrul lui Cezar. Indicați cheia de cifrare.")
        description.pack(padx=10, pady=5)

        # Input/Output frame
        io_frame = ttk.Frame(tab)
        io_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Results area
        result_frame = ttk.LabelFrame(io_frame, text="Solution")
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

        description = ttk.Label(desc_frame,
                                text="Să se codifice textul 'CRIPTARE' folosind un criptosistem afin cu cheia (5,2).")
        description.pack(padx=10, pady=5)

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

        description = ttk.Label(desc_frame,
                                text="Să se codeze cuvântul 'ATTACK' folosind matricea A = [[3, 5], [1, 2]] și b = [[2], [2]].")
        description.pack(padx=10, pady=5)

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

        description = ttk.Label(desc_frame,
                                text="Folosind matricea A = [[2, 5], [1, 3]] să se codifice mesajul 'CRIPTOGRAFIE'.")
        description.pack(padx=10, pady=5)

        # Results area
        result_frame = ttk.LabelFrame(tab, text="Solution")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.exercise6_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.exercise6_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Solve button
        solve_button = ttk.Button(tab, text="Solve", command=self.solve_exercise6)
        solve_button.pack(pady=10)

    def solve_exercise1(self):
        plaintext = "CRIPTOGRAFIE"
        k = 5
        result = ""

        result += "Exercițiul 1: Cifrarea mesajului 'CRIPTOGRAFIE' folosind cifrul lui Cezar cu k = 5\n\n"
        result += "Formula pentru cifrarea Cezar: E(x) = (x + k) mod 26\n"
        result += "unde x este poziția literei în alfabet (A=0, B=1, ..., Z=25) și k=5 este cheia de cifrare.\n\n"

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

        self.exercise1_result.delete(1.0, tk.END)
        self.exercise1_result.insert(tk.END, result)

    def solve_exercise2(self):
        ciphertext = "JAJSN SHJWDU YTQTL DXNQJ SHJNX LTQJJ SXXXX"
        result = ""

        result += "Exercițiul 2: Decriptarea mesajului cifrat cu cifrul lui Cezar\n\n"
        result += "Formula pentru decriptarea Cezar: D(y) = (y - k) mod 26\n"
        result += "unde y este poziția literei cifrate în alfabet și k este cheia de cifrare.\n\n"

        result += "Pentru a afla cheia, vom încerca toate valorile posibile de la 1 la 25:\n\n"

        most_likely_key = 0
        most_likely_text = ""
        best_score = -1

        # Common letter frequencies in English
        letter_freq = {
            'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3,
            'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
            'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0,
            'K': 0.8, 'J': 0.2, 'X': 0.2, 'Q': 0.1, 'Z': 0.1
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

        self.exercise2_result.delete(1.0, tk.END)
        self.exercise2_result.insert(tk.END, result)

    def solve_exercise3(self):
        plaintext = "CRIPTARE"
        a = 5
        b = 2
        result = ""

        result += "Exercițiul 3: Codificarea textului 'CRIPTARE' folosind un criptosistem afin cu cheia (5,2)\n\n"
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

        self.exercise3_result.delete(1.0, tk.END)
        self.exercise3_result.insert(tk.END, result)

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
                result += "Sistemul nu are soluție unică deoarece gcd(Δ, m) ≠ 1\n"

        except ValueError:
            result = "Eroare: Toate valorile trebuie să fie numere întregi."
        except Exception as e:
            result = f"Eroare: {str(e)}"

        self.exercise4_result.delete(1.0, tk.END)
        self.exercise4_result.insert(tk.END, result)

    def solve_exercise5(self):
        plaintext = "ATTACK"
        # A matrix as given in the exercise
        A = np.array([[3, 5], [1, 2]])
        # b vector as given in the exercise
        b = np.array([[2], [2]])

        result = ""
        result += "Exercițiul 5: Codificarea cuvântului 'ATTACK' folosind cifrul Hill modificat\n\n"
        result += "Formula pentru cifrul Hill modificat: C = A·P + b (mod 26)\n"
        result += "unde:\n- A este matricea cheie: [[3, 5], [1, 2]]\n"
        result += "- b este vectorul de deplasare: [[2], [2]]\n"
        result += "- P este vectorul text clar (perechi de litere)\n"
        result += "- C este vectorul text cifrat\n\n"

        # Check if the matrix is invertible modulo 26
        det = int(np.round(np.linalg.det(A))) % 26
        result += f"Verificăm dacă matricea este inversabilă mod 26:\n"
        result += f"det(A) mod 26 = {det}\n"
        if math.gcd(det, 26) != 1:
            result += "EROARE: Matricea nu este inversabilă modulo 26.\n"
        else:
            result += "Matricea este inversabilă modulo 26.\n\n"

            # Pad the plaintext if needed
            if len(plaintext) % 2 != 0:
                plaintext += 'X'  # Padding with X
                result += "Adăugăm padding cu 'X' pentru a avea un număr par de caractere.\n"

            result += "Cifrare pas cu pas:\n"
            ciphertext = ""

            for i in range(0, len(plaintext), 2):
                # Convert pair of characters to numbers (0-25)
                p1 = ord(plaintext[i].upper()) - ord('A')
                p2 = ord(plaintext[i + 1].upper()) - ord('A')

                p_vector = np.array([[p1], [p2]])

                result += f"Perechea de litere: {plaintext[i]}{plaintext[i + 1]} → [{p1}, {p2}]ᵀ\n"

                # Apply Hill cipher with affine modification
                c_vector = np.dot(A, p_vector) + b
                c_vector = c_vector % 26

                c1 = int(c_vector[0][0])
                c2 = int(c_vector[1][0])

                # Convert back to letters
                c1_char = chr(c1 + ord('A'))
                c2_char = chr(c2 + ord('A'))

                ciphertext += c1_char + c2_char

                result += f"Calcul: A·P + b = [[3, 5], [1, 2]]·[{p1}, {p2}]ᵀ + [[2], [2]] = [{c1}, {c2}]ᵀ\n"
                result += f"Rezultat: {c1_char}{c2_char}\n\n"

            result += f"Textul cifrat: {ciphertext}\n\n"

            result += "Notă: Informația din imagine menționează că se obțin cifrurile panta pentru b = [[0], [0]].\n"
            result += "Dacă folosim b = [[0], [0]] în loc de b = [[2], [2]], rezultatul ar fi:\n\n"

            # Recalculate with b = [[0], [0]]
            b_alt = np.array([[0], [0]])
            ciphertext_alt = ""

            for i in range(0, len(plaintext), 2):
                p1 = ord(plaintext[i].upper()) - ord('A')
                p2 = ord(plaintext[i + 1].upper()) - ord('A')

                p_vector = np.array([[p1], [p2]])

                c_vector = np.dot(A, p_vector) + b_alt
                c_vector = c_vector % 26

                c1 = int(c_vector[0][0])
                c2 = int(c_vector[1][0])

                c1_char = chr(c1 + ord('A'))
                c2_char = chr(c2 + ord('A'))

                ciphertext_alt += c1_char + c2_char

            result += f"Textul cifrat cu b = [[0], [0]]: {ciphertext_alt}"

        self.exercise5_result.delete(1.0, tk.END)
        self.exercise5_result.insert(tk.END, result)

    def solve_exercise6(self):
        plaintext = "CRIPTOGRAFIE"
        # A matrix as given in the exercise
        A = np.array([[2, 5], [1, 3]])

        result = ""
        result += "Exercițiul 6: Codificarea mesajului 'CRIPTOGRAFIE' folosind cifrul Hill\n\n"
        result += "Formula pentru cifrul Hill: C = A·P (mod 26)\n"
        result += "unde:\n- A este matricea cheie: [[2, 5], [1, 3]]\n"
        result += "- P este vectorul text clar (perechi de litere)\n"
        result += "- C este vectorul text cifrat\n\n"

        # Check if the matrix is invertible modulo 26
        det = int(np.round(np.linalg.det(A))) % 26
        result += f"Verificăm dacă matricea este inversabilă mod 26:\n"
        result += f"det(A) mod 26 = {det}\n"
        if math.gcd(det, 26) != 1:
            result += "EROARE: Matricea nu este inversabilă modulo 26.\n"
        else:
            result += "Matricea este inversabilă modulo 26.\n\n"

            # Pad the plaintext if needed
            if len(plaintext) % 2 != 0:
                plaintext += 'X'  # Padding with X
                result += "Adăugăm padding cu 'X' pentru a avea un număr par de caractere.\n"

            result += "Cifrare pas cu pas:\n"
            ciphertext = ""

            for i in range(0, len(plaintext), 2):
                # Convert pair of characters to numbers (0-25)
                p1 = ord(plaintext[i].upper()) - ord('A')
                p2 = ord(plaintext[i + 1].upper()) - ord('A')

                p_vector = np.array([[p1], [p2]])

                result += f"Perechea de litere: {plaintext[i]}{plaintext[i + 1]} → [{p1}, {p2}]ᵀ\n"

                # Apply Hill cipher
                c_vector = np.dot(A, p_vector) % 26

                c1 = int(c_vector[0][0])
                c2 = int(c_vector[1][0])

                # Convert back to letters
                c1_char = chr(c1 + ord('A'))
                c2_char = chr(c2 + ord('A'))

                ciphertext += c1_char + c2_char

                result += f"Calcul: A·P = [[2, 5], [1, 3]]·[{p1}, {p2}]ᵀ = [{c1}, {c2}]ᵀ\n"
                result += f"Rezultat: {c1_char}{c2_char}\n\n"

            result += f"Textul cifrat: {ciphertext}"

        self.exercise6_result.delete(1.0, tk.END)
        self.exercise6_result.insert(tk.END, result)


if __name__ == "__main__":
    # Creăm fereastra principală a aplicației
    root = tk.Tk()

    # Inițializăm aplicația
    app = CryptographyApp(root)

    # Pornim bucla principală a interfeței grafice
    root.mainloop()
