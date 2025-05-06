import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import random
import os
import sys


class EllipticCurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicația 2: Criptografie pe Curbe Eliptice")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")

        # Crearea frame-ului principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        ttk.Label(main_frame, text="Criptografie pe Curbe Eliptice",
                  font=("Arial", 16, "bold")).pack(pady=10)

        # Frame pentru parametri curbă
        curve_frame = ttk.LabelFrame(main_frame, text="Parametri Curbă Eliptică", padding="10")
        curve_frame.pack(fill=tk.X, pady=10)

        # Ecuația curbei
        ttk.Label(curve_frame, text="Ecuația curbei: y² = x³ + x + 1 peste Z₇",
                  font=("Arial", 11)).pack(fill=tk.X, pady=5)

        # Frame pentru operațiuni
        operations_frame = ttk.LabelFrame(main_frame, text="Operațiuni", padding="10")
        operations_frame.pack(fill=tk.X, pady=10)

        # Butoane pentru operațiuni
        ttk.Button(operations_frame, text="1. Determină punctele curbei",
                   command=self.find_curve_points).pack(fill=tk.X, pady=3)

        message_frame = ttk.Frame(operations_frame)
        message_frame.pack(fill=tk.X, pady=3)
        ttk.Label(message_frame, text="Mesaj M (x,y): ").pack(side=tk.LEFT)
        self.message_var = tk.StringVar(value="(10,9)")
        ttk.Entry(message_frame, textvariable=self.message_var, width=10).pack(side=tk.LEFT)
        ttk.Button(message_frame, text="2. Cifrează mesajul",
                   command=self.encrypt_message).pack(side=tk.LEFT, padx=5)

        cipher_frame = ttk.Frame(operations_frame)
        cipher_frame.pack(fill=tk.X, pady=3)
        ttk.Label(cipher_frame, text="Mesaj cifrat C: ").pack(side=tk.LEFT)
        self.cipher_var = tk.StringVar()
        ttk.Entry(cipher_frame, textvariable=self.cipher_var, width=30).pack(side=tk.LEFT)
        ttk.Button(cipher_frame, text="3. Descifrează mesajul",
                   command=self.decrypt_message).pack(side=tk.LEFT, padx=5)

        # Frame pentru rezultate
        result_frame = ttk.LabelFrame(main_frame, text="Rezultate", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Text area pentru rezultate
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Butoane pentru actiuni
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Curăță", command=self.clear_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ieșire", command=root.destroy).pack(side=tk.RIGHT, padx=5)

        # Inițializăm variabile
        self.p = 7  # Modulul pentru Z₇
        self.points = []  # Lista punctelor de pe curbă
        self.alpha = None  # Elementul generator public
        self.beta = None  # Cheia publică
        self.k = 4  # Cheia secretă k
        self.d = 3  # Cheia privată d

    def mod_inv(self, a, m):
        # Calculează inversul modular a^-1 mod m
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            raise Exception(f'Inversul modular {a}^-1 mod {m} nu există')
        else:
            return x % m

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def is_quadratic_residue(self, a, p):
        # Verifică dacă a este reziduu pătratic modulo p
        if p == 2:
            return True
        return pow(a, (p - 1) // 2, p) == 1

    def sqrt_mod(self, a, p):
        # Calculează rădăcina pătrată modulară sqrt(a) mod p
        # Folosim algoritmul Tonelli-Shanks pentru simplitate
        if not self.is_quadratic_residue(a, p):
            return []

        # Pentru p ≡ 3 mod 4, sqrt(a) = a^((p+1)/4) mod p
        if p % 4 == 3:
            r = pow(a, (p + 1) // 4, p)
            return [r, p - r]

        # Pentru alte cazuri, implementăm o versiune simplificată
        # Această metodă funcționează pentru moduluri mici
        for i in range(p):
            if (i * i) % p == a % p:
                return [i, p - i]
        return []

    def point_addition(self, P, Q):
        # Adunarea punctelor pe curba eliptică
        if P is None or P == "O":
            return Q
        if Q is None or Q == "O":
            return P

        x1, y1 = P
        x2, y2 = Q

        # Dacă P + (-P) = O (punctul la infinit)
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return "O"

        # Calculăm panta λ
        if x1 == x2 and y1 == y2:  # Dublare punct
            # λ = (3x₁² + 1) / (2y₁) mod p
            numerator = (3 * x1 * x1 + 1) % self.p
            denominator = (2 * y1) % self.p
            lam = (numerator * self.mod_inv(denominator, self.p)) % self.p
        else:  # Adunare puncte diferite
            # λ = (y₂ - y₁) / (x₂ - x₁) mod p
            numerator = (y2 - y1) % self.p
            denominator = (x2 - x1) % self.p
            lam = (numerator * self.mod_inv(denominator, self.p)) % self.p

        # Calculăm x₃ = λ² - x₁ - x₂ mod p
        x3 = (lam * lam - x1 - x2) % self.p

        # Calculăm y₃ = λ(x₁ - x₃) - y₁ mod p
        y3 = (lam * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_multiplication(self, k, P):
        # Multiplicarea scalară: k*P folosind metoda dublărilor și adunărilor succesive
        result = "O"  # Începem cu punctul la infinit (elementul neutru)
        addend = P

        while k > 0:
            if k & 1:  # Dacă bitul curent este 1
                result = self.point_addition(result, addend)
            addend = self.point_addition(addend, addend)  # Dublăm punctul
            k >>= 1  # Deplasare la dreapta cu un bit

        return result

    def find_curve_points(self):
        # Găsim toate punctele de pe curba eliptică y² = x³ + x + 1 peste Z₇
        self.points = []
        result = "Punctele curbei eliptice y² = x³ + x + 1 peste Z₇:\n\n"
        result += "Punct la infinit O\n"

        for x in range(self.p):
            # Calculăm partea dreaptă: x³ + x + 1 mod p
            rhs = (x ** 3 + x + 1) % self.p

            # Găsim valorile y pentru care y² = rhs mod p
            y_values = self.sqrt_mod(rhs, self.p)

            for y in y_values:
                self.points.append((x, y))
                result += f"({x}, {y})\n"

        # Afișăm numărul total de puncte
        result += f"\nTotal puncte: {len(self.points) + 1} (inclusiv punctul la infinit)\n"

        # Alegem alpha (un generator) și calculăm beta
        if len(self.points) > 0:
            self.alpha = self.points[0]  # Pentru simplitate, alegem primul punct
            self.d = 3  # Cheia privată aleasă
            self.beta = self.scalar_multiplication(self.d, self.alpha)

            result += f"\nElement α ales (generator): {self.alpha}\n"
            result += f"Cheie privată d aleasă: {self.d}\n"
            result += f"Cheie publică β = d·α: {self.beta}\n"

            # Calculăm ordinul grupului verificând multiplii lui alpha
            order = 1
            temp = self.alpha
            while temp != "O":
                order += 1
                temp = self.point_addition(temp, self.alpha)
                if order > 20:  # Evităm bucle infinite
                    break

            result += f"Ordinul elementului α: {order}\n"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    def encrypt_message(self):
        try:
            # Cifrăm mesajul M utilizând curba eliptică
            if not self.points:
                self.find_curve_points()

            # Parsăm mesajul din format (x,y)
            message_str = self.message_var.get().strip('()')
            x, y = map(int, message_str.split(','))
            M = (x, y)

            # Verificăm dacă M este pe curbă
            rhs = (x ** 3 + x + 1) % self.p
            lhs = (y ** 2) % self.p

            if lhs != rhs:
                raise ValueError("Mesajul M nu este un punct valid pe curba eliptică!")

            # Generăm k (în acest caz k=4 conform cerinței)
            k = self.k

            # Calculăm C = (k·α, M + k·β)
            kA = self.scalar_multiplication(k, self.alpha)
            kB = self.scalar_multiplication(k, self.beta)
            C2 = self.point_addition(M, kB)
            C = (kA, C2)

            self.cipher_var.set(f"{kA},{C2}")

            result = f"Cifrarea mesajului M = {M}:\n\n"
            result += f"Folosind cheia secretă k = {k}\n"
            result += f"Elementul generator α = {self.alpha}\n"
            result += f"Cheia publică β = {self.beta}\n\n"
            result += f"C1 = k·α = {k}·{self.alpha} = {kA}\n"
            result += f"C2 = M + k·β = {M} + {k}·{self.beta} = {M} + {kB} = {C2}\n"
            result += f"Mesajul cifrat C = (C1, C2) = ({kA}, {C2})\n"

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Eroare: {str(e)}")

    def decrypt_message(self):
        try:
            # Descifrăm mesajul C utilizând curba eliptică
            if not self.points:
                self.find_curve_points()

            # Parsăm textul cifrat din format C1,C2
            cipher_text = self.cipher_var.get()
            parts = cipher_text.split('),(')

            # Dacă este în format ((x,y),(u,v))
            if len(parts) == 2:
                c1_str = parts[0].strip('(')
                c2_str = parts[1].strip(')')
            else:
                # Încercăm formatul (x,y),(u,v)
                parts = cipher_text.split('),(')
                if len(parts) == 2:
                    c1_str = parts[0]
                    c2_str = parts[1]
                else:
                    # Încercăm formatul (x,y),(u,v)
                    parts = cipher_text.split(',')
                    if len(parts) == 4:
                        c1_str = f"{parts[0].strip('(')},{parts[1]}"
                        c2_str = f"{parts[2]},{parts[3].strip(')')}"
                    else:
                        raise ValueError("Format de mesaj cifrat invalid!")

            # Extragem coordonatele punctelor
            c1_coords = c1_str.strip('()').split(',')
            c2_coords = c2_str.strip('()').split(',')

            C1 = (int(c1_coords[0]), int(c1_coords[1]))
            C2 = (int(c2_coords[0]), int(c2_coords[1]))

            # Descifrăm cu d·C1
            dC1 = self.scalar_multiplication(self.d, C1)

            # Negăm punctul dC1 (schimbăm semnul lui y)
            neg_dC1 = (dC1[0], (-dC1[1]) % self.p)

            # Calculăm M = C2 - d·C1
            M = self.point_addition(C2, neg_dC1)

            result = f"Descifrarea mesajului C = ({C1}, {C2}):\n\n"
            result += f"Folosind cheia privată d = {self.d}\n\n"
            result += f"d·C1 = {self.d}·{C1} = {dC1}\n"
            result += f"-(d·C1) = {neg_dC1}\n"
            result += f"M = C2 - d·C1 = {C2} + {neg_dC1} = {M}\n\n"
            result += f"Mesaj descifrat: M = {M}\n"

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Eroare: {str(e)}")

    def clear_result(self):
        self.result_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = EllipticCurveApp(root)
    root.mainloop()