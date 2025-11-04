def generate_key(plaintext, keyword):
    """
    Generates a key for encryption.
    >>> generate_key("ATTACKATDAWN", "LEMON")
    'LEMONLEMONLE'
    """
    keyword = list(keyword)
    if len(plaintext) == len(keyword):
        return keyword
    else:
        for i in range(len(plaintext) - len(keyword)):
            keyword.append(keyword[i % len(keyword)])
    return "".join(keyword)


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword = generate_key(plaintext, keyword)
    for i in range(len(plaintext)):
        char = plaintext[i]
        if char.isupper():
            encrypted_char = chr((ord(char) + ord(keyword[i]) - 2 * ord('A')) % 26 + ord('A'))
        elif char.islower():
            encrypted_char = chr((ord(char) + ord(keyword[i]) - 2 * ord('a')) % 26 + ord('a'))
        else:
            encrypted_char = char
        ciphertext += encrypted_char

    return ciphertext
print(encrypt_vigenere("itmo", "itmo"))


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword = generate_key(ciphertext, keyword)
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isupper():
            decrypted_char = chr((ord(char) - ord(keyword[i]) + 26) % 26 + ord('A'))
        elif char.islower():
            decrypted_char = chr((ord(char) - ord(keyword[i]) + 26) % 26 + ord('a'))
        else:
            decrypted_char = char
        plaintext += decrypted_char
    return plaintext
print(decrypt_vigenere("PYTHON", "ATTACKATDAWN"))