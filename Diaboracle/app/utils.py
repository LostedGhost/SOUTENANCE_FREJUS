import random, string
import datetime
from app.config import *
import numpy as np
import calendar

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

def todayDateStr():
    today = datetime.datetime.today()
    return today.strftime('%Y-%m-%d')

def todayDate():
    return datetime.date.today()

def calculer_age(date_naissance):
    # Convertir la date de naissance en un objet datetime
    if isinstance(date_naissance, str):
        date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d')
    
    # Obtenir la date actuelle
    today = datetime.datetime.today()
    
    # Calculer l'âge en années
    age = today.year - date_naissance.year
    
    # Ajuster l'âge si l'anniversaire de cette année n'est pas encore passé
    if today.month < date_naissance.month or (today.month == date_naissance.month and today.day < date_naissance.day):
        age -= 1
    
    return age

def get_last_7_days():
    last_7_days = []
    today = datetime.datetime.today()

    # Récupère les 7 derniers jours
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        formatted_day = day.strftime('%d/%m/%Y')
        last_7_days.append(formatted_day)
    last_7_days.reverse()
    return last_7_days

def get_last_7_days_dates():
    last_7_days = []
    today = datetime.datetime.today()
    # Récupère les 7 derniers jours
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        last_7_days.append(day)
    last_7_days.reverse()
    
    return last_7_days

def get_days_of_month(month, year):
    # Calcule le nombre de jours dans le mois
    num_days = calendar.monthrange(year, month)[1]
    # Crée une liste pour stocker les dates du mois
    month_days = []
    # Ajoute les dates du mois à la liste
    for day in range(1, num_days + 1):
        date = datetime.datetime(year, month, day)
        month_days.append(date)
    return month_days

def get_days_of_month_str(month, year):
    # Calcule le nombre de jours dans le mois
    num_days = calendar.monthrange(year, month)[1]
    # Crée une liste pour stocker les dates du mois
    month_days = []
    # Ajoute les dates du mois à la liste
    for day in range(1, num_days + 1):
        date = datetime.datetime(year, month, day)
        month_days.append(date.strftime('%d/%m/%Y'))
    return month_days

def get_period_days(start_date, end_date):
    # Calcule la différence entre les deux dates
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    # Calcule la différence entre les deux dates
    delta = end_date - start_date
    # Crée une liste pour stocker les dates du mois
    period_days = []
    # Ajoute les dates du mois à la liste
    for i in range(delta.days + 1):
        date = start_date + datetime.timedelta(days=i)
        period_days.append(date)
    return period_days

def get_period_dates_str(start_date, end_date):
    # Calcule la différence entre les deux dates
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    delta = end_date - start_date
    # Crée une liste pour stocker les dates du mois
    period_days = []
    # Ajoute les dates du mois à la liste
    for i in range(delta.days + 1):
        date = start_date + datetime.timedelta(days=i)
        period_days.append(date.strftime('%d/%m/%Y'))
    return period_days

def is_date_in_intervals(date_to_check, date_list):
    # Convertit la date à vérifier en objet date si ce n'est pas déjà fait
    if isinstance(date_to_check, str):
        date_to_check = datetime.datetime.strptime(date_to_check, '%d/%m/%Y').date()
    elif isinstance(date_to_check, datetime.datetime):
        date_to_check = date_to_check.date()

    # Convertit toutes les dates de la liste en objets date
    date_list = [
        datetime.datetime.strptime(date, '%d/%m/%Y').date() if isinstance(date, str) else date
        for date in date_list
    ]

    # Trie la liste des dates dans l'ordre chronologique
    date_list.sort()

    # Parcourt la liste de dates pour vérifier si la date à vérifier est entre deux dates consécutives
    for i in range(len(date_list) - 1):
        if date_list[i] <= date_to_check <= date_list[i + 1]:
            return True, date_list[i].strftime('%d/%m/%Y')

    # Si la date ne se trouve dans aucun intervalle, retourne False et None
    return False, None

