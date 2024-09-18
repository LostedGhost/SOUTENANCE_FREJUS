import random, string
import datetime
from app.config import *
import numpy as np

def predict_diabetes(age, poids, taille, glycemie, etat_de_grossesse):
    # Coefficients obtenus du modèle
    beta_0 = -6.89147026
    beta_1 = 0.04083271
    beta_2 = 0.02047807
    beta_3 = -0.00261474
    beta_4 = 1.21596762
    beta_5 = -0.13748181
    
    # Calcul de la somme pondérée des paramètres
    linear_combination = (beta_0 + 
                          beta_1 * age + 
                          beta_2 * poids + 
                          beta_3 * taille + 
                          beta_4 * glycemie + 
                          beta_5 * etat_de_grossesse)
    
    # Calcul de la probabilité en utilisant la fonction sigmoïde
    probability = 1 / (1 + np.exp(-linear_combination))
    
    return probability


def date_to_text(date):
    return date.strftime('%Y-%m-%d')

def text_to_date(text):
    return datetime.datetime.strptime(text, '%Y-%m-%d')

def generate_string(length=12):
    """Generate a strong password."""
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits

    # Combine character sets
    all_characters = lowercase_letters + uppercase_letters + digits

    # Ensure at least one character from each set
    password = random.choice(lowercase_letters)
    password += random.choice(uppercase_letters)
    password += random.choice(digits)

    # Fill remaining length with random characters
    for _ in range(length - 3):
        password += random.choice(all_characters)

    # Shuffle the password to make it more random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

def chiffrement(message) -> str:
    decalage = KEY
    message_chiffre = ""
    for caractere in message:
        # Vérifier si le caractère est une lettre majuscule
        if caractere.isupper():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('A') + decalage) % 26 + ord('A')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est une lettre minuscule
        elif caractere.islower():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('a') + decalage) % 26 + ord('a')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est un chiffre
        elif caractere.isdigit():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('0') + decalage) % 10 + ord('0')
            message_chiffre += chr(nouveau_code)
        # Si le caractère est un caractère spécial, le laisser inchangé
        else:
            message_chiffre += caractere
    return message_chiffre

def dechiffrement(message) -> str:
    decalage = -KEY
    message_chiffre = ""
    for caractere in message:
        # Vérifier si le caractère est une lettre majuscule
        if caractere.isupper():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('A') + decalage) % 26 + ord('A')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est une lettre minuscule
        elif caractere.islower():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('a') + decalage) % 26 + ord('a')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est un chiffre
        elif caractere.isdigit():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('0') + decalage) % 10 + ord('0')
            message_chiffre += chr(nouveau_code)
        # Si le caractère est un caractère spécial, le laisser inchangé
        else:
            message_chiffre += caractere
    return message_chiffre

def calculer_age(date_naissance):
    # Convertir la date de naissance en un objet datetime
    if isinstance(date_naissance, str):
        date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d')
    
    # Obtenir la date actuelle
    today = datetime.today()
    
    # Calculer l'âge en années
    age = today.year - date_naissance.year
    
    # Ajuster l'âge si l'anniversaire de cette année n'est pas encore passé
    if today.month < date_naissance.month or (today.month == date_naissance.month and today.day < date_naissance.day):
        age -= 1
    
    return age
