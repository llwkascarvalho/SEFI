from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from core.permissions import CheckUserProfessorMixin
from solicitacao.models import Solicitacao
from django.urls import reverse_lazy
from solicitacao.forms import SolicitacaoForm
from django.contrib import messages
from core.permissions import CheckSolicitacaoFromUserMixin

class NovaSolicitacaoView(CheckUserProfessorMixin, LoginRequiredMixin, CreateView): 
    """
    View para criar uma nova solicitação no sistema.
    
    Apenas professores podem criar novas solicitações.
    Após criar com sucesso, exibe mensagem de confirmação.
    
    Attributes:
        model: Modelo Solicitacao
        template_name: HTML para renderização do formulário
        form_class: Formulário para criação da solicitação
        success_url: URL de redirecionamento após sucesso
    """
    
    model = Solicitacao
    template_name = "solicitacao/nova_solicitacao.html"
    form_class = SolicitacaoForm
    success_url = reverse_lazy('nova-solicitacao')

    def form_valid(self, form):
        """
        Valida e processa o formulário de nova solicitação.
        
        Define o usuário atual como autor da solicitação e
        exibe mensagem de sucesso.
        
        Args:
            form: Formulário preenchido
            
        Returns:
            HttpResponse: Redirecionamento após salvar
        """
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Solicitação enviada com sucesso!')
        return super().form_valid(form)

class SolicitacaoUpdateView(LoginRequiredMixin, CheckSolicitacaoFromUserMixin, UpdateView):
    """
    View para editar uma solicitação existente.
    
    Apenas o autor da solicitação pode editá-la.
    Após editar com sucesso, redireciona para a página de detalhes.
    
    Attributes:
        model: Modelo Solicitacao
        form_class: Formulário para edição da solicitação
        template_name: HTML para renderização do formulário
    """
    
    model = Solicitacao
    form_class = SolicitacaoForm
    template_name = 'solicitacao/editar_solicitacao.html'
    
    def get_success_url(self):
        """
        Define a URL de redirecionamento após edição com sucesso.
        
        Returns:
            str: URL da página de detalhes da solicitação
        """
        return reverse_lazy('detalhes', kwargs={'pk': self.object.pk})

class SolicitacaoDeleteView(LoginRequiredMixin, CheckSolicitacaoFromUserMixin, DeleteView):
    """
    View para excluir uma solicitação existente.
    
    Apenas o autor da solicitação pode excluí-la.
    Após excluir com sucesso, redireciona para a fila.
    
    Attributes:
        model: Modelo Solicitacao
        template_name: HTML para confirmação da exclusão
        success_url: URL de redirecionamento após sucesso
    """
    
    model = Solicitacao
    template_name = 'solicitacao/excluir_solicitacao.html'
    success_url = reverse_lazy('fila')
    
    def delete(self, request, *args, **kwargs):
        """
        Processa a exclusão da solicitação.
        
        Args:
            request: Requisição HTTP
            
        Returns:
            HttpResponse: Redirecionamento após excluir
        """
        return super().delete(request, *args, **kwargs)