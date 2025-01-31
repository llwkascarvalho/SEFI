from django.urls import path
from solicitacao.views import NovaSolicitacaoView

urlpatterns = [
    path('', NovaSolicitacaoView.as_view(), name='nova-solicitacao'),
]