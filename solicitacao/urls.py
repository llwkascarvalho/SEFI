from django.urls import path
from solicitacao.views import NovaSolicitacaoView, SolicitacaoUpdateView, SolicitacaoDeleteView

urlpatterns = [
    path('', NovaSolicitacaoView.as_view(), name='nova-solicitacao'),
    path('editar/<int:pk>/', SolicitacaoUpdateView.as_view(), name='editar_solicitacao'),
    path('excluir/<int:pk>/', SolicitacaoDeleteView.as_view(), name='excluir_solicitacao'),
]