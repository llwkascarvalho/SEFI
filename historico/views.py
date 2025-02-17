from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from solicitacao.models import Solicitacao
from django.db.models import Q

# mudar para listview
class HistoricoView(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = "historico/historico.html"
    context_object_name = "solicitacoes"

    def get_queryset(self):
        return Solicitacao.objects.filter(Q(status=Solicitacao.StatusChoices.CONCLUIDA) | 
                                          Q(status=Solicitacao.StatusChoices.CANCELADA))