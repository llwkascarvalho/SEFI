from django.urls import path
from core import views

# urls
urlpatterns = [
    path('', views.professorIndex, name='professor-index'),
]