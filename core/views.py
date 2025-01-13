from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# views
@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'core/admin/admin-index.html')
    elif user.groups.filter(name='Professor').exists():
        return render(request, 'core/professor-index.html')
    elif user.groups.filter(name='Bolsista').exists():
        return render(request, 'core/bolsista-index.html')
    else:
        return redirect('login')
    
def perfil(request):
    user = request.user
    
    if user.is_superuser:
        return render(request, 'core/perfil-usuario/admin-perfil.html', {'user': user})
    elif user.groups.filter(name='Professor').exists():
        return render(request, 'core/perfil-usuario/professor-perfil.html', {'user': user})
    elif user.groups.filter(name='Bolsista').exists():
        return render(request, 'core/perfil-usuario/bolsista-perfil.html', {'user': user})
    else:
        return redirect('login')

def estatisticas(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'core/admin/admin-estatisticas.html')
    else:
        return redirect('login')