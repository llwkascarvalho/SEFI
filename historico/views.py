from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def historico(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'historico/admin-historico.html')
    elif user.groups.filter(name='Professor').exists():
        return render(request, 'historico/professor-historico.html')
    elif user.groups.filter(name='Bolsista').exists():
        return render(request, 'historico/bolsista-historico.html')
    else:
        return redirect('login')