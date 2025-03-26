![image](https://github.com/user-attachments/assets/0827ac6d-969c-4eb7-9928-292b3525b4b5)

# Cryptography App Test Data

This document contains test data and tips for verifying the functionality of various cryptographic algorithms implemented in the Cryptography App.

## 1. Caesar Cipher Test Data
- **Text to Encrypt/Decrypt**: `HELLO WORLD`
- **Shift Value (k)**: `3`
- **Expected Encrypted Result**: `KHOOR ZRUOG`
- **Expected Decrypted Result**: `HELLO WORLD`

---

## 2. Vigenère Cipher Test Data
- **Text to Encrypt/Decrypt**: `SECRETMESSAGE`
- **Key**: `KEY`
- **Expected Encrypted Result**: `EIKZRGWZIIGKI`
- **Expected Decrypted Result**: `SECRETMESSAGE`

---

## 3. Transposition Cipher Test Data
- **Text to Encrypt/Decrypt**: `CRYPTOGRAPHYISAWESOME`
- **Permutation Key**: `2, 1, 3, 4`
- **Expected Encrypted Result**: (Depends on the specific permutation algorithm used)
- **Expected Decrypted Result**: `CRYPTOGRAPHYISAWESOME`

---

## 4. Custom Cipher Example - ROT13 Cipher
### Encryption Function
```python
def custom_encrypt(text):
    result = ""
    for char in text.upper():
        if char.isalpha():
            # Shift by 13 positions
            shifted = ord(char) + 13
            if shifted > ord('Z'):
                shifted -= 26
            result += chr(shifted)
        else:
            result += char
    return result
```
### Decryption Function
```python
def custom_decrypt(text):
    result = ""
    for char in text.upper():
        if char.isalpha():
            # Reverse shift by 13 positions
            shifted = ord(char) - 13
            if shifted < ord('A'):
                shifted += 26
            result += chr(shifted)
        else:
            result += char
    return result

