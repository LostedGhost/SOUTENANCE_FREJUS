from django.shortcuts import render, redirect
from django.http import JsonResponse
from app.models import *

# Create your views here.
def home(request):
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
    return render(request, "predict.html")

def dash_home(request):
    return render(request, "admin-temp/index.html")