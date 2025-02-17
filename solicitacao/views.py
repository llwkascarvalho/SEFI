from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from core.permissions import CheckUserProfessorMixin
from solicitacao.models import Solicitacao
from django.urls import reverse_lazy
from solicitacao.forms import SolicitacaoForm
from django.contrib import messages

class NovaSolicitacaoView(CheckUserProfessorMixin, LoginRequiredMixin, CreateView): 
    model = Solicitacao
    template_name = "solicitacao/nova_solicitacao.html"
    form_class = SolicitacaoForm
    success_url = reverse_lazy('nova-solicitacao')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Solicitação enviada com sucesso!')
        return super().form_valid(form)