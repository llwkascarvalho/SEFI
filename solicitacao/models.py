from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

# gera o caminho para salvar o arquivo: uploads/user_<id>/<filename>
def arquivo_path(instance, filename):
    return f'uploads/user_{instance.usuario.id}/{filename}'

class Solicitacao(models.Model):
    class TipoAtividadeChoices(models.TextChoices):
        EXERCICIO = 'Exercício', 'Exercício'
        PROVA = 'Prova', 'Prova'
        OUTRO = 'Outro', 'Outro'
    
    class TipoEntregaChoices(models.TextChoices):
        PESSOALMENTE = 'Pessoalmente', 'Pessoalmente'
        BOLSISTA = 'Bolsista', 'Bolsista'
    
    class TipoImpressaoChoices(models.TextChoices):
        COLORIDA = 'Colorida', 'Colorida'
        PRETO_BRANCO = 'Preto e branco', 'Preto e branco'

    class StatusChoices(models.TextChoices):
        PENDENTE = 'Pendente', 'Pendente'
        EM_ANDAMENTO = 'Em andamento', 'Em andamento'
        AGUARDANDO_ENTREGA = 'Aguardando entrega', 'Aguardando entrega'
        AGUARDANDO_RETIRADA = 'Aguardando retirada', 'Aguardando retirada'
        CONCLUIDA = 'Concluída', 'Concluída'
        CANCELADA = 'Cancelada', 'Cancelada'
    
    titulo = models.CharField('Título da Atividade', max_length=200)
    quantidade_copias = models.PositiveIntegerField(
        'Quantidade de cópias',
        validators=[MinValueValidator(1)]
    )
    grampos = models.BooleanField('Grampos', default=False)
    tipo_entrega = models.CharField(
        'Tipo de Entrega',
        max_length=20,
        choices=TipoEntregaChoices.choices,
        default=TipoEntregaChoices.PESSOALMENTE
    )
    tipo_atividade = models.CharField(
        'Tipo de Atividade',
        max_length=20,
        choices=TipoAtividadeChoices.choices,
        default=TipoAtividadeChoices.EXERCICIO
    )
    data_entrega = models.DateField('Data de Entrega')
    tipo_impressao = models.CharField(
        'Tipo de Impressão',
        max_length=20,
        choices=TipoImpressaoChoices.choices,
        default=TipoImpressaoChoices.PRETO_BRANCO
    )
    arquivo = models.FileField(
        'Arquivo',
        upload_to=arquivo_path,
        help_text='Upload do arquivo para impressão'
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Solicitante'
    )
    data_solicitacao = models.DateTimeField('Data da Solicitação', auto_now_add=True)
    status = models.CharField(
        'Status',
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE
    )

    # campos para rastreamento de entrega
    entregue_por = models.ForeignKey(
        'core.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitacoes_entregues'
    )
    data_entrega_efetiva = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data e hora em que a solicitação foi entregue ao solicitante"
    )

    @property
    def tempo_entrega(self):
        if self.data_entrega_efetiva:
            return self.data_entrega_efetiva - self.data_solicitacao
        return None

    def entregar(self, bolsista):
        if self.status == self.StatusChoices.AGUARDANDO_ENTREGA:
            self.status = self.StatusChoices.CONCLUIDA
            self.entregue_por = bolsista
            self.data_entrega_efetiva = timezone.now()
            self.save()

    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f'{self.titulo} - {self.usuario.username} - {self.data_entrega}'
