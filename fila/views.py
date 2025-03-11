from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from solicitacao.models import Solicitacao
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from core.permissions import CheckUserBolsistaMixin

class FilaView(LoginRequiredMixin, ListView):
    """
    View para exibir a lista de solicitações ativas no sistema.
    
    Exibe solicitações que não estão concluídas ou canceladas, com diferentes
    filtros baseados no tipo de usuário (superusuário, professor ou bolsista).
    Suporta paginação e filtros por status, tipo de atividade e título.
    
    Attributes:
        model: Modelo Solicitacao
        template_name: HTML
        context_object_name: Nome do contexto para a lista de solicitações
        paginate_by: Número de itens por página
        page_kwarg: Nome do parâmetro de página na URL
    """
    
    model = Solicitacao
    template_name = "fila/fila.html"
    context_object_name = "solicitacoes"
    paginate_by = 8
    page_kwarg = 'pagina'

    def _base_queryset(self):
        """
        Retorna o queryset base excluindo solicitações concluídas ou canceladas.
        
        Returns:
            QuerySet: Solicitações ativas
        """
        return Solicitacao.objects.exclude(
            Q(status=Solicitacao.StatusChoices.CONCLUIDA) | 
            Q(status=Solicitacao.StatusChoices.CANCELADA)
        ).order_by('data_entrega')

    def get_queryset(self):
        """
        Retorna o queryset filtrado baseado no tipo de usuário e parâmetros da URL.
        
        Filtragem específica para cada tipo de usuário:
        - Superusuário: acesso a todas as solicitações
        - Professor: apenas suas próprias solicitações
        - Bolsista: apenas solicitações para entrega de bolsistas, exceto provas
        
        Também aplica filtros adicionais:
        - status: filtra por status
        - tipo: filtra por tipo de atividade
        - titulo: filtra por texto no título
        
        Returns:
            QuerySet: Solicitações filtradas
        
        Raises:
            PermissionDenied: Se o usuário não tiver permissão
        """
        queryset = self._base_queryset()
        usuario = self.request.user
        
        if usuario.is_superuser:
            queryset = queryset
        elif usuario.groups.filter(name="Professor").exists():
            queryset = queryset.filter(usuario=usuario)
        elif usuario.groups.filter(name="Bolsista").exists():
            queryset = queryset.filter(
                tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA
            ).exclude(tipo_atividade=Solicitacao.TipoAtividadeChoices.PROVA)
        else:
            raise PermissionDenied

        # aplicar filtros da url
        status_filter = self.request.GET.get('status')
        tipo_filter = self.request.GET.get('tipo')
        titulo_filter = self.request.GET.get('titulo')

        # filtrar por status
        if status_filter:
            status_list = status_filter.split(',')
            status_query = Q()
            for status in status_list:
                if status == 'pendente':
                    status_query |= Q(status=Solicitacao.StatusChoices.PENDENTE)
                elif status == 'em_andamento':
                    status_query |= Q(status=Solicitacao.StatusChoices.EM_ANDAMENTO)
                elif status == 'aguardando_retirada':
                    status_query |= Q(status=Solicitacao.StatusChoices.AGUARDANDO_RETIRADA)
                elif status == 'aguardando_entrega':
                    status_query |= Q(status=Solicitacao.StatusChoices.AGUARDANDO_ENTREGA)
            queryset = queryset.filter(status_query)

        # filtrar por tipo de atividade
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

        # filtrar por nome
        if titulo_filter:
            queryset = queryset.filter(Q(titulo__icontains=titulo_filter))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adiciona dados de contexto para o template.
        
        Contextos:
        - Total de solicitações
        - Número de itens na página atual (paginacao)
        - Range de itens sendo exibidos (paginacao)
        
        Returns:
            context: Contexto com informações
        """
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_solicitacoes'] = queryset.count()
        
        page = context['page_obj']
        context['itens_pagina_atual'] = len(page.object_list)
        context['inicio_range'] = (page.number - 1) * self.paginate_by + 1
        context['fim_range'] = min((page.number - 1) * self.paginate_by + len(page.object_list), context['total_solicitacoes'])
        
        return context


class DetalhesView(LoginRequiredMixin, DetailView):
    """
    View para exibir os detalhes de uma solicitação específica.
    
    Controla o acesso aos detalhes baseado no tipo de usuário:
    - Superusuário: acesso a todas as solicitações
    - Professor: apenas suas próprias solicitações
    - Bolsista: apenas solicitações para entrega de bolsistas, exceto provas
    
    Attributes:
        model: Modelo Solicitacao
        template_name: Template HTML para renderização
        context_object_name: Nome do contexto para a solicitação
    """
    
    model = Solicitacao
    template_name = "fila/detalhes.html"
    context_object_name = "solicitacao"

    def get_context_data(self, **kwargs):
        """
        Adiciona a solicitação específica ao contexto.
        
        Returns:
            context: Contexto com a solicitação solicitada
        """
        context = super().get_context_data(**kwargs)
        context["solicitacao"] = Solicitacao.objects.get(id=self.kwargs["pk"])
        return context

    def get_object(self):
        """
        Retorna o objeto solicitação se o usuário tiver permissão.
        
        Returns:
            Solicitacao: Objeto da solicitação
            
        Raises:
            PermissionDenied: Se o usuário não tiver permissão para ver a solicitação
        """
        obj = super().get_object()
        usuario = self.request.user

        if usuario.is_superuser:
            return obj
        
        if usuario.groups.filter(name="Professor").exists():
            if obj.usuario != usuario:
                raise PermissionDenied
        
        if usuario.groups.filter(name="Bolsista").exists():
            if obj.tipo_atividade == Solicitacao.TipoAtividadeChoices.PROVA:
                raise PermissionDenied
            
            if obj.tipo_entrega != Solicitacao.TipoEntregaChoices.BOLSISTA:
                raise PermissionDenied
            
            if obj.status == Solicitacao.StatusChoices.CONCLUIDA and obj.entregue_por != usuario:
                raise PermissionDenied
        
        return obj

class AtualizarStatusView(LoginRequiredMixin, View):
    """
    View para atualizar o status de uma solicitação.
    
    Apenas superusuários podem atualizar o status de solicitações.
    """
    
    def post(self, request, pk, *args, **kwargs):
        """
        Processa a requisição POST para atualizar o status.
        
        Args:
            request: Requisição HTTP
            pk: ID da solicitação
            
        Returns:
            JsonResponse: Resposta JSON indicando sucesso ou falha
            
        Raises:
            PermissionDenied: Se o usuário não for superusuário
        """
        solicitacao = get_object_or_404(Solicitacao, pk=pk)
        novo_status = request.POST.get('novo_status')
        
        # validar status
        valid_status = [choice[0] for choice in Solicitacao.StatusChoices.choices]
        if novo_status not in valid_status:
            return JsonResponse({'success': False, 'message': 'Status inválido'}, status=400)
        
        try:
            if request.user.is_superuser:
                solicitacao.status = novo_status
                solicitacao.save()
                return JsonResponse({'success': True, 'message': 'Status atualizado com sucesso!'})

            raise PermissionDenied
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

class MarcarEntregueView(LoginRequiredMixin, CheckUserBolsistaMixin, View):
    """
    View para marcar uma solicitação como entregue.
    
    Apenas bolsistas podem marcar solicitações como entregues.
    """
    
    def post(self, request, pk):
        """
        Processa a requisição POST para marcar como entregue.
        
        Args:
            request: Requisição HTTP
            pk: ID da solicitação
            
        Returns:
            JsonResponse: Resposta JSON indicando sucesso ou falha
        """
        solicitacao = get_object_or_404(Solicitacao, pk=pk)
        
        try:
            # usa o metodo entregar do model Solicitacao
            solicitacao.entregar(request.user)
            return JsonResponse({
                'success': True,
                'message': 'Solicitação marcada como entregue com sucesso!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Não foi possível marcar a solicitação como entregue.'
            }, status=400)
