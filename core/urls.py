from django.urls import path
from core import views
from core.views import IndexView, PerfilView, EstatisticasView

# urls
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('estatisticas', EstatisticasView.as_view(), name='estatisticas'),
    path('perfil/', PerfilView.as_view(), name='perfil-usuario'),
]