from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def fila(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'fila/admin-fila.html')
    elif user.groups.filter(name='Professor').exists():
        return render(request, 'fila/professor-fila.html')
    elif user.groups.filter(name='Bolsista').exists():
        return render(request, 'fila/bolsista-fila.html')
    else:
        return redirect('login')