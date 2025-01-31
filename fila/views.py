from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# mudar para listview
class FilaView(LoginRequiredMixin, TemplateView):
    template_name = "fila/fila.html"

# mudar para detailview
class DetalhesView(LoginRequiredMixin, TemplateView):
    template_name = "fila/detalhes.html"