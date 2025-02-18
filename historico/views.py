from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from solicitacao.models import Solicitacao
from django.db.models import Q
from django.core.exceptions import PermissionDenied

class HistoricoView(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = "historico/historico.html"
    context_object_name = "solicitacoes"


    def base_queryset(self):
        return Solicitacao.objects.filter(
            Q(status=Solicitacao.StatusChoices.CONCLUIDA) | 
            Q(status=Solicitacao.StatusChoices.CANCELADA)
        ).order_by('data_entrega')

    def get_queryset(self):
        queryset = self.base_queryset()
        usuario = self.request.user
        
        if usuario.is_superuser:
            return queryset
        
        if usuario.groups.filter(name="Professor").exists():
            return queryset.filter(usuario=usuario)
        
        if usuario.groups.filter(name="Bolsista").exists():
            return queryset.filter(tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA)
        
        raise PermissionDenied