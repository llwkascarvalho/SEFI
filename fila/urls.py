from django.urls import path
from fila import views

# urls
urlpatterns = [
    path('', views.fila, name='fila'),
    path('/detalhes/', views.details, name='detalhes')
]