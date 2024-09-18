from django.db import models
from app.utils import *

# Create your models here.
class Profil(models.Model):
    libelle = models.CharField(max_length=MAX_CHAR)

class Utilisateur(models.Model):
    code = models.CharField(max_length=MAX_CHAR)
    nom = models.CharField(max_length=MAX_CHAR)
    prenom = models.CharField(max_length=MAX_CHAR)
    date_naissance = models.DateField()
    specialite = models.CharField(max_length=MAX_CHAR, null=True)
    email = models.EmailField(max_length=MAX_CHAR)
    password = models.CharField(max_length=MAX_CHAR)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Utilisateur.objects.values_list('code', flat=True)
            code = generate_string(LENGTH_CODE)
            while code in codes:
                code = generate_string(LENGTH_CODE)
            self.code = code
        super().save(*args, **kwargs)
  

class Patient(models.Model):
    nom = models.CharField(max_length=MAX_CHAR)
    prenom = models.CharField(max_length=MAX_CHAR)
    docteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

  
class Donnee(models.Model):
    code = models.CharField(max_length=MAX_CHAR)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(null=True)
    poids = models.IntegerField(default=0) # Arrondi
    taille = models.IntegerField(default=0) # En cm
    etat_de_grossesse = models.IntegerField(null=True) # 0 ou  1
    niveauInsuline = models.FloatField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Donnee.objects.values_list('code', flat=True)
            code = generate_string(LENGTH_CODE)
            while code in codes:
                code = generate_string(LENGTH_CODE)
            self.code = code
        super().save(*args, **kwargs)

class Resultat(models.Model):
    code = models.CharField(max_length=MAX_CHAR)
    donnee = models.ForeignKey(Donnee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pourcentage = models.FloatField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Resultat.objects.values_list('code', flat=True)
            code = generate_string(LENGTH_CODE)
            while code in codes:
                code = generate_string(LENGTH_CODE)
            self.code = code
        super().save(*args, **kwargs)

class MessageVisiteur(models.Model):
    nom = models.CharField(max_length=MAX_CHAR)
    email = models.EmailField(max_length=MAX_CHAR)
    telephone = models.CharField(max_length=MAX_CHAR)
    sujet = models.CharField(max_length=MAX_CHAR)
    message = models.CharField(max_length=MAX_CHAR)
    date = models.DateTimeField(auto_now_add=True)