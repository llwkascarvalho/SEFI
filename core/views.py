from django.shortcuts import render

# views
def professorIndex(request):
    return render(request, 'core/professor-index.html')

def fila(request):
    return render(request, 'core/fila.html')