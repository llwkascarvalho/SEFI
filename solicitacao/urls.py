from django.urls import path
from solicitacao import views

urlpatterns = [
    path('', views.nova_solicitacao, name='nova-solicitacao'),
]