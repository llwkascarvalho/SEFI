from django.contrib.auth.mixins import UserPassesTestMixin
from solicitacao.models import Solicitacao
from django.core.exceptions import PermissionDenied

class CheckUserAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
class CheckUserProfessorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Professor").exists()
    
class CheckSolicitacaoFromUserMixin(UserPassesTestMixin):
    def test_func(self):
        solicitacao = self.get_object()
        usuario = self.request.user
        
        return (usuario == solicitacao.usuario and 
                solicitacao.status == solicitacao.StatusChoices.PENDENTE)
    
    def handle_no_permission(self):
        raise PermissionDenied("Você não tem permissão para modificar esta solicitação.")

class CheckUserBolsistaMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Bolsista").exists()
    
    def handle_no_permission(self):
        raise PermissionDenied("Você não tem permissão para modificar esta solicitação.")