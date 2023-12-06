import os
import string
import random
import json
from cryptography.fernet import Fernet

def load_or_create_key():
    try:
        with open('key.key', 'rb') as key_file:
            key = key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)
    return key

key = load_or_create_key()
cipher_suite = Fernet(key)

def load_or_create_passwords():
    try:
        with open('passwords.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_passwords(password_dict):
    with open('passwords.json', 'w') as file:
        json.dump(password_dict, file)

def get_password(username):
    passwords_dict = load_or_create_passwords()
    if username not in passwords_dict:
        return "Error: Username not found."
    encrypted_password = passwords_dict[username].encode()
    with open('key.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    try:
        password = cipher_suite.decrypt(encrypted_password)
        return password.decode()
    except:
        return "Error: Password decryption failed."

def password_encrypt(password):
    with open('key.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(password.encode())
    return cipher_text

def password_decrypt(encrypted_pwd):
    with open('key.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_pwd)
    return decrypted_text.decode()

def generate_complex_string(length, use_lowercase=True, use_uppercase=True, use_numbers=True, use_special=True):
    characters = ''
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def password_strength_checker(password):
    criteria = {
        'length': len(password) >= 8,
        'lowercase': any(c in string.ascii_lowercase for c in password),
        'uppercase': any(c in string.ascii_uppercase for c in password),
        'digits': any(c in string.digits for c in password),
        'special': any(c in string.punctuation for c in password),
        'unique': len(set(password)) >= len(password) / 2,
    }
    strength = sum(criteria.values())
    if strength <= 2:
        return 'Weak'
    elif strength <= 4:
        return 'Moderate'
    else:
        return 'Strong'

def create_password():
    passwords_dict = load_or_create_passwords()
    username = input("Enter a username to save this password: ")
    length = int(input("Enter the length of the password: "))
    use_lowercase = input("Include lowercase letters? (yes/no): ").lower() == 'yes'
    use_uppercase = input("Include uppercase letters? (yes/no): ").lower() == 'yes'
    use_numbers = input("Include numbers? (yes/no): ").lower() == 'yes'
    use_special = input("Include special characters? (yes/no): ").lower() == 'yes'
    password = generate_complex_string(length, use_lowercase, use_uppercase, use_numbers, use_special)
    print("Generated password strength: ", password_strength_checker(password))
    encrypted_password = password_encrypt(password)
    passwords_dict[username] = encrypted_password.decode()
    save_passwords(passwords_dict)
    print(f"Password saved securely for user {username}")

def main_menu():
    while True:
        print("\n1. Create a new password")
        print("2. Retrieve an existing password")
        print("3. Exit")
        choice = input("Please enter your choice: ")

        if choice == '1':
            create_password()
        elif choice == '2':
            username = input("Enter a username to get the password: ")
            print(get_password(username))
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Call the main menu at the start
main_menu()