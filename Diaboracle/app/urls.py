from django.urls import path
from app.views import *

urlpatterns = [
    path('', home, name="home"),
    path('dash', dash_home, name="dash_home"),
    path('predict_now', prediction_passant, name="prediction_passant"),
    path('predict_diabete_api', predict_diabete_api, name="predict_diabete_api"),
]