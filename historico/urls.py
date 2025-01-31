from django.urls import path
from historico.views import HistoricoView

# urls
urlpatterns = [
    path('', HistoricoView.as_view(), name='historico'),
]