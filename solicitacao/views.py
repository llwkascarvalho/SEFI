from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from core.permissions import CheckUserProfessorMixin
from solicitacao.models import Solicitacao
from django.urls import reverse_lazy
from solicitacao.forms import SolicitacaoForm
from django.contrib import messages
from core.permissions import CheckSolicitacaoFromUserMixin

class NovaSolicitacaoView(CheckUserProfessorMixin, LoginRequiredMixin, CreateView): 
    model = Solicitacao
    template_name = "solicitacao/nova_solicitacao.html"
    form_class = SolicitacaoForm
    success_url = reverse_lazy('nova-solicitacao')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Solicitação enviada com sucesso!')
        return super().form_valid(form)

class SolicitacaoUpdateView(LoginRequiredMixin, CheckSolicitacaoFromUserMixin, UpdateView):
    model = Solicitacao
    form_class = SolicitacaoForm
    template_name = 'solicitacao/editar_solicitacao.html'
    
    def get_success_url(self):
        return reverse_lazy('detalhes', kwargs={'pk': self.object.pk})

class SolicitacaoDeleteView(LoginRequiredMixin, CheckSolicitacaoFromUserMixin, DeleteView):
    model = Solicitacao
    template_name = 'solicitacao/excluir_solicitacao.html'
    success_url = reverse_lazy('fila')
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)