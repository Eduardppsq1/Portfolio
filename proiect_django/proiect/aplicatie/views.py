from django.shortcuts import render
from django.http import HttpResponse
from .models import Articol
from .models import Autor

def homepage(request):
    articole = Articol.objects.all()
    context = {'title':"Homepage",'articole':articole}
    return render(request, template_name = "aplicatie/homepage.html", context = context)

def despre(request):
    context = {'title':'Despre'}
    return render(request, template_name = "aplicatie/despre.html",context = context)

