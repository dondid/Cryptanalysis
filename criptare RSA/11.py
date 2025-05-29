import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import sympy


class RSAApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicații Criptare RSA")
        self.geometry("1000x800")
        self.configure(bg="#f0f0f0")

        # Crearea notebook (tab control)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aplicația 1
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Aplicația 1")
        self.setup_app1()

        # Aplicația 2
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Aplicația 2")
        self.setup_app2()

    def setup_app1(self):
        # Frame pentru inputuri
        input_frame = ttk.LabelFrame(self.tab1, text="Date de intrare")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Mesaj, p și q
        ttk.Label(input_frame, text="Mesaj (M):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.message_entry1 = ttk.Entry(input_frame, width=20)
        self.message_entry1.grid(row=0, column=1, padx=5, pady=5)
        self.message_entry1.insert(0, "101")

        ttk.Label(input_frame, text="p:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.p_entry1 = ttk.Entry(input_frame, width=20)
        self.p_entry1.grid(row=1, column=1, padx=5, pady=5)
        self.p_entry1.insert(0, "11")

        ttk.Label(input_frame, text="q:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.q_entry1 = ttk.Entry(input_frame, width=20)
        self.q_entry1.grid(row=2, column=1, padx=5, pady=5)
        self.q_entry1.insert(0, "17")

        ttk.Label(input_frame, text="b (opțional):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.b_entry1 = ttk.Entry(input_frame, width=20)
        self.b_entry1.grid(row=3, column=1, padx=5, pady=5)

        # Buton pentru calcul
        calc_button = ttk.Button(input_frame, text="Calculează", command=self.calculate_app1)
        calc_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Frame pentru rezultate
        result_frame = ttk.LabelFrame(self.tab1, text="Rezultate și pași")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Text widget pentru afișarea rezultatelor
        self.result_text1 = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD)
        self.result_text1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_app2(self):
        # Frame pentru inputuri
        input_frame = ttk.LabelFrame(self.tab2, text="Date de intrare")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Mesaj, p și q
        ttk.Label(input_frame, text="Mesaj:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.message_entry2 = ttk.Entry(input_frame, width=30)
        self.message_entry2.grid(row=0, column=1, padx=5, pady=5)
        self.message_entry2.insert(0, "NUMBER THEORY")

        ttk.Label(input_frame, text="p:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.p_entry2 = ttk.Entry(input_frame, width=30)
        self.p_entry2.grid(row=1, column=1, padx=5, pady=5)
        self.p_entry2.insert(0, "15121")

        ttk.Label(input_frame, text="q:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.q_entry2 = ttk.Entry(input_frame, width=30)
        self.q_entry2.grid(row=2, column=1, padx=5, pady=5)
        self.q_entry2.insert(0, "15131")

        ttk.Label(input_frame, text="b:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.b_entry2 = ttk.Entry(input_frame, width=30)
        self.b_entry2.grid(row=3, column=1, padx=5, pady=5)
        self.b_entry2.insert(0, "2413")

        ttk.Label(input_frame, text="a (pentru decriptare):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.a_entry2 = ttk.Entry(input_frame, width=30)
        self.a_entry2.grid(row=4, column=1, padx=5, pady=5)
        self.a_entry2.insert(0, "223043599")

        # Buton pentru calcul
        calc_button = ttk.Button(input_frame, text="Calculează", command=self.calculate_app2)
        calc_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Frame pentru rezultate
        result_frame = ttk.LabelFrame(self.tab2, text="Rezultate și pași")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Text widget pentru afișarea rezultatelor
        self.result_text2 = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD)
        self.result_text2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def euclidean_extended(self, a, b):
        """Algoritmul lui Euclid extins pentru a găsi inversul modular"""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.euclidean_extended(b % a, a)
            return gcd, y - (b // a) * x, x

    def find_modular_inverse(self, a, m):
        """Găsește inversul modular al lui a mod m"""
        gcd, x, y = self.euclidean_extended(a, m)
        if gcd != 1:
            return None  # Inversul modular nu există
        else:
            return x % m

    def mod_pow(self, base, exponent, modulus):
        """Calcul eficient pentru (base^exponent) % modulus"""
        if modulus == 1:
            return 0

        result = 1
        base = base % modulus

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus

        return result

    def calculate_app1(self):
        try:
            # Curățăm zona de rezultate
            self.result_text1.delete(1.0, tk.END)

            # Obținem valorile introduse
            m = int(self.message_entry1.get())
            p = int(self.p_entry1.get())
            q = int(self.q_entry1.get())

            # Verificăm dacă p și q sunt prime
            if not sympy.isprime(p) or not sympy.isprime(q):
                messagebox.showerror("Eroare", "p și q trebuie să fie numere prime!")
                return

            # Calculează n și phi(n)
            n = p * q
            phi_n = (p - 1) * (q - 1)

            self.result_text1.insert(tk.END, f"Aplicația 1 - Mesaj: M = {m}\n\n")
            self.result_text1.insert(tk.END, f"Pas 1: Calculăm n = p * q = {p} * {q} = {n}\n")
            self.result_text1.insert(tk.END,
                                     f"Pas 2: Calculăm φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {p - 1}*{q - 1} = {phi_n}\n\n")

            # Determinăm b dacă nu a fost specificat
            if not self.b_entry1.get():
                # Găsim un b pentru care (b, phi_n) = 1
                for b in range(2, phi_n):
                    if math.gcd(b, phi_n) == 1:
                        self.b_entry1.delete(0, tk.END)
                        self.b_entry1.insert(0, str(b))
                        break

            b = int(self.b_entry1.get())

            # Verificăm dacă b și phi_n sunt relativ prime
            if math.gcd(b, phi_n) != 1:
                messagebox.showerror("Eroare", f"b = {b} și φ(n) = {phi_n} nu sunt relativ prime!")
                return

            self.result_text1.insert(tk.END, f"Pas 3: Alegem b = {b} astfel încât (b, φ(n)) = 1\n")
            self.result_text1.insert(tk.END, f"       Verificare: gcd({b}, {phi_n}) = {math.gcd(b, phi_n)}\n\n")

            # Calculăm a = inversul lui b modulo phi_n
            a = self.find_modular_inverse(b, phi_n)

            self.result_text1.insert(tk.END, f"Pas 4: Calculăm a astfel încât a*b ≡ 1 (mod φ(n))\n")
            self.result_text1.insert(tk.END, f"       a = {a}\n")
            self.result_text1.insert(tk.END,
                                     f"       Verificare: {a} * {b} = {a * b} ≡ {(a * b) % phi_n} (mod {phi_n})\n\n")

            # Criptarea mesajului
            c = self.mod_pow(m, b, n)

            self.result_text1.insert(tk.END, f"Pas 5: Criptăm mesajul M = {m}\n")
            self.result_text1.insert(tk.END, f"       c = M^b mod n = {m}^{b} mod {n} = {c}\n\n")

            # Decriptarea mesajului
            decrypted = self.mod_pow(c, a, n)

            self.result_text1.insert(tk.END, f"Pas 6: Decriptăm mesajul criptat c = {c}\n")
            self.result_text1.insert(tk.END, f"       M = c^a mod n = {c}^{a} mod {n} = {decrypted}\n\n")

            # Verificare
            self.result_text1.insert(tk.END, f"Verificare finală: Mesajul decriptat ({decrypted}) ")
            if decrypted == m:
                self.result_text1.insert(tk.END, "este identic cu mesajul original!\n\n")
            else:
                self.result_text1.insert(tk.END, "nu este identic cu mesajul original!\n\n")

            # Rezumat
            self.result_text1.insert(tk.END, "REZUMAT:\n")
            self.result_text1.insert(tk.END, f"- Mesaj original: M = {m}\n")
            self.result_text1.insert(tk.END, f"- Cheia publică: (n={n}, b={b})\n")
            self.result_text1.insert(tk.END, f"- Cheia privată: (p={p}, q={q}, a={a})\n")
            self.result_text1.insert(tk.END, f"- Mesaj criptat: c = {c}\n")
            self.result_text1.insert(tk.END, f"- Mesaj decriptat: {decrypted}\n")

        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")

    def calculate_app2(self):
        try:
            # Curățăm zona de rezultate
            self.result_text2.delete(1.0, tk.END)

            # Obținem valorile introduse
            message = self.message_entry2.get()
            p = int(self.p_entry2.get())
            q = int(self.q_entry2.get())
            b = int(self.b_entry2.get())
            a = int(self.a_entry2.get())

            # Verificăm dacă p și q sunt prime
            if not sympy.isprime(p) or not sympy.isprime(q):
                messagebox.showerror("Eroare", "p și q trebuie să fie numere prime!")
                return

            # Calculăm n și phi(n)
            n = p * q
            phi_n = (p - 1) * (q - 1)

            self.result_text2.insert(tk.END, f"Aplicația 2 - Mesaj: '{message}'\n\n")
            self.result_text2.insert(tk.END, f"Pas 1: Calculăm n = p * q = {p} * {q} = {n}\n")
            self.result_text2.insert(tk.END,
                                     f"Pas 2: Calculăm φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {p - 1}*{q - 1} = {phi_n}\n\n")

            # Verificăm dacă b și phi_n sunt relativ prime
            if math.gcd(b, phi_n) != 1:
                messagebox.showerror("Eroare", f"b = {b} și φ(n) = {phi_n} nu sunt relativ prime!")
                return

            self.result_text2.insert(tk.END, f"Pas 3: Verificăm b = {b} astfel încât (b, φ(n)) = 1\n")
            self.result_text2.insert(tk.END, f"       Verificare: gcd({b}, {phi_n}) = {math.gcd(b, phi_n)}\n\n")

            # Verificăm dacă a este inversul lui b
            if (a * b) % phi_n != 1:
                messagebox.showerror("Eroare", f"a = {a} nu este inversul lui b = {b} modulo φ(n)!")
                return

            self.result_text2.insert(tk.END, f"Pas 4: Verificăm a = {a} astfel încât a*b ≡ 1 (mod φ(n))\n")
            self.result_text2.insert(tk.END,
                                     f"       Verificare: {a} * {b} = {a * b} ≡ {(a * b) % phi_n} (mod {phi_n})\n\n")

            # Codificăm mesajul în numere
            mapping = {' ': '00'}
            for i in range(26):
                mapping[chr(65 + i)] = f"{i + 1:02d}"

            self.result_text2.insert(tk.END, "Pas 5: Codificăm mesajul folosind scheme de codificare:\n")
            self.result_text2.insert(tk.END, "       A=01, B=02, ..., Z=26, ' '=00\n\n")

            numeric_message = ""
            for char in message:
                if char in mapping:
                    numeric_message += mapping[char]
                    self.result_text2.insert(tk.END, f"       {char} -> {mapping[char]}\n")

            # Grupăm în blocuri de câte 4 cifre
            blocks = []
            i = 0
            block = ""

            self.result_text2.insert(tk.END, "\nPas 6: Grupăm în blocuri de câte 4 cifre:\n")

            for digit in numeric_message:
                block += digit
                i += 1
                if i % 4 == 0:
                    blocks.append(block)
                    block = ""

            # Dacă a rămas un bloc incomplet, adăugăm zerouri
            if block:
                while len(block) < 4:
                    block += "0"
                blocks.append(block)

            self.result_text2.insert(tk.END, f"       Blocuri: {blocks}\n\n")

            # Criptăm fiecare bloc
            encrypted_blocks = []

            self.result_text2.insert(tk.END, "Pas 7: Criptăm fiecare bloc folosind funcția de criptare:\n")
            self.result_text2.insert(tk.END, f"       e(x) = x^{b} mod {n}\n\n")

            for block in blocks:
                x = int(block)
                if x >= n:
                    messagebox.showwarning("Avertisment", f"Blocul {x} este mai mare sau egal cu n = {n}!")
                encrypted = self.mod_pow(x, b, n)
                encrypted_blocks.append(encrypted)
                self.result_text2.insert(tk.END, f"       {block}^{b} mod {n} = {encrypted}\n")

            self.result_text2.insert(tk.END, f"\n       Mesaj criptat: {encrypted_blocks}\n\n")

            # Decriptăm fiecare bloc
            decrypted_blocks = []

            self.result_text2.insert(tk.END, "Pas 8: Decriptăm fiecare bloc folosind funcția de decriptare:\n")
            self.result_text2.insert(tk.END, f"       d(y) = y^{a} mod {n}\n\n")

            for encrypted in encrypted_blocks:
                decrypted = self.mod_pow(encrypted, a, n)
                decrypted_blocks.append(f"{decrypted:04d}")
                self.result_text2.insert(tk.END, f"       {encrypted}^{a} mod {n} = {decrypted:04d}\n")

            self.result_text2.insert(tk.END, f"\n       Blocuri decriptate: {decrypted_blocks}\n\n")

            # Convertim blocurile decriptate înapoi în text
            inverse_mapping = {v: k for k, v in mapping.items()}

            decrypted_message = ""
            for block in decrypted_blocks:
                for i in range(0, len(block), 2):
                    if i + 1 < len(block):
                        code = block[i:i + 2]
                        if code in inverse_mapping:
                            decrypted_message += inverse_mapping[code]

            self.result_text2.insert(tk.END, "Pas 9: Decodificăm mesajul:\n")

            for block in decrypted_blocks:
                for i in range(0, len(block), 2):
                    if i + 1 < len(block):
                        code = block[i:i + 2]
                        if code in inverse_mapping:
                            self.result_text2.insert(tk.END, f"       {code} -> {inverse_mapping[code]}\n")

            # Elimină eventualele zero-uri adăugate la final
            decrypted_message = decrypted_message.rstrip()

            self.result_text2.insert(tk.END, f"\n       Mesaj decriptat: '{decrypted_message}'\n\n")

            # Verificare
            self.result_text2.insert(tk.END, f"Verificare finală: Mesajul decriptat ('{decrypted_message}') ")
            if decrypted_message == message:
                self.result_text2.insert(tk.END, "este identic cu mesajul original!\n\n")
            else:
                self.result_text2.insert(tk.END, "nu este identic cu mesajul original!\n\n")

            # Rezumat
            self.result_text2.insert(tk.END, "REZUMAT:\n")
            self.result_text2.insert(tk.END, f"- Mesaj original: '{message}'\n")
            self.result_text2.insert(tk.END, f"- Reprezentare numerică: {numeric_message}\n")
            self.result_text2.insert(tk.END, f"- Blocuri de 4 cifre: {blocks}\n")
            self.result_text2.insert(tk.END, f"- Cheia publică: (n={n}, b={b})\n")
            self.result_text2.insert(tk.END, f"- Cheia privată: a={a}\n")
            self.result_text2.insert(tk.END, f"- Mesaj criptat: {encrypted_blocks}\n")
            self.result_text2.insert(tk.END, f"- Mesaj decriptat: '{decrypted_message}'\n")

        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")


if __name__ == "__main__":
    app = RSAApplication()
    app.mainloop()