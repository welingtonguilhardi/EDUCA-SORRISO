from django.urls import path
from . import views

app_name = 'educa_sorriso'

urlpatterns = [
    # Páginas principais
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('completar-perfil/', views.completar_perfil, name='completar_perfil'),
    
    # Anamnese
    path('anamnese/', views.anamnese_list, name='anamnese_list'),
    path('anamnese/nova/', views.anamnese_create, name='anamnese_create'),
    path('anamnese/<int:pk>/', views.anamnese_detail, name='anamnese_detail'),
    
    # Consultas
    path('consultas/', views.consulta_list, name='consulta_list'),
    path('consultas/nova/', views.consulta_create, name='consulta_create'),
    path('consultas/<int:pk>/editar/', views.consulta_update, name='consulta_update'),
    path('consultas/<int:pk>/cancelar/', views.consulta_delete, name='consulta_delete'),
    
    # Lembretes
    path('lembretes/', views.lembrete_list, name='lembrete_list'),
    path('lembretes/novo/', views.lembrete_create, name='lembrete_create'),
    path('lembretes/<int:pk>/marcar-lido/', views.lembrete_marcar_lido, name='lembrete_marcar_lido'),
    
    # Suporte
    path('suporte/', views.suporte_list, name='suporte_list'),
    path('suporte/nova/', views.suporte_create, name='suporte_create'),
    path('suporte/<int:pk>/', views.suporte_detail, name='suporte_detail'),
    
    # Quiz
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/submit/', views.quiz_submit, name='quiz_submit'),
    path('quiz/resultados/', views.quiz_resultados, name='quiz_resultados'),
    
    # Conteúdo Educativo
    path('conteudo/', views.conteudo_list, name='conteudo_list'),
    path('conteudo/<int:pk>/', views.conteudo_detail, name='conteudo_detail'),
    
    # Área do Estudante
    path('estudante/dashboard/', views.estudante_dashboard, name='estudante_dashboard'),
    path('estudante/mensagens/', views.estudante_mensagens, name='estudante_mensagens'),
    path('estudante/mensagens/<int:pk>/responder/', views.estudante_responder, name='estudante_responder'),
    path('estudante/consultas/', views.estudante_consultas, name='estudante_consultas'),
    path('estudante/consultas/<int:pk>/', views.estudante_consulta_detail, name='estudante_consulta_detail'),
    path('estudante/pacientes/', views.estudante_pacientes, name='estudante_pacientes'),
    path('estudante/pacientes/<int:pk>/', views.estudante_paciente_detail, name='estudante_paciente_detail'),
    
    # Área do Profissional
    path('profissional/dashboard/', views.profissional_dashboard, name='profissional_dashboard'),
    path('profissional/consultas/', views.profissional_consultas, name='profissional_consultas'),
    path('profissional/consultas/<int:pk>/', views.profissional_consulta_detail, name='profissional_consulta_detail'),
    path('profissional/pacientes/', views.profissional_pacientes, name='profissional_pacientes'),
    path('profissional/pacientes/<int:pk>/', views.profissional_paciente_detail, name='profissional_paciente_detail'),
    path('profissional/anamnese/<int:pk>/', views.profissional_anamnese_detail, name='profissional_anamnese_detail'),
    
    # API
    path('api/voz/', views.api_voz, name='api_voz'),
]
