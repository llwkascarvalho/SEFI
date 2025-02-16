from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.permissions import CheckUserAdminMixin
from django.core.exceptions import ValidationError 
from django.http import JsonResponse 
from django.views import View 
    
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

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