import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import sympy
import numpy as np
from sympy import mod_inverse, gcd


class CryptoSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptographic Applications Solver")
        self.root.geometry("1000x700")

        # Create notebook with tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs for each application
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Aplicația 1: Pohlig-Hellman")
        self.notebook.add(self.tab2, text="Aplicația 2: Semnătura Eliptică")
        self.notebook.add(self.tab3, text="Aplicația 3: Factorizare")

        # Setup each tab
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

    def setup_tab1(self):
        """Setup for Pohlig-Hellman discrete logarithm"""
        frame = ttk.Frame(self.tab1, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Calcularea logaritmului discret folosind algoritmul Pohlig-Hellman",
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Input fields
        ttk.Label(frame, text="Valoare pentru logaritm (a):").grid(row=1, column=0, sticky='w', pady=5)
        self.value_entry = ttk.Entry(frame, width=10)
        self.value_entry.grid(row=1, column=1, sticky='w', pady=5)
        self.value_entry.insert(0, "14")

        ttk.Label(frame, text="Baza logaritmului (baza 2):").grid(row=2, column=0, sticky='w', pady=5)
        self.base_entry = ttk.Entry(frame, width=10)
        self.base_entry.grid(row=2, column=1, sticky='w', pady=5)
        self.base_entry.insert(0, "2")

        ttk.Label(frame, text="Modul (p):").grid(row=3, column=0, sticky='w', pady=5)
        self.modulus_entry = ttk.Entry(frame, width=10)
        self.modulus_entry.grid(row=3, column=1, sticky='w', pady=5)
        self.modulus_entry.insert(0, "19")

        # Solve button
        ttk.Button(frame, text="Rezolvă", command=self.solve_pohlig_hellman).grid(row=4, column=0, columnspan=2,
                                                                                  pady=10)

        # Output area
        ttk.Label(frame, text="Rezultat:").grid(row=5, column=0, sticky='w')
        self.output_text1 = scrolledtext.ScrolledText(frame, width=80, height=20)
        self.output_text1.grid(row=6, column=0, columnspan=2, pady=5)

    def setup_tab2(self):
        """Setup for Elliptic Curve Signature"""
        frame = ttk.Frame(self.tab2, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Semnătură Digitală folosind Curbe Eliptice",
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Input parameters for the elliptic curve
        param_frame = ttk.LabelFrame(frame, text="Parametri")
        param_frame.grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        ttk.Label(param_frame, text="p:").grid(row=0, column=0, sticky='w', pady=2)
        self.p_entry = ttk.Entry(param_frame, width=10)
        self.p_entry.grid(row=0, column=1, sticky='w', pady=2)
        self.p_entry.insert(0, "11")

        ttk.Label(param_frame, text="q:").grid(row=1, column=0, sticky='w', pady=2)
        self.q_entry = ttk.Entry(param_frame, width=10)
        self.q_entry.grid(row=1, column=1, sticky='w', pady=2)
        self.q_entry.insert(0, "13")

        ttk.Label(param_frame, text="A (punct generator x,y):").grid(row=2, column=0, sticky='w', pady=2)
        self.A_entry = ttk.Entry(param_frame, width=10)
        self.A_entry.grid(row=2, column=1, sticky='w', pady=2)
        self.A_entry.insert(0, "2,7")

        ttk.Label(param_frame, text="B (alt punct x,y):").grid(row=3, column=0, sticky='w', pady=2)
        self.B_entry = ttk.Entry(param_frame, width=10)
        self.B_entry.grid(row=3, column=1, sticky='w', pady=2)
        self.B_entry.insert(0, "7,2")

        ttk.Label(param_frame, text="m (parametru):").grid(row=4, column=0, sticky='w', pady=2)
        self.m_entry = ttk.Entry(param_frame, width=10)
        self.m_entry.grid(row=4, column=1, sticky='w', pady=2)
        self.m_entry.insert(0, "7")

        # Signature parameters
        sig_frame = ttk.LabelFrame(frame, text="Semnătură")
        sig_frame.grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        ttk.Label(sig_frame, text="Mesaj (x):").grid(row=0, column=0, sticky='w', pady=2)
        self.message_entry = ttk.Entry(sig_frame, width=10)
        self.message_entry.grid(row=0, column=1, sticky='w', pady=2)
        self.message_entry.insert(0, "4")

        ttk.Label(sig_frame, text="Valoare aleatoare (k):").grid(row=1, column=0, sticky='w', pady=2)
        self.k_entry = ttk.Entry(sig_frame, width=10)
        self.k_entry.grid(row=1, column=1, sticky='w', pady=2)
        self.k_entry.insert(0, "3")

        # Solve button
        ttk.Button(frame, text="Calculează Semnătura", command=self.solve_elliptic_signature).grid(row=3, column=0,
                                                                                                   columnspan=2,
                                                                                                   pady=10)

        # Output area
        ttk.Label(frame, text="Rezultat:").grid(row=4, column=0, sticky='w')
        self.output_text2 = scrolledtext.ScrolledText(frame, width=80, height=20)
        self.output_text2.grid(row=5, column=0, columnspan=2, pady=5)

    def setup_tab3(self):
        """Setup for Number Factorization using Elliptic Curve"""
        frame = ttk.Frame(self.tab3, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Factorizare Folosind Curbe Eliptice",
                  font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Input parameters
        ttk.Label(frame, text="Număr de factorizat (n):").grid(row=1, column=0, sticky='w', pady=5)
        self.n_entry = ttk.Entry(frame, width=10)
        self.n_entry.grid(row=1, column=1, sticky='w', pady=5)
        self.n_entry.insert(0, "45")

        ttk.Label(frame, text="Coeficient a:").grid(row=2, column=0, sticky='w', pady=5)
        self.a_coef_entry = ttk.Entry(frame, width=10)
        self.a_coef_entry.grid(row=2, column=1, sticky='w', pady=5)
        self.a_coef_entry.insert(0, "1")

        ttk.Label(frame, text="Punct inițial P(x,y):").grid(row=3, column=0, sticky='w', pady=5)
        self.point_entry = ttk.Entry(frame, width=10)
        self.point_entry.grid(row=3, column=1, sticky='w', pady=5)
        self.point_entry.insert(0, "1,1")

        # Solve button
        ttk.Button(frame, text="Factorizează", command=self.solve_factorization).grid(row=4, column=0, columnspan=2,
                                                                                      pady=10)

        # Output area
        ttk.Label(frame, text="Rezultat:").grid(row=5, column=0, sticky='w')
        self.output_text3 = scrolledtext.ScrolledText(frame, width=80, height=20)
        self.output_text3.grid(row=6, column=0, columnspan=2, pady=5)

    def pohlig_hellman(self, a, g, p):
        """
        Implementation of Pohlig-Hellman algorithm for discrete logarithm
        Finds x such that g^x ≡ a (mod p)
        """
        # Find p-1 factorization
        p_minus_1 = p - 1
        factors = sympy.factorint(p_minus_1)

        result_text = f"Aplicăm algoritmul Pohlig-Hellman pentru a calcula log_{g}({a}) în Z_{p}\n\n"
        result_text += f"Pasul 1: Factorizăm p-1 = {p - 1}\n"

        # Display factorization
        factor_str = " * ".join([f"{prime}^{exp}" for prime, exp in factors.items()])
        result_text += f"p-1 = {factor_str}\n\n"

        # Calculate discrete log for each prime factor
        chinese_remainder_equations = []
        moduli = []

        for prime, exponent in factors.items():
            q = prime
            q_power = q ** exponent

            result_text += f"Pasul 2: Pentru factorul primar q = {q} cu exponentul {exponent}:\n"

            # Compute g_q = g^((p-1)/q^e) mod p
            g_q = pow(g, p_minus_1 // q_power, p)
            result_text += f"  g_q = g^((p-1)/{q}^{exponent}) mod p = {g_q}\n"

            # Compute a_q = a^((p-1)/q^e) mod p
            a_q = pow(a, p_minus_1 // q_power, p)
            result_text += f"  a_q = a^((p-1)/{q}^{exponent}) mod p = {a_q}\n"

            # Calculate discrete log for this prime factor
            x_q = 0
            for j in range(exponent):
                # Calculate gamma = (a * g^(-x_q))^((p-1)/(q^(j+1))) mod p
                gamma = pow(a * pow(g, -x_q, p) % p, p_minus_1 // (q ** (j + 1)), p)
                result_text += f"    j = {j}: gamma = {gamma}\n"

                # Find d such that (g^((p-1)/q))^d ≡ gamma (mod p)
                d = 0
                g_to_power = 1
                g_base = pow(g, p_minus_1 // q, p)

                while d < q:
                    if g_to_power == gamma:
                        break
                    g_to_power = (g_to_power * g_base) % p
                    d += 1

                result_text += f"    Found d = {d} such that (g^((p-1)/{q}))^d ≡ gamma (mod p)\n"

                # Update x_q
                x_q = x_q + d * (q ** j)
                result_text += f"    Updated x_q = {x_q}\n"

            result_text += f"  Rezultat parțial: x ≡ {x_q} (mod {q_power})\n\n"
            chinese_remainder_equations.append(x_q)
            moduli.append(q_power)

        # Solve system using Chinese Remainder Theorem
        result_text += "Pasul 3: Aplicăm teorema chineză a resturilor pentru a rezolva sistemul:\n"
        for i in range(len(chinese_remainder_equations)):
            result_text += f"  x ≡ {chinese_remainder_equations[i]} (mod {moduli[i]})\n"

        from sympy.ntheory.modular import crt
        x, mod = crt(moduli, chinese_remainder_equations)

        result_text += f"\nSoluția: x = {x} (mod {mod})\n"
        result_text += f"Verificare: {g}^{x} mod {p} = {pow(g, x, p)} (trebuie să fie {a})\n"

        return result_text, x

    def solve_pohlig_hellman(self):
        try:
            a = int(self.value_entry.get())
            g = int(self.base_entry.get())
            p = int(self.modulus_entry.get())

            # Validate inputs
            if not sympy.isprime(p):
                self.output_text1.delete(1.0, tk.END)
                self.output_text1.insert(tk.END, f"Eroare: {p} nu este prim!")
                return

            result_text, x = self.pohlig_hellman(a, g, p)

            # Display result
            self.output_text1.delete(1.0, tk.END)
            self.output_text1.insert(tk.END, result_text)

        except Exception as e:
            self.output_text1.delete(1.0, tk.END)
            self.output_text1.insert(tk.END, f"Eroare: {str(e)}")

    def point_add(self, P, Q, a, b, p):
        """Add two points on an elliptic curve y^2 = x^3 + ax + b mod p"""
        if P == "O":
            return Q
        if Q == "O":
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and (y1 + y2) % p == 0:
            return "O"  # Point at infinity

        if x1 == x2 and y1 == y2:
            # Point doubling
            lam = (3 * x1 ** 2 + a) * mod_inverse(2 * y1, p) % p
        else:
            # Point addition
            lam = (y2 - y1) * mod_inverse((x2 - x1) % p, p) % p

        x3 = (lam ** 2 - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p

        return (x3, y3)

    def scalar_mult(self, k, P, a, b, p):
        """Multiply point P by scalar k on elliptic curve"""
        if k == 0 or P == "O":
            return "O"

        result = "O"
        addend = P

        while k > 0:
            if k & 1:
                result = self.point_add(result, addend, a, b, p)
            addend = self.point_add(addend, addend, a, b, p)
            k >>= 1

        return result

    def is_on_curve(self, point, a, b, p):
        """Check if point is on the elliptic curve y^2 = x^3 + ax + b mod p"""
        if point == "O":
            return True

        x, y = point
        return (y ** 2 % p) == (x ** 3 + a * x + b) % p

    def solve_elliptic_signature(self):
        try:
            # Parse parameters
            p = int(self.p_entry.get())
            q = int(self.q_entry.get())
            A = tuple(map(int, self.A_entry.get().split(',')))
            B = tuple(map(int, self.B_entry.get().split(',')))
            m = int(self.m_entry.get())
            message = int(self.message_entry.get())
            k = int(self.k_entry.get())

            # Elliptic curve parameters from example: y^2 = x^3 + x + 6
            a = 1
            b = 6

            result_text = "Aplicația 2: Semnătură folosind curba eliptică E: y² = x³ + x + 6 peste Z₁₁\n\n"
            result_text += f"Parametri:\n"
            result_text += f"- p = {p} (modulul pentru curba eliptică)\n"
            result_text += f"- q = {q} (ordinul subgrupului)\n"
            result_text += f"- A = {A} (punctul generator)\n"
            result_text += f"- B = {B} (punctul public)\n"
            result_text += f"- m = {m} (parametru)\n"
            result_text += f"- Mesaj x = {message}\n"
            result_text += f"- Valoare aleatoare k = {k}\n\n"

            # Verify points are on curve
            if not self.is_on_curve(A, a, b, p):
                result_text += f"Eroare: Punctul A {A} nu este pe curbă!\n"
                self.output_text2.delete(1.0, tk.END)
                self.output_text2.insert(tk.END, result_text)
                return

            if not self.is_on_curve(B, a, b, p):
                result_text += f"Eroare: Punctul B {B} nu este pe curbă!\n"
                self.output_text2.delete(1.0, tk.END)
                self.output_text2.insert(tk.END, result_text)
                return

            # Step 1: Compute kA
            kA = self.scalar_mult(k, A, a, b, p)
            result_text += f"Pasul 1: Calculăm kA = {k} * {A} = {kA}\n"

            # Step 2: Compute r = x-coordinate of kA mod q
            if kA == "O":
                result_text += "Eroare: kA este punctul la infinit, alegeți altă valoare pentru k\n"
                self.output_text2.delete(1.0, tk.END)
                self.output_text2.insert(tk.END, result_text)
                return

            r = kA[0] % q
            result_text += f"Pasul 2: r = x-coordonata lui kA mod q = {kA[0]} mod {q} = {r}\n"

            # Step 3: Compute s = k^(-1) * (SHA1(x) + m*r) mod q
            sha1_x = message  # Using message as SHA1(x) for simplicity
            inv_k = mod_inverse(k, q)
            s = (inv_k * (sha1_x + m * r)) % q
            result_text += f"Pasul 3: s = k^(-1) * (SHA1(x) + m*r) mod q\n"
            result_text += f"       = {inv_k} * ({sha1_x} + {m} * {r}) mod {q}\n"
            result_text += f"       = {inv_k} * {sha1_x + m * r} mod {q}\n"
            result_text += f"       = {s}\n\n"

            result_text += f"Semnătura rezultată: (r, s) = ({r}, {s})\n\n"

            # Verification
            result_text += "Verificare semnătură:\n"

            # Step 1: Compute w = s^(-1) mod q
            w = mod_inverse(s, q)
            result_text += f"Pasul 1: w = s^(-1) mod q = {w}\n"

            # Step 2: Compute u1 = SHA1(x) * w mod q
            u1 = (sha1_x * w) % q
            result_text += f"Pasul 2: u1 = SHA1(x) * w mod q = {sha1_x} * {w} mod {q} = {u1}\n"

            # Step 3: Compute u2 = r * w mod q
            u2 = (r * w) % q
            result_text += f"Pasul 3: u2 = r * w mod q = {r} * {w} mod {q} = {u2}\n"

            # Step 4: Compute u1*A + u2*B
            u1A = self.scalar_mult(u1, A, a, b, p)
            u2B = self.scalar_mult(u2, B, a, b, p)
            result_text += f"Pasul 4: u1*A = {u1} * {A} = {u1A}\n"
            result_text += f"         u2*B = {u2} * {B} = {u2B}\n"

            verification_point = self.point_add(u1A, u2B, a, b, p)
            result_text += f"         u1*A + u2*B = {verification_point}\n"

            # Step 5: Check if x-coordinate of (u1*A + u2*B) mod q equals r
            if verification_point == "O":
                is_valid = False
            else:
                is_valid = verification_point[0] % q == r

            result_text += f"Pasul 5: Verificăm dacă x-coordonata lui (u1*A + u2*B) mod q = r\n"
            result_text += f"         {verification_point[0]} mod {q} = {verification_point[0] % q}\n"
            result_text += f"         r = {r}\n"

            if is_valid:
                result_text += "\nSemnătura este VALIDĂ!"
            else:
                result_text += "\nSemnătura este INVALIDĂ!"

            # Display result
            self.output_text2.delete(1.0, tk.END)
            self.output_text2.insert(tk.END, result_text)

        except Exception as e:
            self.output_text2.delete(1.0, tk.END)
            self.output_text2.insert(tk.END, f"Eroare: {str(e)}")

    def elliptic_curve_factorization(self, n, a, start_point):
        """
        Implementation of Lenstra's Elliptic Curve Factorization Method
        """
        if n <= 1:
            return [n]

        if sympy.isprime(n):
            return [n]

        # Starting curve: y^2 = x^3 + ax + b
        x, y = start_point

        # Calculate b such that the starting point is on the curve
        b = (y ** 2 - x ** 3 - a * x) % n

        result_text = f"Aplicația 3: Factorizarea numărului n = {n} folosind curba eliptică\n\n"
        result_text += f"Ecuația curbei: y² = x³ + {a}x + {b} (mod {n})\n"
        result_text += f"Punctul inițial P = {start_point}\n\n"

        # Check if the point is on the curve
        if (y ** 2 - x ** 3 - a * x - b) % n != 0:
            result_text += "Eroare: Punctul inițial nu este pe curbă!"
            return result_text, None

        # Try to find a factor by scalar multiplication
        P = start_point
        i = 1

        result_text += "Începem calculul punctelor successive:\n"
        result_text += f"X₁ = P = {P}\n"

        max_iterations = 20  # Limit iterations to prevent infinite loops

        for j in range(2, max_iterations + 1):
            try:
                # Try to add P to itself
                numer = (3 * P[0] ** 2 + a) % n
                denom = (2 * P[1]) % n

                # Try to compute modular inverse, this is where factorization may happen
                try:
                    inv_denom = mod_inverse(denom, n)
                except ValueError:
                    # GCD is not 1, we found a factor!
                    factor = gcd(denom, n)
                    if 1 < factor < n:
                        result_text += f"\nGăsit factor la pasul {j}:\n"
                        result_text += f"Încercând să calculăm inversul lui {denom} modulo {n}\n"
                        result_text += f"gcd({denom}, {n}) = {factor}, care este un factor netrivial!\n\n"

                        # Get remaining factor
                        other_factor = n // factor

                        # Check if both are prime
                        factor_is_prime = sympy.isprime(factor)
                        other_is_prime = sympy.isprime(other_factor)

                        result_text += f"Factorizare: {n} = {factor} × {other_factor}\n"
                        result_text += f"Factorul {factor} este " + ("prim" if factor_is_prime else "compus") + "\n"
                        result_text += f"Factorul {other_factor} este " + (
                            "prim" if other_is_prime else "compus") + "\n"

                        return result_text, factor

                # If no factorization yet, continue with point addition
                slope = (numer * inv_denom) % n
                x_new = (slope ** 2 - 2 * P[0]) % n
                y_new = (slope * (P[0] - x_new) - P[1]) % n

                P = (x_new, y_new)
                result_text += f"X_{j} = {j}X₁ = {P}\n"

            except Exception as e:
                result_text += f"\nEroare la pasul {j}: {str(e)}\n"
                break

        result_text += "\nNu s-a găsit niciun factor după " + str(max_iterations) + " iterații.\n"
        result_text += "Încercați cu alți parametri sau cu un alt algoritm de factorizare."

        return result_text, None

    def solve_factorization(self):
        try:
            n = int(self.n_entry.get())
            a = int(self.a_coef_entry.get())
            start_point = tuple(map(int, self.point_entry.get().split(',')))

            result_text, factor = self.elliptic_curve_factorization(n, a, start_point)

            # Display result
            self.output_text3.delete(1.0, tk.END)
            self.output_text3.insert(tk.END, result_text)

        except Exception as e:
            self.output_text3.delete(1.0, tk.END)
            self.output_text3.insert(tk.END, f"Eroare: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoSolverApp(root)
    root.mainloop()