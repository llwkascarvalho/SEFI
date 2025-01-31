from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# mudar para listview
class HistoricoView(LoginRequiredMixin, TemplateView):
    template_name = "historico/historico.html"