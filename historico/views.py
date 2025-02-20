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
            queryset = queryset
        elif usuario.groups.filter(name="Professor").exists():
            queryset = queryset.filter(usuario=usuario)
        elif usuario.groups.filter(name="Bolsista").exists():
            queryset = queryset.filter(
                entregue_por=usuario,
                tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA
            )
        else:
            raise PermissionDenied

        status_filter = self.request.GET.get('status')
        tipo_filter = self.request.GET.get('tipo')

        if status_filter:
            status_list = status_filter.split(',')
            status_query = Q()
            for status in status_list:
                if status == 'concluida':
                    status_query |= Q(status=Solicitacao.StatusChoices.CONCLUIDA)
                elif status == 'cancelada':
                    status_query |= Q(status=Solicitacao.StatusChoices.CANCELADA)
            queryset = queryset.filter(status_query)

        if tipo_filter:
            tipo_list = tipo_filter.split(',')
            tipo_query = Q()
            for tipo in tipo_list:
                tipo = tipo.lower()
                if tipo == 'exercicio':
                    tipo_query |= Q(tipo_atividade=Solicitacao.TipoAtividadeChoices.EXERCICIO)
                elif tipo == 'prova':
                    tipo_query |= Q(tipo_atividade=Solicitacao.TipoAtividadeChoices.PROVA)
                elif tipo == 'outro':
                    tipo_query |= Q(tipo_atividade=Solicitacao.TipoAtividadeChoices.OUTRO)
            queryset = queryset.filter(tipo_query)

        return queryset