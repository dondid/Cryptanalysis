import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk


class KnapsackCryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criptare Knapsack Supercrescător")

        # Datele problemei
        self.super_knapsack = [2, 11, 14, 28, 57, 113, 229, 457, 918, 1829]
        self.m = 3837
        self.q = 1001

        # Interfață grafică
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titlu
        title_label = tk.Label(main_frame, text="Criptare Knapsack Supercrescător", font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)

        # Notebook pentru organizarea conținutului
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab pentru explicații
        self.create_explanation_tab()

        # Tab pentru exemplu predefinit
        self.create_example_tab()

        # Tab pentru criptare personalizată
        self.create_custom_tab()

    def create_explanation_tab(self):
        # Tab cu explicații matematice
        explanation_tab = ttk.Frame(self.notebook)
        self.notebook.add(explanation_tab, text="Explicații")

        explanation_text = """
## Algoritmul Knapsack Supercrescător

1. **Knapsack Supercrescător**: 
   - Secvență de numere unde fiecare element > suma precedentelor
   - Secvența noastră: [2, 11, 14, 28, 57, 113, 229, 457, 918, 1829]
   - Verificare: 11 > 2, 14 > 2+11, 28 > 2+11+14, etc.

2. **Parametrii Criptare**:
   - m = 3837 (trebuie m > 2*a10 = 2*1829 = 3658)
   - q = 1001 (trebuie coprim cu m, cmmdc(1001,3837)=1)

3. **Knapsack Public**:
   - Se calculează b_i = (a_i * q) mod m pentru fiecare element
   - Exemplu: b1 = (2 * 1001) mod 3837 = 2002 mod 3837 = 2002

4. **Procesul de Criptare**:
   - Convertim textul în binar (8 biți per caracter)
   - Grupăm biții în blocuri de 10
   - Pentru fiecare bloc, calculăm suma elementelor corespunzătoare biților 1
        """
        explanation_label = tk.Label(explanation_tab, text=explanation_text, justify=tk.LEFT, font=('Arial', 10))
        explanation_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def create_example_tab(self):
        # Tab cu exemplul predefinit
        example_tab = ttk.Frame(self.notebook)
        self.notebook.add(example_tab, text="Exemplu Predefinit")

        # Mesaj predefinit
        example_label = tk.Label(example_tab, text="Mesaj predefinit: 'REPLY IMMEDIATELY'", font=('Arial', 10))
        example_label.pack(pady=5)

        # Buton pentru rularea exemplului
        run_button = tk.Button(example_tab, text="Criptează Exemplul", command=self.run_example)
        run_button.pack(pady=5)

        # Zona de rezultate
        self.example_result = scrolledtext.ScrolledText(example_tab, height=15, width=80, wrap=tk.WORD)
        self.example_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_custom_tab(self):
        # Tab pentru criptare personalizată
        custom_tab = ttk.Frame(self.notebook)
        self.notebook.add(custom_tab, text="Criptare Personalizată")

        # Etichetă și câmp de introducere
        tk.Label(custom_tab, text="Introduceți mesajul pentru criptare:").pack(pady=5)

        self.custom_entry = tk.Entry(custom_tab, width=50)
        self.custom_entry.pack(pady=5)

        # Buton de criptare
        encrypt_button = tk.Button(custom_tab, text="Criptează Mesaj", command=self.encrypt_custom)
        encrypt_button.pack(pady=5)

        # Zona de rezultate
        self.custom_result = scrolledtext.ScrolledText(custom_tab, height=15, width=80, wrap=tk.WORD)
        self.custom_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def modinv(self, a, m):
        # Calcul invers modular
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            return None  # Nu există invers
        else:
            return x % m

    def extended_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def create_public_knapsack(self):
        # Generează knapsack-ul public
        return [(a * self.q) % self.m for a in self.super_knapsack]

    def text_to_bits(self, text):
        # Converteste textul în șir de biți
        bits = []
        for char in text:
            # Obține codul ASCII și convertește în binar pe 8 biți
            bits.extend([int(b) for b in format(ord(char), '08b')])
        return bits

    def pad_bits(self, bits):
        # Completează biții cu zerouri pentru a avea multiplu de 10
        pad_length = (10 - (len(bits) % 10)) % 10
        return bits + [0] * pad_length

    def encrypt_message(self, message):
        # Converteste mesajul în biți
        bits = self.text_to_bits(message)
        padded_bits = self.pad_bits(bits)

        # Generează knapsack-ul public
        public_knapsack = self.create_public_knapsack()

        # Împarte biții în blocuri de 10
        blocks = [padded_bits[i:i + 10] for i in range(0, len(padded_bits), 10)]

        # Criptează fiecare bloc
        ciphertext = []
        for block in blocks:
            # Calculează suma elementelor corespunzătoare biților 1
            s = sum(public_knapsack[i] for i in range(10) if block[i] == 1)
            ciphertext.append(s)

        return ciphertext, bits, padded_bits, blocks, public_knapsack

    def display_encryption_results(self, text_widget, message, ciphertext, bits, padded_bits, blocks, public_knapsack):
        # Afișează rezultatele în widget-ul text specificat
        text_widget.delete(1.0, tk.END)

        text_widget.insert(tk.END, "=== Detalii Criptare ===\n\n", 'bold')

        # Afișează knapsack-ul public
        text_widget.insert(tk.END, "Knapsack Public (b_i = a_i * q mod m):\n")
        for i, (a, b) in enumerate(zip(self.super_knapsack, public_knapsack)):
            text_widget.insert(tk.END, f"b_{i + 1} = ({a} * {self.q}) mod {self.m} = {b}\n")
        text_widget.insert(tk.END, "\n")

        # Afișează conversia mesajului în biți
        text_widget.insert(tk.END, f"Mesaj original: '{message}'\n")
        text_widget.insert(tk.END, f"Cod ASCII (8 biți per caracter):\n")

        # Afișează fiecare caracter cu reprezentarea sa binară
        for char in message:
            text_widget.insert(tk.END, f"'{char}': {format(ord(char), '08b')}\n")

        text_widget.insert(tk.END, "\nȘir de biți complet:\n")
        text_widget.insert(tk.END, ' '.join(map(str, bits)) + "\n")

        text_widget.insert(tk.END, "\nȘir de biți completat (pentru multiplu de 10):\n")
        text_widget.insert(tk.END, ' '.join(map(str, padded_bits)) + "\n")

        text_widget.insert(tk.END, "\nBlocuri de 10 biți:\n")
        for i, block in enumerate(blocks):
            text_widget.insert(tk.END, f"Bloc {i + 1}: {' '.join(map(str, block))}\n")

        text_widget.insert(tk.END, "\nCriptare blocuri:\n")
        for i, (block, c) in enumerate(zip(blocks, ciphertext)):
            selected = [public_knapsack[j] for j in range(10) if block[j] == 1]
            text_widget.insert(tk.END, f"Bloc {i + 1}: {' + '.join(map(str, selected))} = {c}\n")

        text_widget.insert(tk.END, "\n=== Rezultat Final ===\n", 'bold')
        text_widget.insert(tk.END, f"Text cifrat: {' '.join(map(str, ciphertext))}\n")

        # Configurează tag-uri pentru formatare
        text_widget.tag_config('bold', font=('Arial', 10, 'bold'))

    def run_example(self):
        message = "REPLY IMMEDIATELY"

        # Obține rezultatele criptării
        ciphertext, bits, padded_bits, blocks, public_knapsack = self.encrypt_message(message)

        # Afișează rezultatele
        self.display_encryption_results(
            self.example_result, message, ciphertext,
            bits, padded_bits, blocks, public_knapsack
        )

    def encrypt_custom(self):
        message = self.custom_entry.get()

        if not message:
            messagebox.showwarning("Avertisment", "Introduceți un mesaj pentru criptare!")
            return

        try:
            # Obține rezultatele criptării
            ciphertext, bits, padded_bits, blocks, public_knapsack = self.encrypt_message(message)

            # Afișează rezultatele
            self.display_encryption_results(
                self.custom_result, message, ciphertext,
                bits, padded_bits, blocks, public_knapsack
            )
        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")


# Rularea aplicației
if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackCryptoApp(root)
    root.geometry("850x700")
    root.mainloop()