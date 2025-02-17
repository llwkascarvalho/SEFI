from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from solicitacao.models import Solicitacao
from django.db.models import Q

# mudar para listview
class FilaView(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = "fila/fila.html"
    context_object_name = "solicitacoes"

    def get_queryset(self):
        return Solicitacao.objects.filter(Q(status=Solicitacao.StatusChoices.PENDENTE) | 
                                          Q(status=Solicitacao.StatusChoices.EM_ANDAMENTO) | 
                                          Q(status=Solicitacao.StatusChoices.AGUARDANDO_ENTREGA) | 
                                          Q(status=Solicitacao.StatusChoices.AGUARDANDO_RETIRADA)).order_by('-data_solicitacao')

class DetalhesView(LoginRequiredMixin, DetailView):
    model = Solicitacao
    template_name = "fila/detalhes.html"
    context_object_name = "solicitacao"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solicitacao"] = Solicitacao.objects.get(id=self.kwargs["pk"])
        return context
