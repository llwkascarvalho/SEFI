from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.permissions import CheckUserProfessorMixin

# mudar para createview depois   
class NovaSolicitacaoView(CheckUserProfessorMixin, LoginRequiredMixin, TemplateView): 
    template_name = "solicitacao/nova_solicitacao.html"