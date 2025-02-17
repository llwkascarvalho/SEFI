from django.urls import path
from fila.views import FilaView, DetalhesView

# urls
urlpatterns = [
    path('', FilaView.as_view(), name='fila'),
    path('detalhes/<int:pk>/', DetalhesView.as_view(), name='detalhes')
]