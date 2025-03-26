import tkinter as tk
from tkinter import ttk, messagebox
import string


class CryptographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Cryptography Tools")
        master.geometry("800x600")

        # Styles
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.create_caesar_tab()
        self.create_vigenere_tab()
        self.create_transposition_tab()
        self.create_custom_cipher_tab()

    def create_caesar_tab(self):
        # Caesar Cipher Tab
        caesar_frame = ttk.Frame(self.notebook)
        self.notebook.add(caesar_frame, text="Caesar Cipher")

        # Input section
        ttk.Label(caesar_frame, text="Text:").pack(pady=(10, 0))
        self.caesar_input = tk.Text(caesar_frame, height=3, width=50)
        self.caesar_input.pack()

        ttk.Label(caesar_frame, text="Shift Value (k):").pack()
        self.caesar_shift = ttk.Entry(caesar_frame, width=10)
        self.caesar_shift.pack()

        # Buttons frame
        btn_frame = ttk.Frame(caesar_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Encrypt", command=self.caesar_encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Decrypt", command=self.caesar_decrypt).pack(side=tk.LEFT, padx=5)

        # Result section
        self.caesar_result_label = ttk.Label(caesar_frame, text="Result:", font=("Arial", 12, "bold"))
        self.caesar_result_label.pack()
        self.caesar_result = tk.Text(caesar_frame, height=3, width=50, state='disabled')
        self.caesar_result.pack()

        # Step-by-step explanation
        self.caesar_steps = tk.Text(caesar_frame, height=5, width=50, state='disabled')
        self.caesar_steps.pack(pady=10)

    def create_vigenere_tab(self):
        # Vigenère Cipher Tab
        vigenere_frame = ttk.Frame(self.notebook)
        self.notebook.add(vigenere_frame, text="Vigenère Cipher")

        # Input section
        ttk.Label(vigenere_frame, text="Text:").pack(pady=(10, 0))
        self.vigenere_input = tk.Text(vigenere_frame, height=3, width=50)
        self.vigenere_input.pack()

        ttk.Label(vigenere_frame, text="Key:").pack()
        self.vigenere_key = ttk.Entry(vigenere_frame, width=30)
        self.vigenere_key.pack()

        # Buttons frame
        btn_frame = ttk.Frame(vigenere_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Encrypt", command=self.vigenere_encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Decrypt", command=self.vigenere_decrypt).pack(side=tk.LEFT, padx=5)

        # Result section
        self.vigenere_result_label = ttk.Label(vigenere_frame, text="Result:", font=("Arial", 12, "bold"))
        self.vigenere_result_label.pack()
        self.vigenere_result = tk.Text(vigenere_frame, height=3, width=50, state='disabled')
        self.vigenere_result.pack()

        # Step-by-step explanation
        self.vigenere_steps = tk.Text(vigenere_frame, height=5, width=50, state='disabled')
        self.vigenere_steps.pack(pady=10)

    def create_transposition_tab(self):
        # Transposition Cipher Tab
        transposition_frame = ttk.Frame(self.notebook)
        self.notebook.add(transposition_frame, text="Transposition Cipher")

        # Input section
        ttk.Label(transposition_frame, text="Text:").pack(pady=(10, 0))
        self.transposition_input = tk.Text(transposition_frame, height=3, width=50)
        self.transposition_input.pack()

        ttk.Label(transposition_frame, text="Permutation Key (comma-separated indices):").pack()
        self.transposition_key = ttk.Entry(transposition_frame, width=30)
        self.transposition_key.pack()

        # Buttons frame
        btn_frame = ttk.Frame(transposition_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Encrypt", command=self.transposition_encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Decrypt", command=self.transposition_decrypt).pack(side=tk.LEFT, padx=5)

        # Result section
        self.transposition_result_label = ttk.Label(transposition_frame, text="Result:", font=("Arial", 12, "bold"))
        self.transposition_result_label.pack()
        self.transposition_result = tk.Text(transposition_frame, height=3, width=50, state='disabled')
        self.transposition_result.pack()

        # Step-by-step explanation
        self.transposition_steps = tk.Text(transposition_frame, height=5, width=50, state='disabled')
        self.transposition_steps.pack(pady=10)

    def create_custom_cipher_tab(self):
        # Custom Cipher Tab
        custom_frame = ttk.Frame(self.notebook)
        self.notebook.add(custom_frame, text="Create Custom Cipher")

        # Input for custom cipher creation
        ttk.Label(custom_frame, text="Cipher Name:").pack()
        self.custom_name = ttk.Entry(custom_frame, width=30)
        self.custom_name.pack()

        ttk.Label(custom_frame, text="Encryption Function (Python code):").pack()
        self.custom_encrypt_func = tk.Text(custom_frame, height=5, width=50)
        self.custom_encrypt_func.pack()

        ttk.Label(custom_frame, text="Decryption Function (Python code):").pack()
        self.custom_decrypt_func = tk.Text(custom_frame, height=5, width=50)
        self.custom_decrypt_func.pack()

        # Add custom cipher button
        ttk.Button(custom_frame, text="Add Custom Cipher", command=self.add_custom_cipher).pack(pady=10)

    def caesar_encrypt(self):
        try:
            # Get input and shift
            text = self.caesar_input.get("1.0", tk.END).strip().upper()
            k = int(self.caesar_shift.get())

            # Validate input
            if not text:
                messagebox.showerror("Error", "Please enter text to encrypt")
                return

            # Encryption steps
            steps = ["Caesar Cipher Encryption Steps:"]
            result = ""
            for char in text:
                if char.isalpha():
                    # Calculate new position
                    new_pos = (ord(char) - ord('A') + k) % 26
                    new_char = chr(new_pos + ord('A'))
                    steps.append(f"'{char}' -> Shift {k} -> '{new_char}'")
                    result += new_char
                else:
                    result += char

            # Update result and steps
            self.update_result(self.caesar_result, result)
            self.update_steps(self.caesar_steps, "\n".join(steps))

        except ValueError:
            messagebox.showerror("Error", "Invalid shift value. Please enter a number.")

    def caesar_decrypt(self):
        try:
            # Get input and shift
            text = self.caesar_input.get("1.0", tk.END).strip().upper()
            k = int(self.caesar_shift.get())

            # Validate input
            if not text:
                messagebox.showerror("Error", "Please enter text to decrypt")
                return

            # Decryption steps
            steps = ["Caesar Cipher Decryption Steps:"]
            result = ""
            for char in text:
                if char.isalpha():
                    # Calculate original position
                    new_pos = (ord(char) - ord('A') - k) % 26
                    new_char = chr(new_pos + ord('A'))
                    steps.append(f"'{char}' -> Reverse Shift {k} -> '{new_char}'")
                    result += new_char
                else:
                    result += char

            # Update result and steps
            self.update_result(self.caesar_result, result)
            self.update_steps(self.caesar_steps, "\n".join(steps))

        except ValueError:
            messagebox.showerror("Error", "Invalid shift value. Please enter a number.")

    def vigenere_encrypt(self):
        try:
            # Get input and key
            text = self.vigenere_input.get("1.0", tk.END).strip().upper()
            key = self.vigenere_key.get().upper()

            # Validate input
            if not text or not key:
                messagebox.showerror("Error", "Please enter text and key")
                return

            # Encryption steps
            steps = ["Vigenère Cipher Encryption Steps:"]
            result = ""
            key_length = len(key)

            for i, char in enumerate(text):
                if char.isalpha():
                    # Use corresponding key character for shift
                    key_char = key[i % key_length]
                    shift = ord(key_char) - ord('A')

                    # Calculate new position
                    new_pos = (ord(char) - ord('A') + shift) % 26
                    new_char = chr(new_pos + ord('A'))

                    steps.append(f"'{char}' (Key: '{key_char}', Shift: {shift}) -> '{new_char}'")
                    result += new_char
                else:
                    result += char

            # Update result and steps
            self.update_result(self.vigenere_result, result)
            self.update_steps(self.vigenere_steps, "\n".join(steps))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def vigenere_decrypt(self):
        try:
            # Get input and key
            text = self.vigenere_input.get("1.0", tk.END).strip().upper()
            key = self.vigenere_key.get().upper()

            # Validate input
            if not text or not key:
                messagebox.showerror("Error", "Please enter text and key")
                return

            # Decryption steps
            steps = ["Vigenère Cipher Decryption Steps:"]
            result = ""
            key_length = len(key)

            for i, char in enumerate(text):
                if char.isalpha():
                    # Use corresponding key character for shift
                    key_char = key[i % key_length]
                    shift = ord(key_char) - ord('A')

                    # Calculate original position
                    new_pos = (ord(char) - ord('A') - shift) % 26
                    new_char = chr(new_pos + ord('A'))

                    steps.append(f"'{char}' (Key: '{key_char}', Reverse Shift: {shift}) -> '{new_char}'")
                    result += new_char
                else:
                    result += char

            # Update result and steps
            self.update_result(self.vigenere_result, result)
            self.update_steps(self.vigenere_steps, "\n".join(steps))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transposition_encrypt(self):
        try:
            # Get input and key
            text = self.transposition_input.get("1.0", tk.END).strip().upper()
            key_str = self.transposition_key.get()

            # Convert key to list of indices
            key = [int(x.strip()) - 1 for x in key_str.split(',')]

            # Validate input
            if not text or not key:
                messagebox.showerror("Error", "Please enter text and key")
                return

            # Padding
            cols = len(key)
            rows = (len(text) + cols - 1) // cols
            text += 'Q' * (rows * cols - len(text))

            # Create grid
            grid = [text[i:i + cols] for i in range(0, len(text), cols)]

            # Encryption steps
            steps = ["Transposition Cipher Encryption Steps:"]
            steps.append("Original Grid:")
            for row in grid:
                steps.append(row)

            # Permute columns
            result = ""
            for col in sorted(range(len(key)), key=lambda k: key[k]):
                for row in grid:
                    result += row[col]

            steps.append("\nFinal Encrypted Text:")
            steps.append(result)

            # Update result and steps
            self.update_result(self.transposition_result, result)
            self.update_steps(self.transposition_steps, "\n".join(steps))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transposition_decrypt(self):
        try:
            # Get input and key
            text = self.transposition_input.get("1.0", tk.END).strip().upper()
            key_str = self.transposition_key.get()

            # Convert key to list of indices
            key = [int(x.strip()) - 1 for x in key_str.split(',')]

            # Validate input
            if not text or not key:
                messagebox.showerror("Error", "Please enter text and key")
                return

            # Calculate grid dimensions
            cols = len(key)
            rows = len(text) // cols

            # Create inverse permutation
            inv_key = [key.index(i) for i in range(len(key))]

            # Create grid for decryption
            grid = [''] * cols
            start = 0

            # Decryption steps
            steps = ["Transposition Cipher Decryption Steps:"]
            steps.append("Rearranging Columns:")

            for i in range(cols):
                col_length = rows
                grid[inv_key[i]] = text[start:start + col_length]
                start += col_length

            # Reconstruct original text
            result = ''
            for i in range(rows):
                for j in range(cols):
                    result += grid[j][i]

            # Remove padding
            result = result.rstrip('Q')

            steps.append("\nDecrypted Text:")
            steps.append(result)

            # Update result and steps
            self.update_result(self.transposition_result, result)
            self.update_steps(self.transposition_steps, "\n".join(steps))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_custom_cipher(self):
        try:
            name = self.custom_name.get()
            encrypt_code = self.custom_encrypt_func.get("1.0", tk.END).strip()
            decrypt_code = self.custom_decrypt_func.get("1.0", tk.END).strip()

            # Validate input
            if not name or not encrypt_code or not decrypt_code:
                messagebox.showerror("Error", "Please fill all fields")
                return

            # Compile and validate functions
            encrypt_locals = {}
            decrypt_locals = {}

            exec(f"def custom_encrypt(text):\n{encrypt_code}", {}, encrypt_locals)
            exec(f"def custom_decrypt(text):\n{decrypt_code}", {}, decrypt_locals)

            # Create a new tab for the custom cipher
            custom_frame = ttk.Frame(self.notebook)
            self.notebook.add(custom_frame, text=name)

            # Create widgets for the custom cipher tab
            ttk.Label(custom_frame, text="Text:").pack(pady=(10, 0))
            input_text = tk.Text(custom_frame, height=3, width=50)
            input_text.pack()

            # Buttons frame
            btn_frame = ttk.Frame(custom_frame)
            btn_frame.pack(pady=10)

            result_label = ttk.Label(custom_frame, text="Result:", font=("Arial", 12, "bold"))
            result_label.pack()
            result_text = tk.Text(custom_frame, height=3, width=50, state='disabled')
            result_text.pack()

            steps_text = tk.Text(custom_frame, height=5, width=50, state='disabled')
            steps_text.pack(pady=10)

            # Encryption function
            def custom_encrypt_handler():
                try:
                    text = input_text.get("1.0", tk.END).strip()
                    result = encrypt_locals['custom_encrypt'](text)
                    self.update_result(result_text, result)
                    self.update_steps(steps_text, "Custom Encryption Applied")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            # Decryption function
            def custom_decrypt_handler():
                try:
                    text = input_text.get("1.0", tk.END).strip()
                    result = decrypt_locals['custom_decrypt'](text)
                    self.update_result(result_text, result)
                    self.update_steps(steps_text, "Custom Decryption Applied")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            # Add buttons
            ttk.Button(btn_frame, text="Encrypt", command=custom_encrypt_handler).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Decrypt", command=custom_decrypt_handler).pack(side=tk.LEFT, padx=5)

            messagebox.showinfo("Success", f"Custom cipher '{name}' added successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add custom cipher: {str(e)}")

    def update_result(self, result_widget, text):
        # Helper method to update result text widget
        result_widget.config(state='normal')
        result_widget.delete('1.0', tk.END)
        result_widget.insert(tk.END, text)
        result_widget.config(state='disabled')

    def update_steps(self, steps_widget, text):
        # Helper method to update steps text widget
        steps_widget.config(state='normal')
        steps_widget.delete('1.0', tk.END)
        steps_widget.insert(tk.END, text)
        steps_widget.config(state='disabled')


def main():
    root = tk.Tk()
    app = CryptographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()