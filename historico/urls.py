from django.urls import path
from historico import views

# urls
urlpatterns = [
    path('', views.historico, name='historico'),
]