from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Cria grupos iniciais para o sistema'

    def handle(self, *args, **kwargs):
        if not Group.objects.filter(name='Professor').exists():
            Group.objects.create(name='Professor')
            self.stdout.write(self.style.SUCCESS('Grupo Professor criado com sucesso!'))

        if not Group.objects.filter(name='Bolsista').exists():
            Group.objects.create(name='Bolsista')
            self.stdout.write(self.style.SUCCESS('Grupo Bolsista criado com sucesso!'))
