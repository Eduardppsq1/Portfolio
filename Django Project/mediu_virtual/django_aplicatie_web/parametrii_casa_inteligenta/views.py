from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

#Realizare functie de homepage.

def homepage(request):

    """Vom prelua datele din fisierele distanta_parcare.txt, intensitate_lumina.txt, temperatura_umiditate.txt,
    si prezenta_foc.txt ce reprezinta parametrii sistemului de casa inteligenta preluati de la Raspberry pi."""

    while True:
        with open(r'parametrii_casa_inteligenta/intensitate_lumina.txt','rt') as file_0:
            bec = float(file_0.readline())

        with open(r'parametrii_casa_inteligenta/distanta_parcare.txt','rt') as file_1:
            led = float(file_1.readline())

        with open(r'parametrii_casa_inteligenta/temperatura_umiditate.txt', 'rt') as file_2:
            file_2 = file_2.readline().split()
            ventilator_temperatura = float(file_2[2])
            ventilator_umiditate = float(file_2[5])

        with open(r'parametrii_casa_inteligenta/prezenta_foc.txt', 'rt') as file_3:
            foc = int(file_3.readline())

        # Se foloseste dictionarul context pentru a genera continut dinamic in pagina html homepage.
        context = {
                       'title' : 'Homepage',
                       'bec' : bec,
                       'led' : led,
                       'ventilator_temperatura' : ventilator_temperatura,
                       'ventilator_umiditate' : ventilator_umiditate,
                       'foc' : foc
                        }
        # Folosind functia render se va afisa pagina care foloseste continutul html din fisierul homepage.

        return render(request, template_name = "parametrii_casa_inteligenta/homepage.html", context = context)



