from app.models import *

################################################
p = Profil(libelle="Administrateur")
p.save()

p = Profil(libelle="Utilisateur")
p.save()

p = Profil(libelle="Docteur")
p.save()

################################################
u = Utilisateur(nom="LAWSON", prenom="Frejus", date_naissance=datetime.date(2004, 4, 3), email="lawsonfrejus09@gmail.com", password=chiffrement("frejus.lawson"), profil=Profil.objects.get(id=1))
u.save()

################################################

