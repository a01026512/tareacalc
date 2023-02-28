from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def nuvea():
    return 0

def index(request):
    return render(request, 'index.html')

def procesamiento(request):
    nombre = request.POST['nombre']
    nombre = nombre.title()
    return render(request, 'proceso.html', {'name':nombre})