from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# views
@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'core/admin-index.html')
    elif user.groups.filter(name='Professor').exists():
        return render(request, 'core/professor-index.html')
    elif user.groups.filter(name='Bolsista').exists():
        return render(request, 'core/bolsista-index.html')
    else:
        return redirect('login')