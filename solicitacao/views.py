from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def nova_solicitacao(request):
    user = request.user

    if user.groups.filter(name='Professor').exists():
        return render(request, 'solicitacao/nova_solicitacao.html')
    else:
        return redirect('index')