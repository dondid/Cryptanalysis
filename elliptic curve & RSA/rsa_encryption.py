import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import os
import sys


class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicația 1: Criptosistem RSA")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        # Crearea frame-ului principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        ttk.Label(main_frame, text="Criptosistem Exponențial (RSA)",
                  font=("Arial", 16, "bold")).pack(pady=10)

        # Frame pentru datele de intrare
        input_frame = ttk.LabelFrame(main_frame, text="Date de intrare", padding="10")
        input_frame.pack(fill=tk.X, pady=10)

        # Numărul prim p
        ttk.Label(input_frame, text="Număr prim p:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.p_var = tk.StringVar(value="101")
        ttk.Entry(input_frame, textvariable=self.p_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)

        # Cheia de criptare e
        ttk.Label(input_frame, text="Cheie de criptare e:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.e_var = tk.StringVar(value="23")
        ttk.Entry(input_frame, textvariable=self.e_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)

        # Mesaj de criptat
        ttk.Label(input_frame, text="Mesaj de criptat:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.message_var = tk.StringVar(value="CRIPTOGRAFIE")
        ttk.Entry(input_frame, textvariable=self.message_var, width=30).grid(row=2, column=1, columnspan=2, sticky=tk.W,
                                                                             pady=5)

        # Frame pentru rezultate
        result_frame = ttk.LabelFrame(main_frame, text="Rezultate", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Text area pentru rezultate
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=70, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Butoane pentru actiuni
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Criptează Mesaj", command=self.encrypt_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stabilește Cheia Comună", command=self.generate_common_key).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(button_frame, text="Curăță", command=self.clear_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ieșire", command=root.destroy).pack(side=tk.RIGHT, padx=5)

    def char_to_num(self, char):
        # Convertim caracterele în numere (A=1, B=2, ...)
        if 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 1
        return 0

    def num_to_char(self, num):
        # Convertim numere înapoi în caractere
        if 1 <= num <= 26:
            return chr(num + ord('A') - 1)
        return '?'

    def encrypt_message(self):
        try:
            p = int(self.p_var.get())
            e = int(self.e_var.get())
            message = self.message_var.get().upper()

            if not self.is_prime(p):
                self.result_text.insert(tk.END, f"Eroare: {p} nu este număr prim!\n")
                return

            if math.gcd(e, p - 1) != 1:
                self.result_text.insert(tk.END, f"Eroare: e={e} nu este coprim cu p-1={p - 1}!\n")
                return

            # Calculul cheii private d
            d = self.modular_inverse(e, p - 1)

            result = "Criptarea mesajului '" + message + "':\n\n"
            result += f"Folosind criptosistemul exponențial cu p={p}, e={e}\n"
            result += f"Cheia privată d={d} (inversul lui e modulo p-1)\n\n"

            encrypted_values = []
            details = []

            for char in message:
                num = self.char_to_num(char)
                encrypted = pow(num, e, p)
                encrypted_values.append(str(encrypted))
                details.append(f"{char}({num}) -> {num}^{e} mod {p} = {encrypted}")

            result += "Detalii criptare:\n" + "\n".join(details) + "\n\n"
            result += "Mesaj criptat (numere): " + ", ".join(encrypted_values) + "\n"

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Eroare: {str(e)}")

    def generate_common_key(self):
        try:
            p = int(self.p_var.get())

            if not self.is_prime(p):
                self.result_text.insert(tk.END, f"Eroare: {p} nu este număr prim!\n")
                return

            # Găsim o pereche de chei pentru Alice
            e_alice = 23  # Alegem un e pentru Alice (coprim cu p-1)
            d_alice = self.modular_inverse(e_alice, p - 1)

            # Găsim o pereche de chei pentru Bob
            e_bob = 7  # Alegem un e pentru Bob (coprim cu p-1)
            d_bob = self.modular_inverse(e_bob, p - 1)

            # Presupunem că ambele părți aleg un număr comun g
            g = 2  # Generator obișnuit

            # Alice calculează și trimite
            alice_public = pow(g, d_alice, p)

            # Bob calculează și trimite
            bob_public = pow(g, d_bob, p)

            # Alice calculează cheia comună
            alice_common_key = pow(bob_public, d_alice, p)

            # Bob calculează cheia comună
            bob_common_key = pow(alice_public, d_bob, p)

            result = f"Stabilirea unei chei comune cu numărul prim p={p}:\n\n"
            result += f"Alice: Cheie publică e_A={e_alice}, cheie privată d_A={d_alice}\n"
            result += f"Bob: Cheie publică e_B={e_bob}, cheie privată d_B={d_bob}\n\n"
            result += f"Generator g={g}\n\n"
            result += f"Alice trimite: g^d_A mod p = {g}^{d_alice} mod {p} = {alice_public}\n"
            result += f"Bob trimite: g^d_B mod p = {g}^{d_bob} mod {p} = {bob_public}\n\n"
            result += f"Alice calculează: (g^d_B)^d_A mod p = {bob_public}^{d_alice} mod {p} = {alice_common_key}\n"
            result += f"Bob calculează: (g^d_A)^d_B mod p = {alice_public}^{d_bob} mod {p} = {bob_common_key}\n\n"
            result += f"Cheia comună stabilită: {alice_common_key}"

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Eroare: {str(e)}")

    def is_prime(self, n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def modular_inverse(self, a, m):
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise Exception(f"Inversul modular nu există pentru {a} mod {m}")
        else:
            return x % m

    def clear_result(self):
        self.result_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()