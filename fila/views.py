from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from solicitacao.models import Solicitacao
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

class FilaView(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = "fila/fila.html"
    context_object_name = "solicitacoes"

    def _base_queryset(self):
        return Solicitacao.objects.exclude(
            Q(status=Solicitacao.StatusChoices.CONCLUIDA) | 
            Q(status=Solicitacao.StatusChoices.CANCELADA)
        ).order_by('data_entrega')

    def get_queryset(self):
        queryset = self._base_queryset()
        usuario = self.request.user
        
        if usuario.is_superuser:
            return queryset
        
        if usuario.groups.filter(name="Professor").exists():
            return queryset.filter(usuario=usuario)
        
        if usuario.groups.filter(name="Bolsista").exists():
            return queryset.filter(tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA)
        
        raise PermissionDenied


class DetalhesView(LoginRequiredMixin, DetailView):
    model = Solicitacao
    template_name = "fila/detalhes.html"
    context_object_name = "solicitacao"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solicitacao"] = Solicitacao.objects.get(id=self.kwargs["pk"])
        return context

    def get_object(self):
        obj = super().get_object()
        usuario = self.request.user

        if usuario.is_superuser:
            return obj
        
        if usuario.groups.filter(name="Professor").exists():
            if obj.usuario != usuario:
                raise PermissionDenied
        
        if usuario.groups.filter(name="Bolsista").exists():
            if obj.tipo_entrega != Solicitacao.TipoEntregaChoices.BOLSISTA:
                raise PermissionDenied
        
        return obj

class AtualizarStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        solicitacao = get_object_or_404(Solicitacao, pk=pk)
        novo_status = request.POST.get('novo_status')
        
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
