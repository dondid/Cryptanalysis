import tkinter as tk
from tkinter import scrolledtext, ttk
import string


class CipherApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Cipher Application")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f5fa")

        # Create tabs
        self.tab_control = ttk.Notebook(root)

        # Create three tabs for the three tasks
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Sarcina 1: Criptare Autocheia')
        self.tab_control.add(self.tab2, text='Sarcina 2: Decriptare Autocheia')
        self.tab_control.add(self.tab3, text='Sarcina 3: Cheie Fluidă')

        self.tab_control.pack(expand=1, fill="both")

        # Set up each tab
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

    def setup_tab1(self):
        # Frame for input controls
        input_frame = tk.Frame(self.tab1, bg="#f0f5fa", padx=10, pady=10)
        input_frame.pack(fill="x")

        # Input text
        tk.Label(input_frame, text="Text de criptat:", bg="#f0f5fa").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.input_text1 = tk.Entry(input_frame, width=40)
        self.input_text1.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.input_text1.insert(0, "CRIPTANALIZA")

        # Key input
        tk.Label(input_frame, text="Cheia K:", bg="#f0f5fa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.key_input1 = tk.Entry(input_frame, width=10)
        self.key_input1.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.key_input1.insert(0, "13")

        # Encrypt button
        self.encrypt_button = tk.Button(input_frame, text="Criptează", command=self.encrypt_tab1, bg="#4CAF50",
                                        fg="white", padx=10)
        self.encrypt_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Result display
        tk.Label(self.tab1, text="Rezultat:", bg="#f0f5fa").pack(anchor="w", padx=15)
        self.result_display1 = scrolledtext.ScrolledText(self.tab1, width=90, height=5)
        self.result_display1.pack(padx=15, pady=5, fill="both")

        # Step-by-step explanation
        tk.Label(self.tab1, text="Explicație pas cu pas:", bg="#f0f5fa").pack(anchor="w", padx=15, pady=(10, 0))
        self.explanation1 = scrolledtext.ScrolledText(self.tab1, width=90, height=15)
        self.explanation1.pack(padx=15, pady=5, fill="both", expand=True)

    def setup_tab2(self):
        # Frame for input controls
        input_frame = tk.Frame(self.tab2, bg="#f0f5fa", padx=10, pady=10)
        input_frame.pack(fill="x")

        # Input text
        tk.Label(input_frame, text="Text criptat:", bg="#f0f5fa").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.input_text2 = tk.Entry(input_frame, width=40)
        self.input_text2.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.input_text2.insert(0, "OIKEV ZRKS")

        # Key input
        tk.Label(input_frame, text="Cheia K:", bg="#f0f5fa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.key_input2 = tk.Entry(input_frame, width=10)
        self.key_input2.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.key_input2.insert(0, "13")

        # Decrypt button
        self.decrypt_button = tk.Button(input_frame, text="Decriptează", command=self.decrypt_tab2, bg="#2196F3",
                                        fg="white", padx=10)
        self.decrypt_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Result display
        tk.Label(self.tab2, text="Rezultat:", bg="#f0f5fa").pack(anchor="w", padx=15)
        self.result_display2 = scrolledtext.ScrolledText(self.tab2, width=90, height=5)
        self.result_display2.pack(padx=15, pady=5, fill="both")

        # Step-by-step explanation
        tk.Label(self.tab2, text="Explicație pas cu pas:", bg="#f0f5fa").pack(anchor="w", padx=15, pady=(10, 0))
        self.explanation2 = scrolledtext.ScrolledText(self.tab2, width=90, height=15)
        self.explanation2.pack(padx=15, pady=5, fill="both", expand=True)

    def setup_tab3(self):
        # Frame for input controls
        input_frame = tk.Frame(self.tab3, bg="#f0f5fa", padx=10, pady=10)
        input_frame.pack(fill="x")

        # Input text
        tk.Label(input_frame, text="Text de criptat:", bg="#f0f5fa").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.input_text3 = tk.Entry(input_frame, width=40)
        self.input_text3.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.input_text3.insert(0, "CRIPTANALIZA")

        # Key input
        tk.Label(input_frame, text="Cheia K:", bg="#f0f5fa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.key_input3 = tk.Entry(input_frame, width=10)
        self.key_input3.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.key_input3.insert(0, "13")

        # Encrypt button
        self.encrypt_button3 = tk.Button(input_frame, text="Criptează", command=self.encrypt_tab3, bg="#9C27B0",
                                         fg="white", padx=10)
        self.encrypt_button3.grid(row=2, column=0, columnspan=2, pady=10)

        # Result display
        tk.Label(self.tab3, text="Rezultat:", bg="#f0f5fa").pack(anchor="w", padx=15)
        self.result_display3 = scrolledtext.ScrolledText(self.tab3, width=90, height=5)
        self.result_display3.pack(padx=15, pady=5, fill="both")

        # Step-by-step explanation
        tk.Label(self.tab3, text="Explicație pas cu pas:", bg="#f0f5fa").pack(anchor="w", padx=15, pady=(10, 0))
        self.explanation3 = scrolledtext.ScrolledText(self.tab3, width=90, height=15)
        self.explanation3.pack(padx=15, pady=5, fill="both", expand=True)

    def encrypt_tab1(self):
        # Get inputs
        plaintext = self.input_text1.get().upper().replace(" ", "")
        key = int(self.key_input1.get())

        # Create alphabet (Romanian alphabet could be used instead if needed)
        alphabet = string.ascii_uppercase

        # Encryption with auto-key
        encrypted = ""
        key_sequence = [key]  # Starting with the initial key
        explanation = "Algoritmul de criptare cu auto-cheie (cheia inițială K = {})\n\n".format(key)
        explanation += "Alfabetul utilizat: {}\n\n".format(alphabet)
        explanation += "Pasul 1: Se inițializează cheia cu valoarea {} și se construiește secvența de chei.\n".format(
            key)
        explanation += "Pasul 2: Pentru fiecare literă din textul clar, se adună poziția literei cu valoarea cheii corespunzătoare (modulo 26).\n\n"
        explanation += "Procesul pas cu pas:\n"

        for i, char in enumerate(plaintext):
            if char in alphabet:
                # Find position in alphabet (0-25)
                p_i = alphabet.index(char)

                # Calculate ciphertext character position
                c_i = (p_i + key_sequence[i]) % 26

                # Get the ciphertext character
                encrypted_char = alphabet[c_i]
                encrypted += encrypted_char

                # Next key is the position value of the plaintext character
                if i < len(plaintext) - 1:
                    key_sequence.append(p_i)

                # Add explanation for this character
                explanation += "Litera {}: {} (poziția {}) + cheie {} = {} (poziția {}) = {}\n".format(
                    i + 1, char, p_i, key_sequence[i], (p_i + key_sequence[i]), c_i, encrypted_char)
            else:
                encrypted += char

        # Display results
        self.result_display1.delete(1.0, tk.END)
        self.result_display1.insert(tk.END, encrypted)

        # Display explanation
        self.explanation1.delete(1.0, tk.END)
        self.explanation1.insert(tk.END, explanation)

        # Add key sequence to explanation
        self.explanation1.insert(tk.END, "\nSecvența completă de chei: {}\n".format(key_sequence))

    def decrypt_tab2(self):
        # Get inputs
        ciphertext = self.input_text2.get().upper().replace(" ", "")
        key = int(self.key_input2.get())

        # Create alphabet
        alphabet = string.ascii_uppercase

        # Decryption with auto-key
        decrypted = ""
        key_sequence = [key]  # Starting with the initial key
        explanation = "Algoritmul de decriptare cu auto-cheie (cheia inițială K = {})\n\n".format(key)
        explanation += "Alfabetul utilizat: {}\n\n".format(alphabet)
        explanation += "Pasul 1: Se inițializează cheia cu valoarea {} și se construiește secvența de chei.\n".format(
            key)
        explanation += "Pasul 2: Pentru fiecare literă din textul criptat, se scade valoarea cheii corespunzătoare (modulo 26).\n\n"
        explanation += "Procesul pas cu pas:\n"

        for i, char in enumerate(ciphertext):
            if char in alphabet:
                # Find position in alphabet (0-25)
                c_i = alphabet.index(char)

                # Calculate plaintext character position
                p_i = (c_i - key_sequence[i]) % 26

                # Get the plaintext character
                decrypted_char = alphabet[p_i]
                decrypted += decrypted_char

                # Next key is the position value of the plaintext character
                if i < len(ciphertext) - 1:
                    key_sequence.append(p_i)

                # Add explanation for this character
                explanation += "Litera {}: {} (poziția {}) - cheie {} = {} (poziția {}) = {}\n".format(
                    i + 1, char, c_i, key_sequence[i], (c_i - key_sequence[i]), p_i, decrypted_char)
            else:
                decrypted += char

        # Display results
        self.result_display2.delete(1.0, tk.END)
        self.result_display2.insert(tk.END, decrypted)

        # Display explanation
        self.explanation2.delete(1.0, tk.END)
        self.explanation2.insert(tk.END, explanation)

        # Add key sequence to explanation
        self.explanation2.insert(tk.END, "\nSecvența completă de chei: {}\n".format(key_sequence))

    def encrypt_tab3(self):
        # Get inputs
        plaintext = self.input_text3.get().upper().replace(" ", "")
        key = int(self.key_input3.get())

        # Create alphabet
        alphabet = string.ascii_uppercase

        # Encryption with fluid key
        encrypted = ""
        key_sequence = [key]  # Starting with the initial key
        explanation = "Algoritmul de criptare cu cheie fluidă (cheia inițială K = {})\n\n".format(key)
        explanation += "Alfabetul utilizat: {}\n\n".format(alphabet)
        explanation += "Pasul 1: Se inițializează cheia cu valoarea {}.\n".format(key)
        explanation += "Pasul 2: Se generează cheia fluidă folosind formula: z₁ = K, zᵢ = mᵢ₋₁, i ≥ 2\n"
        explanation += "Pasul 3: Pentru fiecare literă din textul clar, se adună poziția literei cu valoarea cheii corespunzătoare (modulo 26).\n\n"
        explanation += "Procesul pas cu pas:\n"

        for i, char in enumerate(plaintext):
            if char in alphabet:
                # Find position in alphabet (0-25)
                p_i = alphabet.index(char)

                # Calculate ciphertext character position
                c_i = (p_i + key_sequence[i]) % 26

                # Get the ciphertext character
                encrypted_char = alphabet[c_i]
                encrypted += encrypted_char

                # Next key is the position value of the previous plaintext character
                if i < len(plaintext) - 1:
                    key_sequence.append(p_i)

                # Add explanation for this character
                explanation += "Litera {}: {} (poziția {}) + cheie {} = {} (poziția {}) = {}\n".format(
                    i + 1, char, p_i, key_sequence[i], (p_i + key_sequence[i]), c_i, encrypted_char)
            else:
                encrypted += char

        # Display results
        self.result_display3.delete(1.0, tk.END)
        self.result_display3.insert(tk.END, encrypted)

        # Display explanation
        self.explanation3.delete(1.0, tk.END)
        self.explanation3.insert(tk.END, explanation)

        # Add key sequence to explanation
        self.explanation3.insert(tk.END, "\nSecvența completă de chei: {}\n".format(key_sequence))
        self.explanation3.insert(tk.END,
                                 "\nObservație: Aceasta este o cheie fluidă, deoarece fiecare element al cheii depinde de caracterul anterior din textul clar.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApplication(root)
    root.mainloop()