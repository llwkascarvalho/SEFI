from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.permissions import CheckUserAdminMixin
from django.core.exceptions import ValidationError 
from django.http import JsonResponse 
from django.views import View 
from django.db.models import Q
from solicitacao.models import Solicitacao

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        if usuario.groups.filter(name='Professor').exists():
            context.update(self.get_professor_context(usuario))
        elif usuario.groups.filter(name='Bolsista').exists():
            context.update(self.get_bolsista_context(usuario))
        elif usuario.is_superuser:
            context.update(self.get_admin_context())

        return context
    
    def get_admin_context(self):
        return {
            'pendentes': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.PENDENTE).count(),
            'em_andamento': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.EM_ANDAMENTO).count(),
            'concluidas': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.CONCLUIDA).count(),
            'recentes': Solicitacao.objects.order_by('-data_solicitacao')[:3],
            'total_solicitacoes': Solicitacao.objects.count(),
            'solicitacao_mais_recente': Solicitacao.objects.order_by('-data_solicitacao').first()
        }

    def get_professor_context(self, usuario):
        return {
            'pendentes': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.PENDENTE,
                usuario=usuario).count(),
            'em_andamento': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.EM_ANDAMENTO,
                usuario=usuario).count(),
            'concluidas': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.CONCLUIDA,
                usuario=usuario).count(),
            'solicitacoes_pendentes': Solicitacao.objects.exclude(
                Q(status=Solicitacao.StatusChoices.CONCLUIDA) | 
                Q(status=Solicitacao.StatusChoices.CANCELADA)
            ).filter(usuario=usuario).order_by('-data_solicitacao')
        }

    def get_bolsista_context(self, usuario):
        return {
            'pendentes': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.PENDENTE,
                tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA).count(),
            'em_andamento': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.EM_ANDAMENTO,
                tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA).count(),
            'concluidas': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.CONCLUIDA,
                tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA,
                entregue_por=usuario).count(),
            'solicitacoes_ag_entrega': Solicitacao.objects.filter(
                status=Solicitacao.StatusChoices.AGUARDANDO_ENTREGA, 
                tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA),
            'ultima_solicitacao': Solicitacao.objects.filter(
                tipo_entrega=Solicitacao.TipoEntregaChoices.BOLSISTA).exclude(
                    status=Solicitacao.StatusChoices.CONCLUIDA).order_by('-data_solicitacao').first()
        }
    
class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "core/perfil.html"

class EstatisticasView(CheckUserAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = "core/estatisticas.html"

class AtualizarFotoPerfilView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        nova_foto = request.FILES.get('foto_perfil')
        
        if nova_foto:
            try:
                if nova_foto.size > 2 * 1024 * 1024:  # 2MB
                    raise ValidationError("O arquivo é muito grande. O tamanho máximo permitido é 2MB.")
                if not nova_foto.content_type.startswith('image'):
                    raise ValidationError("O arquivo deve ser uma imagem.")
                
                user.foto_perfil.save(nova_foto.name, nova_foto, save=True)
                return JsonResponse({'success': True, 'message': 'Foto de perfil atualizada com sucesso!'})
            except ValidationError as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        return JsonResponse({'success': False, 'message': 'Nenhuma foto foi enviada.'})