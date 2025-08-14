from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class PerfilUsuarioForm(forms.ModelForm):
    """Formulário para perfil do usuário"""
    class Meta:
        model = PerfilUsuario
        fields = [
            'cpf', 'cad_unico', 'tipo_usuario', 'data_nascimento', 
            'telefone', 'endereco', 'bairro', 'cidade', 'estado', 'cep'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'cep': forms.TextInput(attrs={'placeholder': '00000-000'}),
        }

class AnamneseForm(forms.ModelForm):
    """Formulário para anamnese"""
    class Meta:
        model = Anamnese
        fields = [
            'possui_alergias', 'alergias_descricao', 'medicamentos_uso', 
            'problemas_saude', 'ultima_consulta', 'frequencia_escovacao',
            'usa_fio_dental', 'frequencia_fio_dental', 'problemas_bucais',
            'dor_dentes', 'sangramento_gengiva', 'problemas_odontologicos_familia'
        ]
        widgets = {
            'ultima_consulta': forms.DateInput(attrs={'type': 'date'}),
            'frequencia_escovacao': forms.Select(choices=[
                ('', 'Selecione...'),
                ('1x_dia', '1 vez por dia'),
                ('2x_dia', '2 vezes por dia'),
                ('3x_dia', '3 vezes por dia'),
                ('mais_3x', 'Mais de 3 vezes por dia'),
            ]),
            'frequencia_fio_dental': forms.Select(choices=[
                ('', 'Selecione...'),
                ('nunca', 'Nunca'),
                ('raramente', 'Raramente'),
                ('1x_dia', '1 vez por dia'),
                ('2x_dia', '2 vezes por dia'),
                ('mais_2x', 'Mais de 2 vezes por dia'),
            ]),
        }

class ConsultaForm(forms.ModelForm):
    """Formulário para agendamento de consultas"""
    class Meta:
        model = Consulta
        fields = ['data_hora', 'tipo_consulta', 'observacoes']
        widgets = {
            'data_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'tipo_consulta': forms.Select(choices=[
                ('', 'Selecione o tipo de consulta...'),
                ('consulta_rotina', 'Consulta de Rotina'),
                ('limpeza', 'Limpeza Dental'),
                ('avaliacao', 'Avaliação Odontológica'),
                ('tratamento_canal', 'Tratamento de Canal'),
                ('extracao', 'Extração'),
                ('restauracao', 'Restauração'),
                ('ortodontia', 'Ortodontia'),
                ('emergencia', 'Emergência'),
            ]),
            'observacoes': forms.Textarea(attrs={'rows': 4}),
        }

class MensagemSuporteForm(forms.ModelForm):
    """Formulário para mensagens de suporte"""
    class Meta:
        model = MensagemSuporte
        fields = ['assunto', 'mensagem']
        widgets = {
            'assunto': forms.TextInput(attrs={'placeholder': 'Digite o assunto da sua dúvida'}),
            'mensagem': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Descreva sua dúvida ou problema detalhadamente...'
            }),
        }

class QuizForm(forms.ModelForm):
    """Formulário para criação de quizzes"""
    class Meta:
        model = Quiz
        fields = ['titulo', 'descricao', 'ativo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class PerguntaQuizForm(forms.ModelForm):
    """Formulário para perguntas do quiz"""
    class Meta:
        model = PerguntaQuiz
        fields = ['pergunta', 'ordem']
        widgets = {
            'pergunta': forms.Textarea(attrs={'rows': 3}),
        }

class AlternativaQuizForm(forms.ModelForm):
    """Formulário para alternativas do quiz"""
    class Meta:
        model = AlternativaQuiz
        fields = ['texto', 'correta']

class ConteudoEducativoForm(forms.ModelForm):
    """Formulário para conteúdo educativo"""
    class Meta:
        model = ConteudoEducativo
        fields = ['titulo', 'categoria', 'conteudo', 'imagem', 'ativo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 10}),
        }

class LembreteForm(forms.ModelForm):
    """Formulário para lembretes"""
    class Meta:
        model = Lembrete
        fields = ['titulo', 'descricao', 'tipo', 'data_lembrete']
        widgets = {
            'data_lembrete': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

# Formulário de busca
class BuscaForm(forms.Form):
    """Formulário de busca"""
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite sua busca...',
            'class': 'form-control'
        })
    )
    categoria = forms.ChoiceField(
        choices=[('', 'Todas as categorias')] + ConteudoEducativo.CATEGORIA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
