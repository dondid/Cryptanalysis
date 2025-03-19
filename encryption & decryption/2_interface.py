import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np


# Original functions from the provided code with fixes
def get_inverse_permutation(perm):
    n = len(perm)
    inverse = [0] * n
    for i, p in enumerate(perm):
        inverse[p - 1] = i + 1
    return inverse


def encrypt(text, perm):
    text = text.replace(" ", "W")  # Replace space with 'W'
    n = len(perm)
    blocks = [text[i:i + n] for i in range(0, len(text), n)]
    encrypted_text = ""
    for block in blocks:
        block = block.ljust(n, "X")  # Padding with 'X' if needed
        encrypted_block = "".join(block[perm[i] - 1] for i in range(n))
        encrypted_text += encrypted_block
    return encrypted_text


def decrypt(encrypted_text, perm):
    inverse_perm = get_inverse_permutation(perm)
    n = len(perm)
    # Make sure the encrypted text length is a multiple of n
    if len(encrypted_text) % n != 0:
        encrypted_text = encrypted_text.ljust((len(encrypted_text) // n + 1) * n, "X")

    blocks = [encrypted_text[i:i + n] for i in range(0, len(encrypted_text), n)]
    decrypted_text = ""
    for block in blocks:
        # Ensure block is exactly n characters
        if len(block) < n:
            block = block.ljust(n, "X")  # Padding with 'X' if needed
        decrypted_block = "".join(block[inverse_perm[i] - 1] for i in range(n))
        decrypted_text += decrypted_block
    return decrypted_text.replace("W", " ").rstrip("X")  # Restore spaces and remove padding


# Playfair cipher functions
def generate_playfair_matrix(keyword):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    keyword = "".join(dict.fromkeys(keyword.upper().replace("J", "I")))
    matrix_string = keyword + "".join([c for c in alphabet if c not in keyword])
    return [list(matrix_string[i:i + 5]) for i in range(0, 25, 5)]


def find_position(matrix, letter):
    letter = letter.upper()
    # Replace J with I as per Playfair rules
    if letter == 'J':
        letter = 'I'
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None


def encrypt_playfair(plaintext, keyword):
    matrix = generate_playfair_matrix(keyword)
    ciphertext = ""
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")

    # If plaintext length is odd, add an 'X' at the end
    if len(plaintext) % 2 != 0:
        plaintext += "X"

    # Process pairs of letters
    i = 0
    while i < len(plaintext):
        if i + 1 >= len(plaintext):
            # Add an X if we're at the last character
            a, b = plaintext[i], 'X'
        else:
            a, b = plaintext[i], plaintext[i + 1]

        # If pair contains same letter, insert 'X' between them
        if a == b:
            a, b = a, 'X'
            i += 1  # Only increment by 1 since we're using X as the second character
        else:
            i += 2  # Normal case, increment by 2

        pos_a = find_position(matrix, a)
        pos_b = find_position(matrix, b)

        if pos_a is None or pos_b is None:
            # Skip characters not in the matrix
            continue

        row_a, col_a = pos_a
        row_b, col_b = pos_b

        if row_a == row_b:  # Same row
            ciphertext += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:  # Same column
            ciphertext += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:  # Rectangle
            ciphertext += matrix[row_a][col_b] + matrix[row_b][col_a]

    return ciphertext


def decrypt_playfair(ciphertext, keyword):
    matrix = generate_playfair_matrix(keyword)
    plaintext = ""
    ciphertext = ciphertext.upper().replace(" ", "")

    # Process pairs of letters
    i = 0
    while i < len(ciphertext):
        if i + 1 >= len(ciphertext):
            # Add an X if we're at the last character (shouldn't happen in a valid ciphertext)
            a, b = ciphertext[i], 'X'
        else:
            a, b = ciphertext[i], ciphertext[i + 1]

        pos_a = find_position(matrix, a)
        pos_b = find_position(matrix, b)

        if pos_a is None or pos_b is None:
            # Skip characters not in the matrix
            i += 1
            continue

        row_a, col_a = pos_a
        row_b, col_b = pos_b

        if row_a == row_b:  # Same row
            plaintext += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:  # Same column
            plaintext += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:  # Rectangle
            plaintext += matrix[row_a][col_b] + matrix[row_b][col_a]

        i += 2

    # Clean up the plaintext (remove padding X's)
    cleaned_text = ""
    i = 0
    while i < len(plaintext):
        if i == len(plaintext) - 1:
            # Last character
            if plaintext[i] != 'X':
                cleaned_text += plaintext[i]
        elif plaintext[i] == 'X' and i % 2 == 1:
            # X in second position of a pair
            # Only keep it if it doesn't look like padding
            if i < len(plaintext) - 2 and plaintext[i - 1] == plaintext[i + 1]:
                pass  # Skip the X that was used to separate identical letters
            else:
                cleaned_text += plaintext[i]
        else:
            cleaned_text += plaintext[i]
        i += 1

    return cleaned_text


# Hill cipher functions
def mod_inverse_matrix(matrix, mod):
    try:
        det = int(round(np.linalg.det(matrix)))
        det = det % mod

        # Check if the determinant is invertible in the given modulo
        gcd_val = np.gcd(det, mod)
        if gcd_val != 1:
            return None

        # Calculate multiplicative inverse of determinant
        det_inv = pow(det, -1, mod)

        # Calculate adjugate matrix
        if matrix.shape == (2, 2):
            # For 2x2 matrix, adjugate is simple
            adjugate = np.array([
                [matrix[1, 1], -matrix[0, 1]],
                [-matrix[1, 0], matrix[0, 0]]
            ]) % mod
        else:
            # For larger matrices, use the cofactor method
            adjugate = np.zeros_like(matrix)
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    # Calculate cofactor
                    minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                    cofactor = int(round(np.linalg.det(minor)))
                    cofactor = cofactor * (-1) ** (i + j)
                    adjugate[j, i] = cofactor  # Note the transpose here

            adjugate = adjugate % mod

        # Calculate inverse
        inverse = (det_inv * adjugate) % mod
        return inverse

    except Exception as e:
        print(f"Error in matrix inversion: {e}")
        return None


def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text.upper() if char.isalpha()]


def numbers_to_text(numbers):
    return "".join(chr(num % 26 + ord('A')) for num in numbers)


def hill_encrypt(text, key_matrix):
    text_numbers = text_to_numbers(text)
    key_size = key_matrix.shape[0]

    # Pad the text if needed
    while len(text_numbers) % key_size != 0:
        text_numbers.append(ord('X') - ord('A'))

    # Process the text in blocks of size key_size
    result = []
    for i in range(0, len(text_numbers), key_size):
        block = text_numbers[i:i + key_size]
        # Multiply the key matrix by the block vector
        encrypted_block = np.dot(key_matrix, block) % 26
        result.extend(encrypted_block)

    return numbers_to_text(result)


def hill_decrypt(ciphertext, key_matrix):
    key_inverse = mod_inverse_matrix(key_matrix, 26)
    if key_inverse is None:
        return "Error: Matrix is not invertible modulo 26"

    cipher_numbers = text_to_numbers(ciphertext)
    key_size = key_matrix.shape[0]

    # Ensure the ciphertext length is a multiple of the key size
    while len(cipher_numbers) % key_size != 0:
        cipher_numbers.append(0)

    # Process the ciphertext in blocks of size key_size
    result = []
    for i in range(0, len(cipher_numbers), key_size):
        block = cipher_numbers[i:i + key_size]
        # Multiply the inverse key matrix by the block vector
        decrypted_block = np.dot(key_inverse, block) % 26
        result.extend(decrypted_block)

    return numbers_to_text(result)


def parse_key_matrix(key_str, size):
    try:
        # Split the input by commas and convert to integers
        elements = [int(x.strip()) for x in key_str.split(',')]

        # Check if we have enough elements
        if len(elements) != size * size:
            return None

        # Create the matrix
        matrix = np.array(elements).reshape(size, size)
        return matrix
    except ValueError:
        return None


def parse_permutation(perm_str):
    try:
        # Split the input by commas and convert to integers
        elements = [int(x.strip()) for x in perm_str.split(',')]

        # Check if permutation is valid (uses integers from 1 to n)
        n = len(elements)
        if set(elements) != set(range(1, n + 1)):
            return None

        return elements
    except ValueError:
        return None


# Create the GUI application
class CryptographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Application")
        self.root.geometry("800x600")

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs for each cipher
        self.permutation_tab = ttk.Frame(self.notebook)
        self.playfair_tab = ttk.Frame(self.notebook)
        self.hill_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.permutation_tab, text="Permutation Cipher")
        self.notebook.add(self.playfair_tab, text="Playfair Cipher")
        self.notebook.add(self.hill_tab, text="Hill Cipher")

        # Set up the UI for each tab
        self.setup_permutation_tab()
        self.setup_playfair_tab()
        self.setup_hill_tab()

    def setup_permutation_tab(self):
        # Text input
        ttk.Label(self.permutation_tab, text="Enter text:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.permutation_text = ttk.Entry(self.permutation_tab, width=50)
        self.permutation_text.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

        # Permutation input
        ttk.Label(self.permutation_tab, text="Enter permutation (comma-separated):").grid(row=1, column=0, sticky=tk.W,
                                                                                          padx=10, pady=5)
        self.permutation_key = ttk.Entry(self.permutation_tab, width=50)
        self.permutation_key.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        self.permutation_key.insert(0, "2,1,3")  # Default value

        # Buttons
        ttk.Button(self.permutation_tab, text="Encrypt", command=self.permutation_encrypt).grid(row=2, column=0,
                                                                                                padx=10, pady=10)
        ttk.Button(self.permutation_tab, text="Decrypt", command=self.permutation_decrypt).grid(row=2, column=1,
                                                                                                padx=10, pady=10)
        ttk.Button(self.permutation_tab, text="Clear", command=self.permutation_clear).grid(row=2, column=2, padx=10,
                                                                                            pady=10)

        # Result display
        ttk.Label(self.permutation_tab, text="Result:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.permutation_result = scrolledtext.ScrolledText(self.permutation_tab, width=60, height=10)
        self.permutation_result.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    def setup_playfair_tab(self):
        # Text input
        ttk.Label(self.playfair_tab, text="Enter text:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.playfair_text = ttk.Entry(self.playfair_tab, width=50)
        self.playfair_text.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

        # Keyword input
        ttk.Label(self.playfair_tab, text="Enter keyword:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.playfair_key = ttk.Entry(self.playfair_tab, width=50)
        self.playfair_key.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        self.playfair_key.insert(0, "CRIPTOGRAFIE")  # Default value

        # Buttons
        ttk.Button(self.playfair_tab, text="Encrypt", command=self.playfair_encrypt).grid(row=2, column=0, padx=10,
                                                                                          pady=10)
        ttk.Button(self.playfair_tab, text="Decrypt", command=self.playfair_decrypt).grid(row=2, column=1, padx=10,
                                                                                          pady=10)
        ttk.Button(self.playfair_tab, text="Clear", command=self.playfair_clear).grid(row=2, column=2, padx=10, pady=10)

        # Result display
        ttk.Label(self.playfair_tab, text="Result:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.playfair_result = scrolledtext.ScrolledText(self.playfair_tab, width=60, height=10)
        self.playfair_result.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        # Matrix display
        ttk.Label(self.playfair_tab, text="Playfair Matrix:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        self.playfair_matrix = scrolledtext.ScrolledText(self.playfair_tab, width=60, height=5)
        self.playfair_matrix.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

        # Show matrix button
        ttk.Button(self.playfair_tab, text="Show Matrix", command=self.show_playfair_matrix).grid(row=7, column=0,
                                                                                                  padx=10, pady=10)

    def setup_hill_tab(self):
        # Text input
        ttk.Label(self.hill_tab, text="Enter text:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.hill_text = ttk.Entry(self.hill_tab, width=50)
        self.hill_text.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

        # Matrix size selection
        ttk.Label(self.hill_tab, text="Matrix size:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.hill_matrix_size = ttk.Combobox(self.hill_tab, values=["2x2", "3x3"], state="readonly")
        self.hill_matrix_size.grid(row=1, column=1, padx=10, pady=5)
        self.hill_matrix_size.current(0)  # Default to 2x2

        # Matrix input
        ttk.Label(self.hill_tab, text="Enter matrix (comma-separated):").grid(row=2, column=0, sticky=tk.W, padx=10,
                                                                              pady=5)
        self.hill_key = ttk.Entry(self.hill_tab, width=50)
        self.hill_key.grid(row=2, column=1, columnspan=3, padx=10, pady=5)
        self.hill_key.insert(0, "19,4,18,19")  # Default value for 2x2 matrix

        # Buttons
        ttk.Button(self.hill_tab, text="Encrypt", command=self.hill_encrypt).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(self.hill_tab, text="Decrypt", command=self.hill_decrypt).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(self.hill_tab, text="Clear", command=self.hill_clear).grid(row=3, column=2, padx=10, pady=10)
        ttk.Button(self.hill_tab, text="Calculate Inverse", command=self.calculate_inverse).grid(row=3, column=3,
                                                                                                 padx=10, pady=10)

        # Result display
        ttk.Label(self.hill_tab, text="Result:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.hill_result = scrolledtext.ScrolledText(self.hill_tab, width=60, height=10)
        self.hill_result.grid(row=5, column=0, columnspan=4, padx=10, pady=5)

    # Permutation Cipher methods
    def permutation_encrypt(self):
        text = self.permutation_text.get().upper()
        perm_str = self.permutation_key.get()
        perm = parse_permutation(perm_str)

        if not text:
            messagebox.showerror("Error", "Please enter text to encrypt")
            return

        if not perm:
            messagebox.showerror("Error", "Invalid permutation format")
            return

        try:
            encrypted = encrypt(text, perm)
            self.permutation_result.delete(1.0, tk.END)
            self.permutation_result.insert(tk.END, f"Original text: {text}\n")
            self.permutation_result.insert(tk.END, f"Encrypted text: {encrypted}\n")
            self.permutation_result.insert(tk.END, f"Permutation used: {perm}\n")
            self.permutation_result.insert(tk.END, f"Inverse permutation: {get_inverse_permutation(perm)}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def permutation_decrypt(self):
        text = self.permutation_text.get().upper()
        perm_str = self.permutation_key.get()
        perm = parse_permutation(perm_str)

        if not text:
            messagebox.showerror("Error", "Please enter text to decrypt")
            return

        if not perm:
            messagebox.showerror("Error", "Invalid permutation format")
            return

        try:
            decrypted = decrypt(text, perm)
            self.permutation_result.delete(1.0, tk.END)
            self.permutation_result.insert(tk.END, f"Encrypted text: {text}\n")
            self.permutation_result.insert(tk.END, f"Decrypted text: {decrypted}\n")
            self.permutation_result.insert(tk.END, f"Permutation used: {perm}\n")
            self.permutation_result.insert(tk.END, f"Inverse permutation: {get_inverse_permutation(perm)}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

    def permutation_clear(self):
        self.permutation_text.delete(0, tk.END)
        self.permutation_result.delete(1.0, tk.END)

    # Playfair Cipher methods
    def playfair_encrypt(self):
        text = self.playfair_text.get().upper()
        keyword = self.playfair_key.get().upper()

        if not text:
            messagebox.showerror("Error", "Please enter text to encrypt")
            return

        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword")
            return

        try:
            encrypted = encrypt_playfair(text, keyword)
            self.playfair_result.delete(1.0, tk.END)
            self.playfair_result.insert(tk.END, f"Original text: {text}\n")
            self.playfair_result.insert(tk.END, f"Encrypted text: {encrypted}\n")
            self.playfair_result.insert(tk.END, f"Keyword used: {keyword}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def playfair_decrypt(self):
        text = self.playfair_text.get().upper()
        keyword = self.playfair_key.get().upper()

        if not text:
            messagebox.showerror("Error", "Please enter text to decrypt")
            return

        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword")
            return

        try:
            decrypted = decrypt_playfair(text, keyword)
            self.playfair_result.delete(1.0, tk.END)
            self.playfair_result.insert(tk.END, f"Encrypted text: {text}\n")
            self.playfair_result.insert(tk.END, f"Decrypted text: {decrypted}\n")
            self.playfair_result.insert(tk.END, f"Keyword used: {keyword}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

    def playfair_clear(self):
        self.playfair_text.delete(0, tk.END)
        self.playfair_result.delete(1.0, tk.END)
        self.playfair_matrix.delete(1.0, tk.END)

    def show_playfair_matrix(self):
        keyword = self.playfair_key.get().upper()

        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword")
            return

        try:
            matrix = generate_playfair_matrix(keyword)
            self.playfair_matrix.delete(1.0, tk.END)

            for row in matrix:
                self.playfair_matrix.insert(tk.END, " ".join(row) + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate matrix: {str(e)}")

    # Hill Cipher methods
    def hill_encrypt(self):
        text = self.hill_text.get().upper()
        key_str = self.hill_key.get()
        size = 2 if self.hill_matrix_size.get() == "2x2" else 3

        if not text:
            messagebox.showerror("Error", "Please enter text to encrypt")
            return

        key_matrix = parse_key_matrix(key_str, size)
        if key_matrix is None:
            messagebox.showerror("Error",
                                 f"Invalid matrix format. Please enter {size * size} comma-separated integers.")
            return

        try:
            encrypted = hill_encrypt(text, key_matrix)
            self.hill_result.delete(1.0, tk.END)
            self.hill_result.insert(tk.END, f"Original text: {text}\n")
            self.hill_result.insert(tk.END, f"Encrypted text: {encrypted}\n")
            self.hill_result.insert(tk.END, f"Matrix used:\n{key_matrix}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def hill_decrypt(self):
        text = self.hill_text.get().upper()
        key_str = self.hill_key.get()
        size = 2 if self.hill_matrix_size.get() == "2x2" else 3

        if not text:
            messagebox.showerror("Error", "Please enter text to decrypt")
            return

        key_matrix = parse_key_matrix(key_str, size)
        if key_matrix is None:
            messagebox.showerror("Error",
                                 f"Invalid matrix format. Please enter {size * size} comma-separated integers.")
            return

        try:
            decrypted = hill_decrypt(text, key_matrix)
            self.hill_result.delete(1.0, tk.END)
            self.hill_result.insert(tk.END, f"Encrypted text: {text}\n")
            self.hill_result.insert(tk.END, f"Decrypted text: {decrypted}\n")
            self.hill_result.insert(tk.END, f"Matrix used:\n{key_matrix}")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")

    def hill_clear(self):
        self.hill_text.delete(0, tk.END)
        self.hill_result.delete(1.0, tk.END)

    def calculate_inverse(self):
        key_str = self.hill_key.get()
        size = 2 if self.hill_matrix_size.get() == "2x2" else 3

        key_matrix = parse_key_matrix(key_str, size)
        if key_matrix is None:
            messagebox.showerror("Error",
                                 f"Invalid matrix format. Please enter {size * size} comma-separated integers.")
            return

        try:
            inverse = mod_inverse_matrix(key_matrix, 26)
            if inverse is None:
                self.hill_result.delete(1.0, tk.END)
                self.hill_result.insert(tk.END, "Error: Matrix is not invertible modulo 26")
            else:
                self.hill_result.delete(1.0, tk.END)
                self.hill_result.insert(tk.END, f"Original matrix:\n{key_matrix}\n\n")
                self.hill_result.insert(tk.END, f"Inverse matrix (mod 26):\n{inverse}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate inverse: {str(e)}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptographyApp(root)
    root.mainloop()