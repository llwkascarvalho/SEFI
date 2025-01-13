from django.urls import path
from core import views

# urls
urlpatterns = [
    path('', views.index, name='index'),
    path('estatisticas', views.estatisticas, name='estatisticas'),
    path('perfil/', views.perfil, name='perfil-usuario'),
]