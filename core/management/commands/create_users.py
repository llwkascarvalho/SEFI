from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import CustomUser
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Cria usuários de teste para o sistema'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
                vinculo=CustomUser.VinculoChoices.COORDENADOR,
                matricula='2000000000001'
            )
            self.stdout.write(self.style.SUCCESS('Superuser criado com sucesso!'))

        # professor
        if not User.objects.filter(username='professor').exists():
            professor_group = Group.objects.get(name='Professor')
            professor = User.objects.create_user(
                username='professor',
                email='professor@example.com',
                password='testeProfessor123',
                vinculo=CustomUser.VinculoChoices.PROFESSOR,
                matricula='2000000000002'
            )
            professor_group.user_set.add(professor)
            self.stdout.write(self.style.SUCCESS('Professor criado com sucesso!'))

        # bolsista
        if not User.objects.filter(username='bolsista').exists():
            bolsista_group = Group.objects.get(name='Bolsista')
            bolsista = User.objects.create_user(
                username='bolsista',
                email='bolsista@example.com',
                password='testeBolsista123',
                vinculo=CustomUser.VinculoChoices.BOLSISTA,
                matricula='2000000000003'
            )
            bolsista_group.user_set.add(bolsista)
            self.stdout.write(self.style.SUCCESS('Bolsista criado com sucesso!'))