import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math


class CryptographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicația de Criptografie - RSA și Number Theory")
        self.root.geometry("1000x800")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1 - Problem 1 (RSA)
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Problema 1 - RSA")

        # Tab 2 - Problem 2 (Number Theory)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Problema 2 - Number Theory")

        self.setup_tab1()
        self.setup_tab2()

    def setup_tab1(self):
        """Setup pentru Problema 1 - RSA"""
        # Input frame
        input_frame = ttk.LabelFrame(self.tab1, text="Parametri de intrare")
        input_frame.pack(fill='x', padx=10, pady=5)

        # M input
        ttk.Label(input_frame, text="M (mesaj):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.m_var = tk.StringVar(value="101")
        ttk.Entry(input_frame, textvariable=self.m_var, width=15).grid(row=0, column=1, padx=5, pady=2)

        # p input
        ttk.Label(input_frame, text="p (număr prim):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.p_var = tk.StringVar(value="11")
        ttk.Entry(input_frame, textvariable=self.p_var, width=15).grid(row=0, column=3, padx=5, pady=2)

        # q input
        ttk.Label(input_frame, text="q (număr prim):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.q_var = tk.StringVar(value="17")
        ttk.Entry(input_frame, textvariable=self.q_var, width=15).grid(row=1, column=1, padx=5, pady=2)

        # n input
        ttk.Label(input_frame, text="n (p*q):").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.n_var = tk.StringVar(value="187")
        ttk.Entry(input_frame, textvariable=self.n_var, width=15).grid(row=1, column=3, padx=5, pady=2)

        # Calculate button
        ttk.Button(input_frame, text="Calculează Problema 1",
                   command=self.solve_problem1).grid(row=2, column=0, columnspan=4, pady=10)

        # Results
        self.result1_text = scrolledtext.ScrolledText(self.tab1, height=25, width=100)
        self.result1_text.pack(fill='both', expand=True, padx=10, pady=5)

    def setup_tab2(self):
        """Setup pentru Problema 2 - Number Theory"""
        # Input frame
        input_frame = ttk.LabelFrame(self.tab2, text="Parametri de intrare")
        input_frame.pack(fill='x', padx=10, pady=5)

        # p input
        ttk.Label(input_frame, text="p (număr prim):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.p2_var = tk.StringVar(value="15121")
        ttk.Entry(input_frame, textvariable=self.p2_var, width=15).grid(row=0, column=1, padx=5, pady=2)

        # q input
        ttk.Label(input_frame, text="q (număr prim):").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.q2_var = tk.StringVar(value="15131")
        ttk.Entry(input_frame, textvariable=self.q2_var, width=15).grid(row=0, column=3, padx=5, pady=2)

        # n input
        ttk.Label(input_frame, text="n (calculat automat):").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.n2_label = ttk.Label(input_frame, text="228795851")
        self.n2_label.grid(row=1, column=1, padx=5, pady=2)

        # a input
        ttk.Label(input_frame, text="a (pentru decriptare):").grid(row=1, column=2, sticky='w', padx=5, pady=2)
        self.a_var = tk.StringVar(value="223043599")
        ttk.Entry(input_frame, textvariable=self.a_var, width=15).grid(row=1, column=3, padx=5, pady=2)

        # Calculate button
        ttk.Button(input_frame, text="Calculează Problema 2",
                   command=self.solve_problem2).grid(row=2, column=0, columnspan=4, pady=10)

        # Results
        self.result2_text = scrolledtext.ScrolledText(self.tab2, height=25, width=100)
        self.result2_text.pack(fill='both', expand=True, padx=10, pady=5)

    def gcd_extended(self, a, b):
        """Algoritmul Euclidian extins"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def mod_inverse(self, a, m):
        """Calculează inversul modular"""
        gcd, x, _ = self.gcd_extended(a, m)
        if gcd != 1:
            return None
        return (x % m + m) % m

    def is_prime(self, n):
        """Verifică dacă un număr este prim"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def power_mod(self, base, exp, mod):
        """Calculează (base^exp) mod mod folosind exponențierea rapidă"""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result

    def solve_problem1(self):
        """Rezolvă Problema 1 - RSA"""
        try:
            M = int(self.m_var.get())
            p = int(self.p_var.get())
            q = int(self.q_var.get())
            n = int(self.n_var.get())

            result = "=== PROBLEMA 1 - CRIPTOGRAFIA RSA ===\n\n"
            result += f"Parametri de intrare:\n"
            result += f"M = {M} (mesajul secret)\n"
            result += f"p = {p}, q = {q}, n = {n}\n\n"

            # Verifică că p și q sunt prime
            if not self.is_prime(p):
                result += f"ATENȚIE: p = {p} nu este număr prim!\n"
            if not self.is_prime(q):
                result += f"ATENȚIE: q = {q} nu este număr prim!\n"

            # Verifică că n = p * q
            if n != p * q:
                result += f"ATENȚIE: n = {n} ≠ p × q = {p * q}!\n"

            result += "\n" + "=" * 60 + "\n"

            # a) Determinarea funcției alegând b astfel încât (b, (p-1)(q-1)) = 1
            phi_n = (p - 1) * (q - 1)
            result += f"a) Determinarea funcției de criptare:\n"
            result += f"φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {p - 1} × {q - 1} = {phi_n}\n\n"

            result += f"Căutăm b astfel încât gcd(b, φ(n)) = gcd(b, {phi_n}) = 1\n"

            # Găsește un b valid (de obicei se folosește 3, 17, 65537)
            possible_b = [3, 5, 7, 17, 257, 65537]
            b = None
            for candidate in possible_b:
                if math.gcd(candidate, phi_n) == 1:
                    b = candidate
                    break

            if b is None:
                # Caută primul număr impar > 1
                for candidate in range(3, phi_n, 2):
                    if math.gcd(candidate, phi_n) == 1:
                        b = candidate
                        break

            result += f"Alegem b = {b} (gcd({b}, {phi_n}) = {math.gcd(b, phi_n)})\n"
            result += f"Funcția de criptare: E(x) = x^{b} mod {n}\n\n"

            # b) Scrierea mesajului codat
            result += f"b) Criptarea mesajului:\n"
            encrypted = self.power_mod(M, b, n)
            result += f"M_criptat = E({M}) = {M}^{b} mod {n} = {encrypted}\n\n"

            # c) Determinarea funcției de decodare
            result += f"c) Determinarea funcției de decodare:\n"
            result += f"Căutăm a astfel încât a × b ≡ 1 (mod φ(n))\n"
            result += f"Adică: a × {b} ≡ 1 (mod {phi_n})\n"

            a = self.mod_inverse(b, phi_n)
            if a is None:
                result += f"EROARE: Nu se poate calcula inversul modular!\n"
                return

            result += f"a = {a} (verificare: {a} × {b} mod {phi_n} = {(a * b) % phi_n})\n"
            result += f"Funcția de decodare: D(y) = y^{a} mod {n}\n\n"

            # d) Verificarea prin decriptare
            result += f"d) Verificarea prin decriptare:\n"
            decrypted = self.power_mod(encrypted, a, n)
            result += f"M_decriptat = D({encrypted}) = {encrypted}^{a} mod {n} = {decrypted}\n"

            if decrypted == M:
                result += f"✓ SUCCES: Decriptarea a redat mesajul original ({M})\n"
            else:
                result += f"✗ EROARE: Decriptarea nu a redat mesajul original!\n"

            result += "\n" + "=" * 60 + "\n"
            result += "REZUMAT:\n"
            result += f"• Cheia publică: (n={n}, b={b})\n"
            result += f"• Cheia privată: (n={n}, a={a})\n"
            result += f"• Mesaj original: {M}\n"
            result += f"• Mesaj criptat: {encrypted}\n"
            result += f"• Mesaj decriptat: {decrypted}\n"

            self.result1_text.delete(1.0, tk.END)
            self.result1_text.insert(1.0, result)

        except ValueError as e:
            messagebox.showerror("Eroare", f"Valori invalide: {e}")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare în calcul: {e}")

    def solve_problem2(self):
        """Rezolvă Problema 2 - Number Theory"""
        try:
            p = int(self.p2_var.get())
            q = int(self.q2_var.get())
            a = int(self.a_var.get())

            n = p * q
            self.n2_label.config(text=str(n))

            result = "=== PROBLEMA 2 - NUMBER THEORY ===\n\n"
            result += f"Transmitem mesajul: NUMBER THEORY\n"
            result += f"Parametri: p = {p}, q = {q}, n = {n}\n"
            result += f"Pentru decriptare: a = {a}\n\n"

            # Codificare alfabet
            message = "NUMBER THEORY"
            result += f"Mesajul de transmis: '{message}'\n\n"

            # a) Expresia numerică a mesajului
            result += "a) Expresia numerică a mesajului (grupând în grupuri de câte 4, adăugând 00 la final):\n\n"

            # Convertire litere în numere (A=01, B=02, ..., Z=26, spațiu=00)
            char_to_num = {}
            for i in range(26):
                char_to_num[chr(ord('A') + i)] = f"{i + 1:02d}"
            char_to_num[' '] = "00"

            result += "Codificare: A=01, B=02, C=03, ..., Z=26, spațiu=00\n\n"

            # Convertește mesajul
            numeric_string = ""
            for char in message:
                if char in char_to_num:
                    numeric_string += char_to_num[char]
                    result += f"'{char}' → {char_to_num[char]}, "

            result = result.rstrip(", ") + "\n\n"
            result += f"Șirul numeric complet: {numeric_string}\n\n"

            # Grupare în blocuri de 4 cifre
            groups = []
            i = 0
            while i < len(numeric_string):
                group = numeric_string[i:i + 4]
                if len(group) < 4:
                    group += "00" * (4 - len(group))  # completează cu 00
                groups.append(group)
                i += 4

            result += f"Gruparea în blocuri de 4 cifre:\n"
            for i, group in enumerate(groups):
                result += f"Bloc {i + 1}: {group}\n"

            result += f"\nBlocurile ca numere întregi: {[int(g) for g in groups]}\n\n"

            # b) Funcția de codare
            phi_n = (p - 1) * (q - 1)
            result += f"b) Funcția de codare:\n"
            result += f"φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {phi_n}\n"

            # Găsește b (cheia publică)
            b = self.mod_inverse(a, phi_n)
            if b is None:
                result += f"EROARE: Nu se poate determina b din a = {a}\n"
                self.result2_text.delete(1.0, tk.END)
                self.result2_text.insert(1.0, result)
                return

            result += f"Din a = {a}, calculăm b = {b} (verificare: a×b mod φ(n) = {(a * b) % phi_n})\n"
            result += f"Funcția de codare: E(x) = x^{b} mod {n}\n\n"

            # c) Aplicarea funcției de codare
            result += f"c) Aplicarea funcției de codare și scrierea mesajului codat:\n\n"
            encrypted_blocks = []
            for i, group in enumerate(groups):
                block_num = int(group)
                encrypted_block = self.power_mod(block_num, b, n)
                encrypted_blocks.append(encrypted_block)
                result += f"Bloc {i + 1}: E({block_num}) = {block_num}^{b} mod {n} = {encrypted_block}\n"

            result += f"\nMesajul codat: {encrypted_blocks}\n\n"

            # d) Funcția de decodare și verificare
            result += f"d) Funcția de decodare:\n"
            result += f"Pentru a = {a}: D(y) = y^{a} mod {n}\n\n"

            result += f"Aplicarea funcției de decodare:\n"
            decrypted_blocks = []
            for i, encrypted_block in enumerate(encrypted_blocks):
                decrypted_block = self.power_mod(encrypted_block, a, n)
                decrypted_blocks.append(decrypted_block)
                result += f"D({encrypted_block}) = {encrypted_block}^{a} mod {n} = {decrypted_block}\n"

            # e) Recuperarea mesajului original
            result += f"\ne) Recuperarea mesajului original:\n\n"

            # Convertește numerele înapoi în text
            num_to_char = {}
            for char, num in char_to_num.items():
                num_to_char[num] = char

            decoded_message = ""
            for i, block in enumerate(decrypted_blocks):
                block_str = f"{block:04d}"
                result += f"Bloc {i + 1}: {block} → {block_str} → "

                # Decodifică fiecare pereche de cifre
                for j in range(0, len(block_str), 2):
                    pair = block_str[j:j + 2]
                    if pair in num_to_char:
                        char = num_to_char[pair]
                        decoded_message += char
                        result += f"'{pair}'→'{char}' "
                    elif pair == "00":
                        decoded_message += " "
                        result += f"'{pair}'→' ' "

                result += "\n"

            # Curăță mesajul de zerouri suplimentare
            decoded_message = decoded_message.rstrip(' ')

            result += f"\nMesajul decodat final: '{decoded_message}'\n"

            if decoded_message.strip() == message:
                result += "✓ SUCCES: Mesajul a fost recuperat corect!\n"
            else:
                result += f"⚠ ATENȚIE: Mesajul decodat diferă de originalul '{message}'\n"

            result += "\n" + "=" * 60 + "\n"
            result += "REZUMAT:\n"
            result += f"• Mesaj original: '{message}'\n"
            result += f"• Codificare numerică: {groups}\n"
            result += f"• Mesaj criptat: {encrypted_blocks}\n"
            result += f"• Mesaj decriptat: '{decoded_message}'\n"
            result += f"• Cheia publică: (n={n}, b={b})\n"
            result += f"• Cheia privată: (n={n}, a={a})\n"

            self.result2_text.delete(1.0, tk.END)
            self.result2_text.insert(1.0, result)

        except ValueError as e:
            messagebox.showerror("Eroare", f"Valori invalide: {e}")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare în calcul: {e}")


def main():
    root = tk.Tk()
    app = CryptographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()