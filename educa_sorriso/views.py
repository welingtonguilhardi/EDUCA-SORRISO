from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from .forms import *
import json
from datetime import datetime, timedelta

def home(request):
    """Página inicial do sistema"""
    return render(request, 'educa_sorriso/home.html')

def cadastro(request):
    """Cadastro de novos usuários"""
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)
        
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.usuario = user
            perfil.save()
            
            # Login automático após cadastro
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('educa_sorriso:dashboard')
    else:
        user_form = UserCreationForm()
        perfil_form = PerfilUsuarioForm()
    
    return render(request, 'educa_sorriso/cadastro.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

@login_required
def dashboard(request):
    """Dashboard principal do usuário"""
    try:
        perfil = request.user.perfilusuario
    except:
        return redirect('educa_sorriso:completar_perfil')
    
    # Dados para o dashboard
    consultas_proximas = Consulta.objects.filter(
        paciente=perfil,
        data_hora__gte=timezone.now(),
        status__in=['agendada', 'confirmada']
    ).order_by('data_hora')[:5]
    
    lembretes_nao_lidos = Lembrete.objects.filter(
        usuario=perfil,
        lido=False
    ).order_by('-data_criacao')[:5]
    
    mensagens_nao_respondidas = MensagemSuporte.objects.filter(
        usuario=perfil,
        status__in=['aberta', 'em_andamento']
    ).order_by('-data_envio')[:3]
    
    context = {
        'perfil': perfil,
        'consultas_proximas': consultas_proximas,
        'lembretes_nao_lidos': lembretes_nao_lidos,
        'mensagens_nao_respondidas': mensagens_nao_respondidas,
    }
    
    return render(request, 'educa_sorriso/dashboard.html', context)

@login_required
def completar_perfil(request):
    """Completar perfil do usuário"""
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            messages.success(request, 'Perfil completado com sucesso!')
            return redirect('educa_sorriso:dashboard')
    else:
        form = PerfilUsuarioForm()
    
    return render(request, 'educa_sorriso/completar_perfil.html', {'form': form})

@login_required
def anamnese_list(request):
    """Lista de anamneses do usuário"""
    perfil = request.user.perfilusuario
    anamneses = Anamnese.objects.filter(paciente=perfil).order_by('-data_preenchimento')
    
    paginator = Paginator(anamneses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/anamnese_list.html', {
        'page_obj': page_obj
    })

@login_required
def anamnese_create(request):
    """Criar nova anamnese"""
    if request.method == 'POST':
        form = AnamneseForm(request.POST)
        if form.is_valid():
            anamnese = form.save(commit=False)
            anamnese.paciente = request.user.perfilusuario
            anamnese.save()
            messages.success(request, 'Anamnese criada com sucesso!')
            return redirect('educa_sorriso:anamnese_list')
    else:
        form = AnamneseForm()
    
    return render(request, 'educa_sorriso/anamnese_form.html', {'form': form})

@login_required
def anamnese_detail(request, pk):
    """Detalhes da anamnese"""
    anamnese = get_object_or_404(Anamnese, pk=pk, paciente=request.user.perfilusuario)
    return render(request, 'educa_sorriso/anamnese_detail.html', {'anamnese': anamnese})

@login_required
def consulta_list(request):
    """Lista de consultas do usuário"""
    perfil = request.user.perfilusuario
    consultas = Consulta.objects.filter(paciente=perfil).order_by('-data_hora')
    
    paginator = Paginator(consultas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/consulta_list.html', {
        'page_obj': page_obj
    })

@login_required
def consulta_create(request):
    """Agendar nova consulta"""
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = request.user.perfilusuario
            consulta.save()
            messages.success(request, 'Consulta agendada com sucesso!')
            return redirect('educa_sorriso:consulta_list')
    else:
        form = ConsultaForm()
    
    return render(request, 'educa_sorriso/consulta_form.html', {'form': form})

@login_required
def consulta_update(request, pk):
    """Atualizar consulta"""
    consulta = get_object_or_404(Consulta, pk=pk, paciente=request.user.perfilusuario)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta atualizada com sucesso!')
            return redirect('educa_sorriso:consulta_list')
    else:
        form = ConsultaForm(instance=consulta)
    
    return render(request, 'educa_sorriso/consulta_form.html', {'form': form})

@login_required
def consulta_delete(request, pk):
    """Cancelar consulta"""
    consulta = get_object_or_404(Consulta, pk=pk, paciente=request.user.perfilusuario)
    
    if request.method == 'POST':
        consulta.status = 'cancelada'
        consulta.save()
        messages.success(request, 'Consulta cancelada com sucesso!')
        return redirect('educa_sorriso:consulta_list')
    
    return render(request, 'educa_sorriso/consulta_confirm_delete.html', {'consulta': consulta})

@login_required
def lembrete_list(request):
    """Lista de lembretes do usuário"""
    perfil = request.user.perfilusuario
    lembretes = Lembrete.objects.filter(usuario=perfil).order_by('-data_criacao')
    
    paginator = Paginator(lembretes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/lembrete_list.html', {
        'page_obj': page_obj
    })

@login_required
def lembrete_marcar_lido(request, pk):
    """Marcar lembrete como lido"""
    lembrete = get_object_or_404(Lembrete, pk=pk, usuario=request.user.perfilusuario)
    lembrete.lido = True
    lembrete.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    messages.success(request, 'Lembrete marcado como lido!')
    return redirect('educa_sorriso:lembrete_list')

@login_required
def lembrete_create(request):
    """Criar novo lembrete"""
    if request.method == 'POST':
        form = LembreteForm(request.POST)
        if form.is_valid():
            lembrete = form.save(commit=False)
            lembrete.usuario = request.user.perfilusuario
            lembrete.save()
            messages.success(request, 'Lembrete criado com sucesso!')
            return redirect('educa_sorriso:lembrete_list')
    else:
        form = LembreteForm()
    
    return render(request, 'educa_sorriso/lembrete_form.html', {'form': form})

@login_required
def suporte_list(request):
    """Lista de mensagens de suporte"""
    perfil = request.user.perfilusuario
    mensagens = MensagemSuporte.objects.filter(usuario=perfil).order_by('-data_envio')
    
    paginator = Paginator(mensagens, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/suporte_list.html', {
        'page_obj': page_obj
    })

@login_required
def suporte_create(request):
    """Criar nova mensagem de suporte"""
    if request.method == 'POST':
        form = MensagemSuporteForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.usuario = request.user.perfilusuario
            mensagem.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('educa_sorriso:suporte_list')
    else:
        form = MensagemSuporteForm()
    
    return render(request, 'educa_sorriso/suporte_form.html', {'form': form})

@login_required
def suporte_detail(request, pk):
    """Detalhes da mensagem de suporte"""
    mensagem = get_object_or_404(MensagemSuporte, pk=pk, usuario=request.user.perfilusuario)
    return render(request, 'educa_sorriso/suporte_detail.html', {'mensagem': mensagem})

@login_required
def quiz_list(request):
    """Lista de quizzes disponíveis"""
    quizzes = Quiz.objects.filter(ativo=True).order_by('-data_criacao')
    return render(request, 'educa_sorriso/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, pk):
    """Detalhes do quiz"""
    quiz = get_object_or_404(Quiz, pk=pk, ativo=True)
    perguntas = quiz.perguntas.all()
    
    return render(request, 'educa_sorriso/quiz_detail.html', {
        'quiz': quiz,
        'perguntas': perguntas
    })

@csrf_exempt
@login_required
def quiz_submit(request, pk):
    """Submeter respostas do quiz"""
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, pk=pk, ativo=True)
        data = json.loads(request.body)
        respostas = data.get('respostas', {})
        
        # Calcular pontuação
        pontuacao = 0
        total_perguntas = quiz.perguntas.count()
        
        for pergunta_id, alternativa_id in respostas.items():
            try:
                pergunta = PerguntaQuiz.objects.get(id=pergunta_id, quiz=quiz)
                alternativa = AlternativaQuiz.objects.get(id=alternativa_id, pergunta=pergunta)
                if alternativa.correta:
                    pontuacao += 1
            except:
                pass
        
        # Salvar resultado
        resultado = ResultadoQuiz.objects.create(
            usuario=request.user.perfilusuario,
            quiz=quiz,
            pontuacao=pontuacao,
            total_perguntas=total_perguntas
        )
        
        return JsonResponse({
            'success': True,
            'pontuacao': pontuacao,
            'total_perguntas': total_perguntas,
            'percentual': round((pontuacao / total_perguntas) * 100, 1)
        })
    
    return JsonResponse({'success': False})

@login_required
def quiz_resultados(request):
    """Histórico de resultados dos quizzes"""
    perfil = request.user.perfilusuario
    resultados = ResultadoQuiz.objects.filter(usuario=perfil).order_by('-data_realizacao')
    
    paginator = Paginator(resultados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/quiz_resultados.html', {
        'page_obj': page_obj
    })

def conteudo_list(request):
    """Lista de conteúdo educativo"""
    categoria = request.GET.get('categoria', '')
    if categoria:
        conteudos = ConteudoEducativo.objects.filter(ativo=True, categoria=categoria).order_by('-data_criacao')
    else:
        conteudos = ConteudoEducativo.objects.filter(ativo=True).order_by('-data_criacao')
    
    paginator = Paginator(conteudos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/conteudo_list.html', {
        'page_obj': page_obj,
        'categoria_atual': categoria
    })

def conteudo_detail(request, pk):
    """Detalhes do conteúdo educativo"""
    conteudo = get_object_or_404(ConteudoEducativo, pk=pk, ativo=True)
    return render(request, 'educa_sorriso/conteudo_detail.html', {'conteudo': conteudo})

# Views para estudantes de odontologia
@login_required
def estudante_dashboard(request):
    """Dashboard para estudantes de odontologia"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'estudante':
        messages.error(request, 'Acesso negado. Apenas estudantes podem acessar esta área.')
        return redirect('educa_sorriso:dashboard')
    
    mensagens_pendentes = MensagemSuporte.objects.filter(
        status__in=['aberta', 'em_andamento'],
        estudante__isnull=True
    ).order_by('-data_envio')
    
    mensagens_atendidas = MensagemSuporte.objects.filter(
        estudante=perfil
    ).order_by('-data_envio')[:10]
    
    # Consultas agendadas para o estudante
    consultas_agendadas = Consulta.objects.filter(
        status__in=['agendada', 'confirmada'],
        data_hora__gte=timezone.now()
    ).order_by('data_hora')[:10]
    
    return render(request, 'educa_sorriso/estudante_dashboard.html', {
        'mensagens_pendentes': mensagens_pendentes,
        'mensagens_atendidas': mensagens_atendidas,
        'consultas_agendadas': consultas_agendadas
    })

@login_required
def estudante_mensagens(request):
    """Lista de mensagens para estudantes responderem"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'estudante':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    mensagens = MensagemSuporte.objects.filter(
        status__in=['aberta', 'em_andamento'],
        estudante__isnull=True
    ).order_by('-data_envio')
    
    paginator = Paginator(mensagens, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/estudante_mensagens.html', {
        'page_obj': page_obj
    })

@login_required
def estudante_responder(request, pk):
    """Responder mensagem de suporte"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'estudante':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    mensagem = get_object_or_404(MensagemSuporte, pk=pk, status__in=['aberta', 'em_andamento'])
    
    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        if resposta:
            mensagem.resposta = resposta
            mensagem.estudante = perfil
            mensagem.status = 'respondida'
            mensagem.data_resposta = timezone.now()
            mensagem.save()
            messages.success(request, 'Resposta enviada com sucesso!')
            return redirect('educa_sorriso:estudante_mensagens')
    
    return render(request, 'educa_sorriso/estudante_responder.html', {'mensagem': mensagem})

@login_required
def estudante_consultas(request):
    """Lista de consultas para estudantes gerenciarem"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'estudante':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    consultas = Consulta.objects.filter(
        status__in=['agendada', 'confirmada']
    ).order_by('data_hora')
    
    paginator = Paginator(consultas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/estudante_consultas.html', {
        'page_obj': page_obj
    })

@login_required
def estudante_consulta_detail(request, pk):
    """Detalhes da consulta para estudantes"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'estudante':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    consulta = get_object_or_404(Consulta, pk=pk)
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'confirmar':
            consulta.status = 'confirmada'
            consulta.save()
            messages.success(request, 'Consulta confirmada com sucesso!')
        elif acao == 'realizar':
            consulta.status = 'realizada'
            consulta.save()
            messages.success(request, 'Consulta marcada como realizada!')
        elif acao == 'cancelar':
            consulta.status = 'cancelada'
            consulta.save()
            messages.success(request, 'Consulta cancelada!')
        
        return redirect('educa_sorriso:estudante_consultas')
    
    return render(request, 'educa_sorriso/estudante_consulta_detail.html', {
        'consulta': consulta
    })

@login_required
def estudante_pacientes(request):
    """Lista de pacientes para estudantes"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'estudante':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    pacientes = PerfilUsuario.objects.filter(
        tipo_usuario__in=['paciente', 'responsavel']
    ).order_by('usuario__first_name')
    
    paginator = Paginator(pacientes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/estudante_pacientes.html', {
        'page_obj': page_obj
    })

@login_required
def estudante_paciente_detail(request, pk):
    """Detalhes do paciente para estudantes"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'estudante':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    paciente = get_object_or_404(PerfilUsuario, pk=pk, tipo_usuario__in=['paciente', 'responsavel'])
    anamneses = paciente.anamneses.all().order_by('-data_preenchimento')
    consultas = paciente.consultas.all().order_by('-data_hora')
    
    return render(request, 'educa_sorriso/estudante_paciente_detail.html', {
        'paciente': paciente,
        'anamneses': anamneses,
        'consultas': consultas
    })

# Views para profissionais de saúde
@login_required
def profissional_dashboard(request):
    """Dashboard para profissionais de saúde"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'profissional':
        messages.error(request, 'Acesso negado. Apenas profissionais podem acessar esta área.')
        return redirect('educa_sorriso:dashboard')
    
    # Consultas agendadas para hoje
    hoje = timezone.now().date()
    consultas_hoje = Consulta.objects.filter(
        data_hora__date=hoje,
        status__in=['agendada', 'confirmada']
    ).order_by('data_hora')
    
    # Consultas da semana
    fim_semana = hoje + timedelta(days=7)
    consultas_semana = Consulta.objects.filter(
        data_hora__date__range=[hoje, fim_semana],
        status__in=['agendada', 'confirmada']
    ).order_by('data_hora')
    
    # Pacientes recentes
    pacientes_recentes = PerfilUsuario.objects.filter(
        tipo_usuario__in=['paciente', 'responsavel'],
        data_cadastro__gte=timezone.now() - timedelta(days=30)
    ).order_by('-data_cadastro')[:10]
    
    return render(request, 'educa_sorriso/profissional_dashboard.html', {
        'consultas_hoje': consultas_hoje,
        'consultas_semana': consultas_semana,
        'pacientes_recentes': pacientes_recentes
    })

@login_required
def profissional_consultas(request):
    """Lista de consultas para profissionais gerenciarem"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'profissional':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    consultas = Consulta.objects.all().order_by('-data_hora')
    
    # Filtros
    status_filter = request.GET.get('status', '')
    if status_filter:
        consultas = consultas.filter(status=status_filter)
    
    paginator = Paginator(consultas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/profissional_consultas.html', {
        'page_obj': page_obj,
        'status_filter': status_filter
    })

@login_required
def profissional_consulta_detail(request, pk):
    """Detalhes da consulta para profissionais"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'profissional':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    consulta = get_object_or_404(Consulta, pk=pk)
    
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'confirmar':
            consulta.status = 'confirmada'
            consulta.save()
            messages.success(request, 'Consulta confirmada com sucesso!')
        elif acao == 'realizar':
            consulta.status = 'realizada'
            consulta.save()
            messages.success(request, 'Consulta marcada como realizada!')
        elif acao == 'cancelar':
            consulta.status = 'cancelada'
            consulta.save()
            messages.success(request, 'Consulta cancelada!')
        elif acao == 'faltou':
            consulta.status = 'faltou'
            consulta.save()
            messages.success(request, 'Paciente marcado como ausente!')
        
        return redirect('educa_sorriso:profissional_consultas')
    
    return render(request, 'educa_sorriso/profissional_consulta_detail.html', {
        'consulta': consulta
    })

@login_required
def profissional_pacientes(request):
    """Lista de pacientes para profissionais"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'profissional':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    pacientes = PerfilUsuario.objects.filter(
        tipo_usuario__in=['paciente', 'responsavel']
    ).order_by('usuario__first_name')
    
    # Filtro de busca
    busca = request.GET.get('q', '')
    if busca:
        pacientes = pacientes.filter(
            Q(usuario__first_name__icontains=busca) |
            Q(usuario__last_name__icontains=busca) |
            Q(cpf__icontains=busca) |
            Q(usuario__username__icontains=busca)
        )
    
    paginator = Paginator(pacientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'educa_sorriso/profissional_pacientes.html', {
        'page_obj': page_obj,
        'busca': busca
    })

@login_required
def profissional_paciente_detail(request, pk):
    """Detalhes do paciente para profissionais"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'profissional':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    paciente = get_object_or_404(PerfilUsuario, pk=pk, tipo_usuario__in=['paciente', 'responsavel'])
    anamneses = paciente.anamneses.all().order_by('-data_preenchimento')
    consultas = paciente.consultas.all().order_by('-data_hora')
    lembretes = paciente.lembretes.all().order_by('-data_criacao')[:10]
    
    return render(request, 'educa_sorriso/profissional_paciente_detail.html', {
        'paciente': paciente,
        'anamneses': anamneses,
        'consultas': consultas,
        'lembretes': lembretes
    })

@login_required
def profissional_anamnese_detail(request, pk):
    """Detalhes da anamnese para profissionais"""
    perfil = request.user.perfilusuario
    
    if perfil.tipo_usuario != 'profissional':
        messages.error(request, 'Acesso negado.')
        return redirect('educa_sorriso:dashboard')
    
    anamnese = get_object_or_404(Anamnese, pk=pk)
    
    return render(request, 'educa_sorriso/profissional_anamnese_detail.html', {
        'anamnese': anamnese
    })

# API para comandos de voz (simulação)
@csrf_exempt
def api_voz(request):
    """API para comandos de voz"""
    if request.method == 'POST':
        data = json.loads(request.body)
        comando = data.get('comando', '').lower()
        
        # Simulação de comandos de voz
        if 'agendar consulta' in comando:
            return JsonResponse({
                'acao': 'agendar_consulta',
                'mensagem': 'Vou te ajudar a agendar uma consulta. Acesse a seção de agendamento.'
            })
        elif 'lembrete' in comando:
            return JsonResponse({
                'acao': 'lembretes',
                'mensagem': 'Vou mostrar seus lembretes. Acesse a seção de lembretes.'
            })
        elif 'quiz' in comando:
            return JsonResponse({
                'acao': 'quiz',
                'mensagem': 'Vou te levar para o quiz educativo. Acesse a seção de quiz.'
            })
        else:
            return JsonResponse({
                'acao': 'nao_entendi',
                'mensagem': 'Desculpe, não entendi o comando. Tente novamente.'
            })
    
    return JsonResponse({'error': 'Método não permitido'})
