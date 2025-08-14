from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class PerfilUsuario(models.Model):
    """Perfil do usuário do sistema EDUCA SORRISO"""
    TIPO_USUARIO_CHOICES = [
        ('paciente', 'Paciente'),
        ('responsavel', 'Responsável'),
        ('estudante', 'Estudante de Odontologia'),
        ('profissional', 'Profissional de Saúde'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True, validators=[
        RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF deve estar no formato XXX.XXX.XXX-XX')
    ])
    cad_unico = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número do CadÚnico')
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='paciente')
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100, default='Santo Antônio de Jesus')
    estado = models.CharField(max_length=2, default='BA')
    cep = models.CharField(max_length=9)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cpf}"

class Anamnese(models.Model):
    """Ficha de anamnese digital"""
    paciente = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='anamneses')
    data_preenchimento = models.DateTimeField(auto_now_add=True)
    
    # Dados gerais
    possui_alergias = models.BooleanField(default=False)
    alergias_descricao = models.TextField(blank=True, null=True)
    medicamentos_uso = models.TextField(blank=True, null=True)
    problemas_saude = models.TextField(blank=True, null=True)
    
    # Dados odontológicos
    ultima_consulta = models.DateField(blank=True, null=True)
    frequencia_escovacao = models.CharField(max_length=50, blank=True, null=True)
    usa_fio_dental = models.BooleanField(default=False)
    frequencia_fio_dental = models.CharField(max_length=50, blank=True, null=True)
    problemas_bucais = models.TextField(blank=True, null=True)
    dor_dentes = models.BooleanField(default=False)
    sangramento_gengiva = models.BooleanField(default=False)
    
    # Histórico familiar
    problemas_odontologicos_familia = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Anamnese de {self.paciente.usuario.get_full_name()} - {self.data_preenchimento.strftime('%d/%m/%Y')}"

class Consulta(models.Model):
    """Agendamento de consultas"""
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        ('faltou', 'Faltou'),
    ]
    
    paciente = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='consultas')
    data_hora = models.DateTimeField()
    tipo_consulta = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendada')
    data_agendamento = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Consulta de {self.paciente.usuario.get_full_name()} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class Lembrete(models.Model):
    """Lembretes e alertas para o usuário"""
    TIPO_CHOICES = [
        ('higiene', 'Higiene Bucal'),
        ('consulta', 'Consulta Odontológica'),
        ('prevencao', 'Prevenção'),
        ('tratamento', 'Acompanhamento de Tratamento'),
    ]
    
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='lembretes')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_lembrete = models.DateTimeField()
    lido = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.usuario.get_full_name()}"

class MensagemSuporte(models.Model):
    """Canal de mensagens para suporte com universitários"""
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_andamento', 'Em Andamento'),
        ('respondida', 'Respondida'),
        ('fechada', 'Fechada'),
    ]
    
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    estudante = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='mensagens_atendidas', limit_choices_to={'tipo_usuario': 'estudante'})
    assunto = models.CharField(max_length=200)
    mensagem = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    data_envio = models.DateTimeField(auto_now_add=True)
    data_resposta = models.DateTimeField(blank=True, null=True)
    resposta = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.assunto} - {self.usuario.usuario.get_full_name()}"

class Quiz(models.Model):
    """Quiz educativo para crianças"""
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

class PerguntaQuiz(models.Model):
    """Perguntas do quiz"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='perguntas')
    pergunta = models.TextField()
    ordem = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.quiz.titulo} - {self.pergunta[:50]}..."
    
    class Meta:
        ordering = ['ordem']

class AlternativaQuiz(models.Model):
    """Alternativas das perguntas do quiz"""
    pergunta = models.ForeignKey(PerguntaQuiz, on_delete=models.CASCADE, related_name='alternativas')
    texto = models.CharField(max_length=200)
    correta = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.pergunta.pergunta[:30]}... - {self.texto}"

class ResultadoQuiz(models.Model):
    """Resultados dos quizzes realizados pelas crianças"""
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='resultados_quiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='resultados')
    pontuacao = models.IntegerField()
    total_perguntas = models.IntegerField()
    data_realizacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.usuario.get_full_name()} - {self.quiz.titulo} - {self.pontuacao}/{self.total_perguntas}"

class ConteudoEducativo(models.Model):
    """Conteúdo educativo sobre saúde bucal"""
    CATEGORIA_CHOICES = [
        ('higiene', 'Higiene Bucal'),
        ('alimentacao', 'Alimentação'),
        ('prevencao', 'Prevenção'),
        ('tratamento', 'Tratamento'),
        ('criancas', 'Para Crianças'),
    ]
    
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='conteudo/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.get_categoria_display()}"
