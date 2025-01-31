from django.contrib.auth.mixins import UserPassesTestMixin

class CheckUserAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
class CheckUserProfessorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Professor").exists()