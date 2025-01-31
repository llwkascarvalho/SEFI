from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.permissions import CheckUserAdminMixin
    
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "core/perfil.html"

class EstatisticasView(CheckUserAdminMixin, LoginRequiredMixin, TemplateView):
    template_name = "core/estatisticas.html"