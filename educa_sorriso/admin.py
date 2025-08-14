from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cpf', 'tipo_usuario', 'cidade', 'estado', 'data_cadastro']
    list_filter = ['tipo_usuario', 'cidade', 'estado', 'data_cadastro']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'cpf']
    readonly_fields = ['data_cadastro']
    ordering = ['-data_cadastro']

@admin.register(Anamnese)
class AnamneseAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'data_preenchimento', 'possui_alergias', 'dor_dentes', 'sangramento_gengiva']
    list_filter = ['possui_alergias', 'dor_dentes', 'sangramento_gengiva', 'data_preenchimento']
    search_fields = ['paciente__usuario__username', 'paciente__usuario__first_name']
    readonly_fields = ['data_preenchimento']
    ordering = ['-data_preenchimento']

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'data_hora', 'tipo_consulta', 'status', 'data_agendamento']
    list_filter = ['status', 'tipo_consulta', 'data_hora', 'data_agendamento']
    search_fields = ['paciente__usuario__username', 'paciente__usuario__first_name', 'tipo_consulta']
    readonly_fields = ['data_agendamento', 'data_atualizacao']
    ordering = ['-data_hora']
    date_hierarchy = 'data_hora'

@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'titulo', 'tipo', 'data_lembrete', 'lido', 'data_criacao']
    list_filter = ['tipo', 'lido', 'data_lembrete', 'data_criacao']
    search_fields = ['usuario__usuario__username', 'titulo', 'descricao']
    readonly_fields = ['data_criacao']
    ordering = ['-data_criacao']
    list_editable = ['lido']

@admin.register(MensagemSuporte)
class MensagemSuporteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'assunto', 'status', 'estudante', 'data_envio']
    list_filter = ['status', 'data_envio', 'data_resposta']
    search_fields = ['usuario__usuario__username', 'assunto', 'mensagem']
    readonly_fields = ['data_envio']
    ordering = ['-data_envio']
    list_editable = ['status']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ativo', 'data_criacao', 'perguntas_count']
    list_filter = ['ativo', 'data_criacao']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['data_criacao']
    ordering = ['-data_criacao']
    list_editable = ['ativo']
    
    def perguntas_count(self, obj):
        return obj.perguntas.count()
    perguntas_count.short_description = 'Perguntas'

@admin.register(PerguntaQuiz)
class PerguntaQuizAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'pergunta_short', 'ordem', 'alternativas_count']
    list_filter = ['quiz', 'ordem']
    search_fields = ['quiz__titulo', 'pergunta']
    ordering = ['quiz', 'ordem']
    
    def pergunta_short(self, obj):
        return obj.pergunta[:50] + '...' if len(obj.pergunta) > 50 else obj.pergunta
    pergunta_short.short_description = 'Pergunta'
    
    def alternativas_count(self, obj):
        return obj.alternativas.count()
    alternativas_count.short_description = 'Alternativas'

@admin.register(AlternativaQuiz)
class AlternativaQuizAdmin(admin.ModelAdmin):
    list_display = ['pergunta_short', 'texto_short', 'correta']
    list_filter = ['correta', 'pergunta__quiz']
    search_fields = ['pergunta__pergunta', 'texto']
    ordering = ['pergunta__quiz', 'pergunta__ordem']
    list_editable = ['correta']
    
    def pergunta_short(self, obj):
        return obj.pergunta.pergunta[:30] + '...' if len(obj.pergunta.pergunta) > 30 else obj.pergunta.pergunta
    pergunta_short.short_description = 'Pergunta'
    
    def texto_short(self, obj):
        return obj.texto[:30] + '...' if len(obj.texto) > 30 else obj.texto
    texto_short.short_description = 'Alternativa'

@admin.register(ResultadoQuiz)
class ResultadoQuizAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'quiz', 'pontuacao', 'total_perguntas', 'percentual', 'data_realizacao']
    list_filter = ['quiz', 'data_realizacao']
    search_fields = ['usuario__usuario__username', 'quiz__titulo']
    readonly_fields = ['data_realizacao']
    ordering = ['-data_realizacao']
    
    def percentual(self, obj):
        if obj.total_perguntas > 0:
            return f"{(obj.pontuacao / obj.total_perguntas * 100):.1f}%"
        return "0%"
    percentual.short_description = 'Percentual'

@admin.register(ConteudoEducativo)
class ConteudoEducativoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'ativo', 'data_criacao']
    list_filter = ['categoria', 'ativo', 'data_criacao']
    search_fields = ['titulo', 'conteudo']
    readonly_fields = ['data_criacao']
    ordering = ['-data_criacao']
    list_editable = ['ativo']

# Configurações do Admin
admin.site.site_header = "EDUCA SORRISO - Administração"
admin.site.site_title = "EDUCA SORRISO Admin"
admin.site.index_title = "Bem-vindo ao Painel de Administração do EDUCA SORRISO"
