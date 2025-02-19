from django.urls import path
from fila.views import FilaView, DetalhesView, AtualizarStatusView, MarcarEntregueView

# urls
urlpatterns = [
    path('', FilaView.as_view(), name='fila'),
    path('detalhes/<int:pk>/', DetalhesView.as_view(), name='detalhes'),
    path('detalhes/<int:pk>/atualizar-status/', AtualizarStatusView.as_view(), name='atualizar_status'),
    path('detalhes/<int:pk>/marcar-entregue/', MarcarEntregueView.as_view(), name='marcar_entregue'),
]