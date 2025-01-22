from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# views
@login_required
def index(request):
    return render(request, "core/index.html")
    
@login_required
def perfil(request):
    return render(request, "core/perfil.html")

@login_required
def estatisticas(request):
    user = request.user
    if user.is_superuser:
        return render(request, "core/estatisticas.html")
    else:
        return redirect("index")