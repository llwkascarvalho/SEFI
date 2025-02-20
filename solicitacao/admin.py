from django.contrib import admin
from solicitacao.models import Solicitacao

# Register your models here.

class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'data_solicitacao', 'status')
    list_filter = ('usuario', 'status', 'data_solicitacao')
    search_fields = ('usuario__username', 'status')
    ordering = ('-data_solicitacao',)

admin.site.register(Solicitacao, SolicitacaoAdmin)
