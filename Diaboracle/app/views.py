from django.shortcuts import render, redirect
from django.http import JsonResponse
from app.models import *

# Create your views here.
def home(request):
    user_code = request.session.get("user", None)
    if user_code != None:
        return redirect("/dash")
    if request.POST:
        mv = MessageVisiteur(
            nom=request.POST["name"],
            email=request.POST["email"],
            telephone=request.POST["phone"],
            sujet=request.POST["subject"],
            message=request.POST["message"],
        )
        mv.save()
        return redirect("/")
    return render(request, "index.html")

def predict_diabete_api(request):
    data = {
        'status': 400,
        'message': 'Une erreur est survenue',
        'answer': None
    }
    age = request.GET.get('age', None)
    poids = request.GET.get('poids', None)
    taille = request.GET.get('taille', None)
    glycemie = request.GET.get('glycemie', None)
    etat_de_grossesse = int(request.GET.get('etat_de_grossesse', None))
    if age !='' and poids!='' and taille!='' and glycemie!='':
        age = int(age)
        poids = int(poids)
        taille = int(taille)
        glycemie = float(glycemie)
        data['status'] = 200
        data['message'] = ""
        answer = predict_diabetes(age, poids, taille, glycemie, etat_de_grossesse) * 100
        answer = float(f'{answer:.2f}')
        if answer > 60:
            data['message'] = "Vous avez un risque élevé de diabète."
        elif answer > 30:
            data['message'] = "Vous avez un risque modéré de diabète."
        else:
            data['message'] = "Vous avez un risque faible de diabète."
        data['answer'] = answer
        data['decimal_answer'] = answer / 100
    else:
        data['status'] = 400
        data['message'] = "Veuillez remplir tous les champs"
        data['answer'] = None
    return JsonResponse(data)

def prediction_passant(request):
    user_code = request.session.get("user", None)
    if user_code != None:
        return redirect("/dash")
    return render(request, "predict.html")

def login(request):
    user_code = request.session.get("user", None)
    if user_code != None:
        return redirect("/dash")
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        utilisateur = Utilisateur.objects.filter(email=email)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            if chiffrement(password) == utilisateur.password:
                return redirect("/dash")
            else:
                return redirect("/login")
        else:
            return redirect("/login")
    return render(request, "admin-temp/login.html")

def api_login(request):
    if request.GET:
        email = request.GET["email"]
        password = request.GET["password"]
        if email == "" or password == "":
            return JsonResponse({
                "status": 400,
                "message": "Veuillez remplir tous les champs"
            })
        utilisateur = Utilisateur.objects.filter(email=email)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            if chiffrement(password) == utilisateur.password:
                request.session["user"] = utilisateur.code
                return JsonResponse({
                    "status": 200,
                    "message": "Connexion réussie",
                    "data": {
                        "id": utilisateur.id,
                        "nom": utilisateur.nom,
                        "prenoms": utilisateur.prenom,
                        "email": utilisateur.email,
                        "specialite": utilisateur.specialite,
                        "date_naissance": utilisateur.date_naissance,
                    }
                })
            else:
                return JsonResponse({
                    "status": 400,
                    "message": "Mot de passe incorrect",
                    "data": None
                    })
        else:
                    return JsonResponse({
                        "status": 400,
                        "message": "Utilisateur non trouvé",
                        "data": None
                    })

def signin(request):
    user_code = request.session.get("user", None)
    if user_code != None:
        return redirect("/dash")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request, "admin-temp/signin.html",{
        "today": today
    })

def api_signin(request):
    if request.GET:
        nom = request.GET["nom"]
        prenoms = request.GET["prenoms"]
        date_naissance = request.GET["date_naissance"]
        email = request.GET["email"]
        password = request.GET["password"]
        repassword = request.GET["repassword"]
        specialite = request.GET["speciality"]
        if nom =="" or prenoms == "" or date_naissance == "" or email == "" or password == "" or repassword == "":
            return JsonResponse({
                "status": 400,
                "message": "Les champs ne sont pas optionnels."
            })
        if Utilisateur.objects.filter(email=email).exists():
            return JsonResponse({
                "status": 400,
                "message": "Cet email est déjà utilisé"
            })
        else:
            if password != repassword:
                return JsonResponse({
                    "status": 400,
                    "message": "Les mots de passe ne correspondent pas"
                })
            else:
                utilisateur = Utilisateur(
                    nom=nom,
                    prenom=prenoms,
                    date_naissance=date_naissance,
                    email=email,
                    password=chiffrement(password)
                )
                if specialite != "":
                    utilisateur.specialite = specialite
                    utilisateur.profil = Profil.objects.get(id=3)
                else:
                    utilisateur.profil = Profil.objects.get(id=2)
                utilisateur.save()
                donnee = Donnee(
                    utilisateur=utilisateur,
                    age=calculer_age(utilisateur.date_naissance),
                    poids= utilisateur.poids,
                    taille=utilisateur.taille,
                    prenom=prenoms,
                    specialite=specialite
                )
                return JsonResponse({
                    "status": 200,
                    "message": "Votre compte a été créé avec succès"
                })
    else:
        return JsonResponse({
            "status": 400,
            "message": "Vous n'êtes pas autorisé à utilisé cette fonctionnalité"
        })

def logout(request):
    request.session.flush()
    return redirect("/login")

def dash_home(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.get(code=user_code)
        max_month = datetime.datetime.now().strftime("%Y-%m")
        max_day = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request, "admin-temp/index.html", {
        "user": utilisateur,
        "error": error,
        "success": success,
        "max_month": max_month,
        "max_day": max_day
    })

def profile(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.get(code=user_code)
    if request.POST:
        if "nom" in request.POST:
            nom = request.POST["nom"]
            prenoms = request.POST["prenoms"]
            date_naissance = request.POST["date_naissance"]
            email = request.POST["email"]
            image =  request.FILES.get("image", None)
            if nom =="" or prenoms == "" or date_naissance == "" or email == "":
                request.session["error"] = "Les champs ne sont pas optionnels."
                return redirect("/profil")
            if True:
                    utilisateur.nom = nom
                    utilisateur.prenom = prenoms
                    utilisateur.date_naissance = date_naissance
                    if image:
                        utilisateur.image = image
                    utilisateur.save()
                    request.session["success"] = "Votre compte a été modifié avec succès"
                    return redirect("/profil")
        elif "password" in request.POST:
            oldpassword = request.POST["oldpassword"]
            password = request.POST["password"]
            repassword = request.POST["repassword"]
            if chiffrement(oldpassword) != utilisateur.password:
                request.session["error"] = "Le mot de passe actuel est incorrect"
                return redirect("/profil")
            if password != repassword:
                request.session["error"] = "Les mots de passe ne correspondent pas"
                return redirect("/profil")
            else:
                if chiffrement(oldpassword) == utilisateur.password:
                    utilisateur.password = chiffrement(password)
                    utilisateur.save()
                    request.session["success"] = "Votre mot de passe a été modifié avec succès"
                    return redirect("/profil")
                else:
                    request.session["error"] = "Le mot de passe actuel est incorrect"
                    return redirect("/profil")
    return render(request, "admin-temp/profile.html", {
        "user": utilisateur,
        "error": error,
        "success": success
    })

def api_constanteAdd(request):
    user_code = request.session.get("user", None)
    if user_code is None:
        return JsonResponse({
            "status": 400,
            "message": "Vous n'êtes pas autorisé à utilisé cette fonctionnalité"
        })
    else:
        utilisateur = Utilisateur.objects.filter(code=user_code)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            nom = request.GET.get('constante', "")
            valeur = request.GET.get('valeur', None)
            if nom == "" or valeur == None:
                return JsonResponse({
                    "status": 400,
                    "message": "Les champs ne sont pas optionnels"
                })
            else:
                last_data = utilisateur.last_data()
                if utilisateur.has_save_data_today():
                    data = utilisateur.data_saved_today()
                    if nom == "Poids":
                        data.poids = int(valeur)
                    elif nom == "Taille":
                        data.taille = int(valeur)
                    elif nom == "Etat de grossesse":
                        if valeur == "Oui":
                            valeur = 1
                        else:
                            valeur = 0
                        data.etat_de_grossesse = valeur
                    elif nom == "Glycémie":
                        data.niveauInsuline = float(valeur)
                    data.save()
                elif last_data:
                    new_data = Donnee(
                        utilisateur = utilisateur,
                        age = calculer_age(utilisateur.date_naissance),
                        poids= last_data.poids,
                        taille = last_data.taille,
                        etat_de_grossesse = last_data.etat_de_grossesse,
                        niveauInsuline = last_data.niveauInsuline,
                    )
                    if nom == "Poids":
                        new_data.poids = int(valeur)
                    elif nom == "Taille":
                        new_data.taille = int(valeur)
                    elif nom == "Etat de grossesse":
                        if valeur == "Oui":
                            valeur = 1
                        else:
                            valeur = 0
                        new_data.etat_de_grossesse = valeur
                    elif nom == "Glycémie":
                        new_data.niveauInsuline = float(valeur)
                    new_data.save()
                else:
                    new_data = Donnee(
                        utilisateur = utilisateur,
                        age = calculer_age(utilisateur.date_naissance),
                    )
                    new_data.save()
                
                return JsonResponse({
                    "status": 200,
                    "message": "La constante a été ajoutée avec succès"
                    })
        else:
            return JsonResponse({
                "status": 400,
                "message": "Vous n'êtes pas autorisé à utilisé cette fonctionnalité"
            })

def poids(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.filter(code=user_code)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            donnees = Donnee.objects.filter(utilisateur=utilisateur)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.poids, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                poids = request.POST.get("poids", None)
                if poids == None:
                    request.session["error"] = "Le poids est obligatoire"
                    return redirect("/poids")
                else:
                    poids = int(poids)
                    if utilisateur.has_save_data_today():
                        data = utilisateur.data_saved_today()
                        data.poids = poids
                        data.save()
                    else:
                        if utilisateur.has_data():
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                age= utilisateur.age(),
                                poids = poids,
                                taille = utilisateur.last_data().taille,
                                etat_de_grossesse = utilisateur.last_data().etat_de_grossesse,
                                niveauInsuline = utilisateur.last_data().niveauInsuline,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                age = utilisateur.age(),
                                poids = poids
                            )
                            new_data.save()
                    request.session["success"] = "Le poids a été ajouté avec succès"
                    return redirect("/poids")
            else:
                return render(request, "admin-temp/poids-add.html", {
                    "user": utilisateur,
                    "donnees": datas,
                    "nb_donnees": len(datas),
                    "error": error,
                    "success": success,
                })
        else:
            return redirect("/login")

def taille(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.filter(code=user_code)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            donnees = Donnee.objects.filter(utilisateur=utilisateur)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.taille, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                taille = request.POST.get("taille", None)
                if taille == None:
                    request.session["error"] = "La taille est obligatoire"
                    return redirect("/taille")
                else:
                    taille = int(taille)
                    if utilisateur.has_save_data_today():
                        data = utilisateur.data_saved_today()
                        data.taille = taille
                        data.save()
                    else:
                        if utilisateur.has_data():
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                age= utilisateur.age(),
                                poids = utilisateur.last_data().poids,
                                taille = taille,
                                etat_de_grossesse = utilisateur.last_data().etat_de_grossesse,
                                niveauInsuline = utilisateur.last_data().niveauInsuline,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                taille = taille
                            )
                            new_data.save()
                    request.session["success"] = "La taille a été ajoutée avec succès"
                    return redirect("/taille")
            else:
                return render(request, "admin-temp/taille-add.html", {
                    "user": utilisateur,
                    "donnees": datas,
                    "nb_donnees": len(datas),
                    "error": error,
                    "success": success,
                })
        else:
            return redirect("/login")

def glycemie(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.filter(code=user_code)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            donnees = Donnee.objects.filter(utilisateur=utilisateur)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.niveauInsuline, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                glycemie = request.POST.get("glycemie", None)
                if glycemie == None:
                    request.session["error"] = "La glycémie est obligatoire"
                    return redirect("/glycemie")
                else:
                    try:
                        glycemie = float(glycemie.replace(",", "."))
                    except:
                        request.session["error"] = "La glycémie doit être un nombre"
                        return redirect("/glycemie")
                    if utilisateur.has_save_data_today():
                        data = utilisateur.data_saved_today()
                        data.niveauInsuline = glycemie
                        data.save()
                    else:
                        if utilisateur.has_data():
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                age= utilisateur.age(),
                                poids = utilisateur.last_data().poids,
                                taille = utilisateur.last_data().taille,
                                niveauInsuline = glycemie,
                                etat_de_grossesse = utilisateur.last_data().etat_de_grossesse,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                niveauInsuline = glycemie
                            )
                            new_data.save()
                    request.session["success"] = "Le niveau d'insuline a été ajoutée avec succès"
                    return redirect("/glycemie")
            else:
                return render(request, "admin-temp/glycemie-add.html", {
                        "user": utilisateur,
                        "donnees": datas,
                        "nb_donnees": len(datas),
                        "error": error,
                        "success": success,
                    })
        else:
            return redirect("/login")

def gestation(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.filter(code=user_code)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            donnees = Donnee.objects.filter(utilisateur=utilisateur)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.etat_de_grossesse, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                etat_de_grossesse = request.POST.get("enceinte", None)
                if etat_de_grossesse == None:
                    request.session["error"] = "L'état de grossesse est obligatoire"
                    return redirect("/gestation")
                else:
                    etat_de_grossesse = int(etat_de_grossesse)
                    if utilisateur.has_save_data_today():
                        data = utilisateur.data_saved_today()
                        data.etat_de_grossesse = etat_de_grossesse
                        data.save()
                    else:
                        if utilisateur.has_data():
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                age= utilisateur.age(),
                                poids = utilisateur.last_data().poids,
                                taille = utilisateur.last_data().taille,
                                niveauInsuline = utilisateur.last_data().niveauInsuline,
                                etat_de_grossesse = etat_de_grossesse,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                utilisateur = utilisateur,
                                etat_de_grossesse = etat_de_grossesse
                            )
                            new_data.save()
                        request.session["success"] = "L'état de grossesse a été ajoutée avec succès"
                    return redirect("/gestation")
            else:
                return render(request, "admin-temp/gestation-add.html", {
                            "user": utilisateur,
                            "donnees": datas,
                            "nb_donnees": len(datas),
                            "error": error,
                            "success": success,
                        })
        else:
            return redirect("/login")

def prediction(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.filter(code=user_code)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            donnees = Donnee.objects.filter(utilisateur=utilisateur)
            if donnees.exists():
                donnees = donnees.order_by("-date")
            else:
                request.session["error"] = "Aucune donnée n'a été trouvée. Veuillez renseigner vos constantes avant de pouvoir faire une prédiction."
                return redirect("/prediction")
        else:
            return redirect("/login")

def api_getGrapheDatas(request):
    user_code = request.session.get("user", None)
    if user_code is None:
        return redirect("/login")
    else:
        utilisateur = Utilisateur.objects.filter(code=user_code)
        if utilisateur.exists():
            utilisateur = utilisateur.first()
            donnees = Donnee.objects.filter(utilisateur=utilisateur)
            if donnees.exists():
                donnees = donnees.order_by("date")
                option = int(request.GET.get("option", None))
                if option == 0:
                    period = get_last_7_days_dates()
                    donnees = donnees.filter(date__gte=period[0], date__lte=period[-1])
                    period_str = get_last_7_days()
                elif option == 1:
                    mois = request.GET.get("mois", None)
                    if mois is None:
                        return JsonResponse({
                            "status": 400,
                            "message": "Le paramètre mois est obligatoire"
                        })
                    annee, mois = mois.split("-")
                    mois = int(mois)
                    annee = int(annee)
                    period = get_days_of_month(mois, annee)
                    donnees = donnees.filter(date__gte=period[0], date__lte=period[-1])
                    period_str = get_days_of_month_str(mois, annee)
                elif option == 2:
                    debut = request.GET.get("start", None)
                    fin = request.GET.get("end", None)
                    if debut is None or fin is None:
                        return JsonResponse({
                            "status": 400,
                            "message": "Le paramètre start et celui end sont obligatoires."
                        })
                    period = get_period_days(debut, fin)
                    donnees = donnees.filter(date__gte=period[0], date__lte=period[-1])
                    period_str = get_period_dates_str(debut, fin)
                constante = request.GET.get("constante", None)
                if constante is None:
                    return JsonResponse({
                        "status": 400,
                        "message": "Le paramètre constante est obligatoire"
                    })
                if constante == "Poids":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.poids)
                        else:
                            datas.append(0)
                elif constante == "Taille":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.taille)
                        elif is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[0]:
                            donnee = donnees.filter(date=is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[1]).first()
                            datas.append(donnee.taille)
                        else:
                            datas.append(0)
                elif constante == "Glycémie":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.niveauInsuline)
                        elif is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[0]:
                            donnee = donnees.filter(date=is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[1]).first()
                            datas.append(donnee.niveauInsuline)
                        else:
                            datas.append(0)
                elif constante == "Etat de grossesse":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.etat_de_grossesse)
                        elif is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[0]:
                            donnee = donnees.filter(date=is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[1]).first()
                            datas.append(donnee.etat_de_grossesse)
                        else:
                            datas.append(0)
                return JsonResponse({
                    "status": 200,
                    "datas": datas,
                    "period": period_str
                })
            else:
                return JsonResponse({
                    "status": 400,
                    "message": "Aucune donnée disponible."
                })
        else:
            return redirect("/login")
            
def predictions(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    user = Utilisateur.objects.filter(code=user_code).first()
    donnees = Donnee.objects.filter(utilisateur=user)
    for donnee in donnees:
        donnee.evaluate()
    donnees = donnees.order_by("-date")
    return render(request, "admin-temp/prediction.html",{
        "user": user,
        "error": error,
        "success": success,
        "donnees": donnees,
        "nb_donnees": donnees.count()
    })

def patients(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    user = Utilisateur.objects.filter(code=user_code).first()
    patients = Patient.objects.filter(docteur=user)
    return render(request, "admin-temp/patients.html",{
        "user": user,
        "error": error,
        "success": success,
        "patients": patients,
        "nb_donnees": patients.count()
    })

def add_patient(request):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    user = Utilisateur.objects.filter(code=user_code).first()
    max_day = datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        nom = request.POST.get("nom", None)
        prenom = request.POST.get("prenom", None)
        date_naissance = request.POST.get("date_naissance", None)
        sexe = bool(int(request.POST.get("sexe")))
        telephone = request.POST.get("telephone", None)
        if nom is None or prenom is None or date_naissance is None or telephone is None:
            request.session["error"] = "Veuillez remplir tous les champs."
            return redirect("/add_patient")
        patient = Patient(
            nom=nom, 
            prenom=prenom,
            date_naissance= date_naissance,
            sexe = sexe,
            telephone = "+229" + telephone,
            docteur = user
        )
        patient.save()
        request.session["success"] = "Le patient a été ajouté avec succès."
        return redirect("/patients")
    return render(request, "admin-temp/add_patient.html",{
        "user": user,
        "error": error,
        "success": success,
        "max_day": max_day
    })

def delete_patient(request, code):
    user_code = request.session.get("user", None)
    if user_code is None:
        return redirect("/login")
    user = Utilisateur.objects.filter(code=user_code).first()
    if user.profil.id == 3:
        patient = Patient.objects.filter(code=code).first()
        if patient is not None:
            patient.delete()
            request.session["success"] = "Le patient a été supprimé avec succès."
            return redirect("/patients")
        else:
            return redirect("/patients")
    else:
        request.session["error"] = "Vous n'avez pas les droits pour accéder à cette fonctionnalité."
        return redirect("/patients")

def dash_patient(request, code):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    user = Utilisateur.objects.filter(code=user_code).first()
    if user.profil.id == 3:
        patient = Patient.objects.filter(code=code).first()
        if patient is not None:
            donnees = Donnee.objects.filter(patient=patient)
            for donnee in donnees:
                donnee.evaluate()
            donnees = donnees.order_by("-date")
            return render(request, "admin-temp/dash_patient.html",{
                "user": user,
                "error": error,
                "success": success,
                "patient": patient,
                "donnees": donnees,
                "nb_donnees": donnees.count()
            })
        else:
            request.session["error"] = "Le patient n'existe pas."
            return redirect("/patients")
    else:
        request.session["error"] = "Vous n'avez pas les droits pour accéder à cette fonctionnalité."
        return redirect("/patients")

def api_getGrapheDatasPatient(request, code):
    user_code = request.session.get("user", None)
    if user_code is None:
        return redirect("/login")
    else:
        patient = Patient.objects.filter(code=code)
        if patient.exists():
            patient = patient.first()
            donnees = Donnee.objects.filter(patient=patient)
            if donnees.exists():
                donnees = donnees.order_by("date")
                option = int(request.GET.get("option", None))
                if option == 0:
                    period = get_last_7_days_dates()
                    donnees = donnees.filter(date__gte=period[0], date__lte=period[-1])
                    period_str = get_last_7_days()
                elif option == 1:
                    mois = request.GET.get("mois", None)
                    if mois is None:
                        return JsonResponse({
                            "status": 400,
                            "message": "Le paramètre mois est obligatoire"
                        })
                    annee, mois = mois.split("-")
                    mois = int(mois)
                    annee = int(annee)
                    period = get_days_of_month(mois, annee)
                    donnees = donnees.filter(date__gte=period[0], date__lte=period[-1])
                    period_str = get_days_of_month_str(mois, annee)
                elif option == 2:
                    debut = request.GET.get("start", None)
                    fin = request.GET.get("end", None)
                    if debut is None or fin is None:
                        return JsonResponse({
                            "status": 400,
                            "message": "Le paramètre start et celui end sont obligatoires."
                        })
                    period = get_period_days(debut, fin)
                    donnees = donnees.filter(date__gte=period[0], date__lte=period[-1])
                    period_str = get_period_dates_str(debut, fin)
                constante = request.GET.get("constante", None)
                if constante is None:
                    return JsonResponse({
                        "status": 400,
                        "message": "Le paramètre constante est obligatoire"
                    })
                if constante == "Poids":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.poids)
                        else:
                            datas.append(0)
                elif constante == "Taille":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.taille)
                        elif is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[0]:
                            donnee = donnees.filter(date=is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[1]).first()
                            datas.append(donnee.taille)
                        else:
                            datas.append(0)
                elif constante == "Glycémie":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.niveauInsuline)
                        elif is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[0]:
                            donnee = donnees.filter(date=is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[1]).first()
                            datas.append(donnee.niveauInsuline)
                        else:
                            datas.append(0)
                elif constante == "Etat de grossesse":
                    datas = []
                    for jour in period:
                        if donnees.filter(date=jour).exists():
                            donnee = donnees.filter(date=jour).first()
                            datas.append(donnee.etat_de_grossesse)
                        elif is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[0]:
                            donnee = donnees.filter(date=is_date_in_intervals(jour, donnees.values_list("date", flat=True).all())[1]).first()
                            datas.append(donnee.etat_de_grossesse)
                        else:
                            datas.append(0)
                return JsonResponse({
                    "status": 200,
                    "datas": datas,
                    "period": period_str
                })
            else:
                return JsonResponse({
                    "status": 400,
                    "message": "Aucune donnée disponible."
                })
        else:
            return redirect("/login")
 
def constantes_patient(request, code):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    user = Utilisateur.objects.filter(code=user_code).first()
    patient = Patient.objects.filter(code=code)
    if not patient.exists():
        request.session["error"] = "Ce patient n'existe pas."
    else:
        patient = patient.first()
    if user is None:
        return redirect("/login")
    return render(request, "admin-temp/constantes_patient.html", {
        "user": user,
        "error": error,
        "success": success,
        "patient": patient
    })

def poids_patient(request, code):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        user = Utilisateur.objects.filter(code=user_code).first()
        patient = Patient.objects.filter(code=code)
        if patient.exists():
            patient = patient.first()
            donnees = Donnee.objects.filter(patient=patient)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.poids, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                poids = request.POST.get("poids", None)
                if poids == None:
                    request.session["error"] = "Le poids est obligatoire"
                    return redirect(f"/poids_patient/{code}")
                else:
                    poids = int(poids)
                    if patient.has_save_data_today():
                        data = patient.data_saved_today()
                        data.poids = poids
                        data.save()
                    else:
                        if patient.has_data():
                            new_data = Donnee(
                                patient = patient,
                                age= patient.age(),
                                poids = poids,
                                taille = patient.last_data().taille,
                                etat_de_grossesse = patient.last_data().etat_de_grossesse,
                                niveauInsuline = patient.last_data().niveauInsuline,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                patient = patient,
                                age = patient.age(),
                                poids = poids
                            )
                            new_data.save()
                    request.session["success"] = "Le poids a été ajouté avec succès"
                    return redirect(f"/poids_patient/{code}")
            else:
                return render(request, "admin-temp/poids-add.html", {
                    "user": user,
                    "donnees": datas,
                    "patient": patient,
                    "nb_donnees": len(datas),
                    "error": error,
                    "success": success,
                })
        else:
            return redirect("/login")

def taille_patient(request, code):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        user = Utilisateur.objects.filter(code=user_code).first()
        patient = Patient.objects.filter(code=code)
        if patient.exists():
            patient = patient.first()
            donnees = Donnee.objects.filter(patient=patient)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.taille, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                taille = request.POST.get("taille", None)
                if taille == None:
                    request.session["error"] = "La taille est obligatoire"
                    return redirect(f"/taille_patient/{code}")
                else:
                    taille = int(taille)
                    if patient.has_save_data_today():
                        data = patient.data_saved_today()
                        data.taille = taille
                        data.save()
                    else:
                        if patient.has_data():
                            new_data = Donnee(
                                patient = patient,
                                age= patient.age(),
                                poids = patient.last_data().poids,
                                taille = taille,
                                etat_de_grossesse = patient.last_data().etat_de_grossesse,
                                niveauInsuline = patient.last_data().niveauInsuline,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                patient = patient,
                                age = patient.age(),
                                taille = taille
                            )
                            new_data.save()
                    request.session["success"] = "La taille a été ajouté avec succès"
                    return redirect(f"/taille_patient/{code}")
            else:
                return render(request, "admin-temp/taille-add.html", {
                    "user": user,
                    "donnees": datas,
                    "patient": patient,
                    "nb_donnees": len(datas),
                    "error": error,
                    "success": success,
                })

def glycemie_patient(request, code):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        user = Utilisateur.objects.filter(code=user_code).first()
        patient = Patient.objects.filter(code=code)
        if patient.exists():
            patient = patient.first()
            donnees = Donnee.objects.filter(patient=patient)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.niveauInsuline, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                glycemie = request.POST.get("glycemie", None)
                if glycemie == None:
                    request.session["error"] = "La glycemie est obligatoire"
                    return redirect(f"/glycemie_patient/{code}")
                else:
                    glycemie = glycemie.replace(",", ".")
                    glycemie = float(glycemie)
                    if patient.has_save_data_today():
                        data = patient.data_saved_today()
                        data.niveauInsuline = glycemie
                        data.save()
                    else:
                        if patient.has_data():
                            new_data = Donnee(
                                patient = patient,
                                age= patient.age(),
                                poids = patient.last_data().poids,
                                taille = patient.last_data().taille,
                                niveauInsuline = glycemie,
                                etat_de_grossesse = patient.last_data().etat_de_grossesse,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                patient = patient,
                                age = patient.age(),
                                niveauInsuline = glycemie
                            )
                            new_data.save()
                    request.session["success"] = "La glycemie a été ajouté avec succès"
                    return redirect(f"/glycemie_patient/{code}")
            else:
                    return render(request, "admin-temp/glycemie-add.html", {
                        "user": user,
                        "donnees": datas,
                        "patient": patient,
                        "nb_donnees": len(datas),
                        "error": error,
                        "success": success,
                    })

def gestation_patient(request, code):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    else:
        user = Utilisateur.objects.filter(code=user_code).first()
        patient = Patient.objects.filter(code=code)
        if patient.exists():
            patient = patient.first()
            donnees = Donnee.objects.filter(patient=patient)
            if donnees.exists():
                donnees = donnees.order_by("-date")
                datas = [{'valeur': donnee.etat_de_grossesse, 'date': date_to_text(donnee.date)} for donnee in donnees]
            else:
                datas = []
            if request.method == "POST":
                etat_de_grossesse = request.POST.get("enceinte", None)
                if etat_de_grossesse == None:
                    request.session["error"] = "L'état de grossesse est obligatoire"
                    return redirect(f"/gestation_patient/{code}")
                else:
                    if patient.has_save_data_today():
                        data = patient.data_saved_today()
                        data.etat_de_grossesse = etat_de_grossesse
                        data.save()
                    else:
                        if patient.has_data():
                            new_data = Donnee(
                                patient = patient,
                                age= patient.age(),
                                poids = patient.last_data().poids,
                                taille = patient.last_data().taille,
                                niveauInsuline = patient.last_data().niveauInsuline,
                                etat_de_grossesse = etat_de_grossesse,
                            )
                            new_data.save()
                        else:
                            new_data = Donnee(
                                patient = patient,
                                age = patient.age(),
                                etat_de_grossesse = etat_de_grossesse
                            )
                            new_data.save()
                    request.session["success"] = "L'état de grossesse a été ajouté avec succès"
                    return redirect(f"/gestation_patient/{code}")
            else:
                    return render(request, "admin-temp/gestation-add.html", {
                        "user": user,
                        "donnees": datas,
                        "patient": patient,
                        "nb_donnees": len(datas),
                        "error": error,
                        "success": success,
                    })

def predictions_patient(request, code):
    user_code = request.session.get("user", None)
    error = request.session.pop("error", None)
    success = request.session.pop("success", None)
    if user_code is None:
        return redirect("/login")
    user = Utilisateur.objects.filter(code=user_code).first()
    patient = Patient.objects.filter(code=code)
    if patient.exists():
        patient = patient.first()
    else:
        request.session["error"] = "Le patient n'existe pas"
        return redirect("/patients")
    donnees = Donnee.objects.filter(patient=patient)
    for donnee in donnees:
        donnee.evaluate()
    donnees = donnees.order_by("-date")
    return render(request, "admin-temp/prediction.html",{
        "user": user,
        "patient": patient,
        "error": error,
        "success": success,
        "donnees": donnees,
        "nb_donnees": donnees.count()
    })
