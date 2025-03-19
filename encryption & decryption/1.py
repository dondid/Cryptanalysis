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
    blocks = [encrypted_text[i:i + n] for i in range(0, len(encrypted_text), n)]
    decrypted_text = ""
    for block in blocks:
        decrypted_block = "".join(block[inverse_perm[i] - 1] for i in range(n))
        decrypted_text += decrypted_block
    return decrypted_text.replace("W", " ").rstrip("X")  # Restore spaces and remove padding

# Given permutation sigma = (1 2 3) -> (2 1 3)
permutation = [2, 1, 3]

text = "FLOAREALBASTRA"
encrypted_text = encrypt(text, permutation)
decrypted_text = decrypt(encrypted_text, permutation)

print(f"Original text: {text}")
print(f"Encrypted text: {encrypted_text}")
print(f"Decrypted text: {decrypted_text}")
print(f"Permutation used: {permutation}")
print(f"Inverse permutation: {get_inverse_permutation(permutation)}")

print()

def generate_playfair_matrix(keyword):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    keyword = "".join(dict.fromkeys(keyword.upper().replace("J", "I")))
    matrix_string = keyword + "".join([c for c in alphabet if c not in keyword])
    return [list(matrix_string[i:i + 5]) for i in range(0, 25, 5)]


def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col


def decrypt_playfair(ciphertext, keyword):
    matrix = generate_playfair_matrix(keyword)
    plaintext = ""
    ciphertext = ciphertext.replace(" ", "")

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b] + matrix[row_b][col_a]

    return plaintext.replace("X", "")


# Messages to decrypt
messages = [
    ("UFRIL ERGPC RQAW", "CRIPTOGRAFIE"),
    ("KDPEK DOSTF RDRXB NBBBB", "PASSWORD"),
    ("GBQY YAAO RNBM", "TEST")
]

for message, keyword in messages:
    decrypted_text = decrypt_playfair(message, keyword)
    print(f"Ciphertext: {message}")
    print(f"Decrypted text: {decrypted_text}")
    print(f"Keyword used: {keyword}\n")

print()

import numpy as np

def mod_inverse_matrix(matrix, mod):
    det = int(round(np.linalg.det(matrix)))
    if np.gcd(det, mod) != 1:
        print(("Matrix determinant is not invertible modulo 26"))
    else:
        det_inv = pow(det, -1, mod)
        adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % mod
        return (det_inv * adjugate) % mod

def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text.upper() if char.isalpha()]

def numbers_to_text(numbers):
    return "".join(chr(num + ord('A')) for num in numbers)

def hill_encrypt(text, key_matrix):
    text_numbers = text_to_numbers(text)
    while len(text_numbers) % key_matrix.shape[0] != 0:
        text_numbers.append(ord('X') - ord('A'))
    text_matrix = np.array(text_numbers).reshape(-1, key_matrix.shape[0]).T
    encrypted_matrix = np.dot(key_matrix, text_matrix) % 26
    return numbers_to_text(encrypted_matrix.T.flatten())

def hill_decrypt(ciphertext, key_matrix):
    key_inverse = mod_inverse_matrix(key_matrix, 26)
    cipher_numbers = text_to_numbers(ciphertext)
    cipher_matrix = np.array(cipher_numbers).reshape(-1, key_matrix.shape[0]).T
    decrypted_matrix = np.dot(key_inverse, cipher_matrix) % 26
    return numbers_to_text(decrypted_matrix.T.flatten())

# Encryption and Decryption
key_matrix = np.array([[19, 4], [18, 19]])  # (T E / S T)

plaintext = "CRYPTOLOGY"
ciphertext = hill_encrypt(plaintext, key_matrix)
decrypted_text = hill_decrypt("CVWPBKFWCS", key_matrix)

print(f"Original text: {plaintext}")
print(f"Encrypted text: {ciphertext}")
print(f"Decrypted text: {decrypted_text}")

def permutation_encrypt(text, perm):
    text = text.ljust(len(perm), 'X')
    encrypted_text = "".join(text[perm[i] - 1] for i in range(len(perm)))
    return encrypted_text

# Given permutation sigma = (1 2 3 4 5 6) -> (2 4 6 1 3 5)
permutation = [2, 4, 6, 1, 3, 5]

# Hill cipher key matrix for permutation encryption
hill_key_matrix = np.zeros((6, 6), dtype=int)
for i, p in enumerate(permutation):
    hill_key_matrix[p - 1, i] = 1

plaintext = "SECRET"
ciphertext_permutation = permutation_encrypt(plaintext, permutation)
ciphertext_hill = hill_encrypt(plaintext, hill_key_matrix)

print(f"Original text: {plaintext}")
print(f"Encrypted text using permutation cipher: {ciphertext_permutation}")
print(f"Encrypted text using Hill cipher: {ciphertext_hill}")
print(f"Hill cipher encryption matrix:\n{hill_key_matrix}")

def find_hill_key(plaintext, ciphertext):
    M = np.array(text_to_numbers(plaintext)).reshape(2, 2)
    C = np.array(text_to_numbers(ciphertext)).reshape(2, 2)
    M_inv = mod_inverse_matrix(M, 26)
    A = None
    if M_inv is not None:
        A = np.dot(M_inv, C) % 26
    return A

# Application A: Finding Hill Cipher Key
plaintext_A = "FRAC"
ciphertext_A = "XWEG"
A_matrix = find_hill_key(plaintext_A, ciphertext_A)

# Application B: Chosen Plaintext Attack
plaintext_B = "BRAD"
ciphertext_B = "LKGP"
M_matrix = np.array(text_to_numbers(plaintext_B)).reshape(2, 2)
C_matrix = np.array(text_to_numbers(ciphertext_B)).reshape(2, 2)
M_inv = mod_inverse_matrix(M_matrix, 26)
A_recovered = np.dot(M_inv, C_matrix) % 26

print(f"Recovered Hill Cipher Key Matrix A from (FRAC, XWEG):\n{A_matrix}")
print(f"Recovered Hill Cipher Key Matrix A from chosen plaintext attack (BRAD, LKGP):\n{A_recovered}")