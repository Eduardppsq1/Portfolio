from django.urls import path
from django.contrib import admin
from . import views

# Atunci cand pagina se va accesa folosind adresa:
#   - 127.0.0.1 -> se va afisa homepage-ul
#   - 127.0.0.1/app -> se vor afisa pictograme ce reprezinta subsisteme ale casei, si dedesubt valorile masurate.
#   - 127.0.0.1/despre -> se va afisa o pagina cu detalii despre aplicatie.
#   - 127.0.0.1/signup -> se va afisa un formular de inregistrare de cont.
urlpatterns = [
    path('', views.homepage, name = "homepage")
]