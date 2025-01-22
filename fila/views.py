from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def fila(request):
    return render(request, "fila/fila.html")
    
@login_required
def detalhes(request):
    return render(request, "fila/detalhes.html")
