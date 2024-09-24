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
    sexe = models.BooleanField(default=True)
    password = models.CharField(max_length=MAX_CHAR)
    image = models.ImageField(upload_to='images/', null=True)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Utilisateur.objects.values_list('code', flat=True)
            code = generate_string(LENGTH_CODE)
            while code in codes:
                code = generate_string(LENGTH_CODE)
            self.code = code
        super().save(*args, **kwargs)
    
    def age(self):
        return calculer_age(self.date_naissance)
    
    def nom_prenom(self):
        return f"{self.nom} {self.prenom}"
    
    def date_naissance_rep(self):
        return date_to_text(self.date_naissance)
    
    def has_data(self):
        return Donnee.objects.filter(utilisateur=self).exists()
    
    def last_data(self):
        if self.has_data():
            return Donnee.objects.filter(utilisateur=self).last()
        return None
    
    def has_save_data_today(self):
        if self.has_data():
            return Donnee.objects.filter(utilisateur=self, date=todayDate()).exists()
        return False
    
    def data_saved_today(self):
        if self.has_data():
            return Donnee.objects.filter(utilisateur=self, date=todayDate()).first()
        return None
    
    def donnees(self):
        if self.has_data():
            return Donnee.objects.filter(utilisateur=self)
        return None
    
    def nb_donnees(self):
        if self.has_data():
            return Donnee.objects.filter(utilisateur=self).count()
        return 0
    
    def resultats(self):
        if self.has_data():
            return Resultat.objects.filter(donnee__utilisateur=self)
        return None
    
    def nb_resultats(self):
        if self.has_data():
            return Resultat.objects.filter(donnee__utilisateur=self).count()
        return 0
    
    def poids_actuel(self):
        if self.has_data():
            return Donnee.objects.filter(utilisateur=self).last().poids
        return 0
    
    def glycemie_actuelle(self):
        if self.has_data():
            return Donnee.objects.filter(utilisateur=self).last().niveauInsuline
        return 0

class Patient(models.Model):
    code = models.CharField(max_length=MAX_CHAR)
    nom = models.CharField(max_length=MAX_CHAR)
    prenom = models.CharField(max_length=MAX_CHAR)
    date_naissance = models.DateField()
    sexe = models.BooleanField(default=True)
    telephone = models.CharField(max_length=MAX_CHAR)
    docteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Patient.objects.values_list('code', flat=True)
            code = generate_string(LENGTH_CODE)
            while code in codes:
                code = generate_string(LENGTH_CODE)
            self.code = code
        super().save(*args, **kwargs)
    
    def age(self):
        return calculer_age(self.date_naissance)
    
    def nom_prenom(self):
        return f"{self.nom} {self.prenom}"
    
    def date_naissance_rep(self):
        return date_to_text(self.date_naissance)
    
    def has_data(self):
        return Donnee.objects.filter(patient=self).exists()
    
    def last_data(self):
        if self.has_data():
            return Donnee.objects.filter(patient=self).last()
        return None
    
    def has_save_data_today(self):
        if self.has_data():
            return Donnee.objects.filter(patient=self, date=todayDate()).exists()
        return False
    
    def data_saved_today(self):
        if self.has_data():
            return Donnee.objects.filter(patient=self, date=todayDate()).first()
        return None
    
    def donnees(self):
        if self.has_data():
            return Donnee.objects.filter(patient=self)
        return None
    
    def nb_donnees(self):
        if self.has_data():
            return Donnee.objects.filter(patient=self).count()
        return 0
    
    def resultats(self):
        if self.has_data():
            return Resultat.objects.filter(donnee__patient=self)
        return None
    
    def nb_resultats(self):
        if self.has_data():
            return Resultat.objects.filter(donnee__patient=self).count()
        return 0
    
    def poids_actuel(self):
        if self.has_data():
            return Donnee.objects.filter(patient=self).last().poids
        return 0
    
    def glycemie_actuelle(self):
        if self.has_data():
            return Donnee.objects.filter(patient=self).last().niveauInsuline
        return 0

  
class Donnee(models.Model):
    code = models.CharField(max_length=MAX_CHAR)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(null=True)
    poids = models.IntegerField(default=0) # Arrondi
    taille = models.IntegerField(default=0) # En cm
    etat_de_grossesse = models.IntegerField(default=0) # 0 ou  1
    niveauInsuline = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Donnee.objects.values_list('code', flat=True)
            code = generate_string(LENGTH_CODE)
            while code in codes:
                code = generate_string(LENGTH_CODE)
            self.code = code
        super().save(*args, **kwargs)
    
    def date_rep(self):
        return date_to_text(self.date)
    
    def has_answer(self):
        return Resultat.objects.filter(donnee=self).exists()
    
    def answer(self):
        if self.has_answer():
            return Resultat.objects.filter(donnee=self).last()
        return None
    
    def has_predict_today(self):
        if self.has_answer():
            return Resultat.objects.filter(donnee=self, date=todayDate()).exists()
        return False
    
    def evaluate(self):
        if self.has_answer():
            res = self.answer()
            res.pourcentage = predict_diabetes(self.age, self.poids, self.taille, self.niveauInsuline, self.etat_de_grossesse)
            res.save()
        else:
            res = Resultat(donnee=self)
            res.pourcentage = predict_diabetes(self.age, self.poids, self.taille, self.niveauInsuline, self.etat_de_grossesse)
            res.save()

class Resultat(models.Model):
    code = models.CharField(max_length=MAX_CHAR)
    donnee = models.ForeignKey(Donnee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    pourcentage = models.FloatField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.code:
            codes = Resultat.objects.values_list('code', flat=True)
            code = generate_string(LENGTH_CODE)
            while code in codes:
                code = generate_string(LENGTH_CODE)
            self.code = code
        super().save(*args, **kwargs)
    
    def risque_text(self):
        if self.risque() >= 66:
            return "Fort"
        elif self.risque() >= 33:
            return "Moyen"
        else:
            return "Faible"
    
    def risque(self):
        return float(f'{self.pourcentage*100:.2f}')
class MessageVisiteur(models.Model):
    nom = models.CharField(max_length=MAX_CHAR)
    email = models.EmailField(max_length=MAX_CHAR)
    telephone = models.CharField(max_length=MAX_CHAR)
    sujet = models.CharField(max_length=MAX_CHAR)
    message = models.CharField(max_length=MAX_CHAR)
    date = models.DateTimeField(auto_now_add=True)