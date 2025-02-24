from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from solicitacao.models import Solicitacao
from django.db.models import Q
from django.core.exceptions import PermissionDenied

class HistoricoView(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = "historico/historico.html"
    context_object_name = "solicitacoes"
    paginate_by = 8
    page_kwarg = 'pagina'

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
        titulo_filter = self.request.GET.get('titulo')

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
            if tipo_query:
                queryset = queryset.filter(tipo_query)

        if titulo_filter:
            queryset = queryset.filter(Q(titulo__icontains=titulo_filter))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_solicitacoes'] = queryset.count()
        
        page = context['page_obj']
        context['itens_pagina_atual'] = len(page.object_list)
        context['inicio_range'] = (page.number - 1) * self.paginate_by + 1
        context['fim_range'] = min((page.number - 1) * self.paginate_by + len(page.object_list), context['total_solicitacoes'])
        
        return context