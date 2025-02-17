from django import forms
from solicitacao.models import Solicitacao
from datetime import datetime
import os

class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['titulo', 'quantidade_copias', 'grampos', 'tipo_entrega', 'tipo_atividade',
               'data_entrega', 'tipo_impressao', 'arquivo']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'id': 'titulo', 'placeholder': 'Exercício de fixação...'}),
            'quantidade_copias': forms.NumberInput(attrs={'id': 'quantidade_copias', 'placeholder': '30'}),
            'grampos': forms.Select(attrs={'id': 'grampos'}, choices=[(True, 'Sim'), (False, 'Não')]),
            'tipo_entrega': forms.Select(attrs={'id': 'tipo_entrega'}),
            'tipo_atividade': forms.Select(attrs={'id': 'tipo_atividade'}),
            'data_entrega': forms.DateInput(attrs={'id': 'data_entrega', 'type': 'date'}),
            'tipo_impressao': forms.Select(attrs={'id': 'tipo_impressao'}),
            'arquivo': forms.FileInput(attrs={'id': 'arquivo', 'class': 'file-input'}),
        }

        error_messages = {
            'titulo': {
                'required': 'O título é obrigatório.',
                'min_length': 'O título deve ter pelo menos 1 caractere.',
            },
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']

        if len(titulo) < 1:
            raise forms.ValidationError('O título deve ter pelo menos 1 caractere.')

        if titulo.isdigit():
            raise forms.ValidationError('O título não pode ser apenas números.')
        
        return titulo
    
    def clean_quantidade_copias(self):
        quantidade_copias = self.cleaned_data['quantidade_copias']

        if quantidade_copias < 1:
            raise forms.ValidationError('A quantidade de cópias deve ser pelo menos 1.')
        elif quantidade_copias > 100:
            raise forms.ValidationError('A quantidade de cópias não pode ser maior que 100.')

        return quantidade_copias

    def clean_data_entrega(self):
        data_entrega = self.cleaned_data['data_entrega']

        if data_entrega < datetime.now().date():
            raise forms.ValidationError('A data de entrega não pode ser anterior a data atual.')
        return data_entrega

    def clean_arquivo(self):
        arquivo = self.cleaned_data['arquivo']
        
        if not arquivo:
            raise forms.ValidationError('É necessário enviar um arquivo.')

        return arquivo

