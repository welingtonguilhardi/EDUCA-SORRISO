# EDUCA SORRISO - Saúde Bucal na Palma da Mão

## 📋 Descrição do Projeto

O **EDUCA SORRISO** é uma plataforma inovadora que promove a prevenção e acompanhamento em saúde bucal para famílias de baixa renda, com foco especial em crianças e responsáveis. O projeto integra tecnologia, educação e saúde para democratizar o acesso à informação e cuidados odontológicos.

## 🎯 Objetivos

### Objetivo Geral
Promover a prevenção e o acompanhamento em saúde bucal para famílias de baixa renda, utilizando um aplicativo integrado que facilite o acesso à informação, consultas e atividades educativas.

### Objetivos Específicos
- ✅ Facilitar o cadastro e acompanhamento odontológico dos usuários
- ✅ Oferecer orientações preventivas e educativas sobre saúde bucal
- ✅ Apoiar pessoas analfabetas ou com deficiência por meio de interface com comando de voz
- ✅ Criar interação lúdica para crianças com quiz e jogos educativos
- ✅ Integrar agendamentos com o sistema das Unidades de Saúde
- ✅ Estimular a participação familiar nos cuidados odontológicos

## 🚀 Funcionalidades Implementadas

### 👤 Gestão de Usuários
- **Cadastro completo** com CPF e CadÚnico
- **Perfis diferenciados**: Paciente, Responsável, Estudante de Odontologia, Profissional de Saúde
- **Sistema de autenticação** seguro
- **Completar perfil** com dados pessoais e endereço

### 📋 Anamnese Digital
- **Ficha de anamnese completa** com dados de saúde bucal e geral
- **Suporte a comandos de voz** para acessibilidade
- **Histórico de anamneses** do usuário
- **Dados organizados** por categorias (geral, odontológico, familiar)

### 📅 Agendamento de Consultas
- **Sistema de agendamento** completo
- **Tipos de consulta** pré-definidos
- **Edição e cancelamento** de consultas
- **Status de acompanhamento** (agendada, confirmada, realizada, cancelada, faltou)

### 🔔 Lembretes e Alertas
- **Sistema de notificações** sobre higiene bucal
- **Lembretes de consultas** e revisões odontológicas
- **Alertas para acompanhamento** de tratamentos
- **Marcação de lembretes** como lidos

### 💬 Suporte Interativo
- **Canal de mensagens** para dúvidas sobre saúde bucal
- **Respostas por estudantes** de Odontologia supervisionados
- **Sistema de status** das mensagens (aberta, em andamento, respondida, fechada)
- **Área específica** para estudantes responderem

### 🎮 Quiz Educativo
- **Sistema de quizzes** interativos sobre saúde bucal
- **Perguntas e alternativas** configuráveis
- **Cálculo automático** de pontuação
- **Histórico de resultados** dos usuários
- **Interface lúdica** para crianças

### 📚 Conteúdo Educativo
- **Materiais educativos** sobre saúde bucal
- **Categorização** por temas (higiene, alimentação, prevenção, etc.)
- **Sistema de busca** e filtros
- **Conteúdo ativo/inativo** para controle

### 🎤 Comandos de Voz
- **API para reconhecimento** de comandos de voz
- **Comandos básicos** implementados (agendar consulta, lembretes, quiz)
- **Suporte a acessibilidade** para analfabetos e pessoas com deficiência

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.5** - Framework web Python
- **SQLite** - Banco de dados (desenvolvimento)
- **Pillow** - Processamento de imagens

### Frontend
- **Bootstrap 5.3.0** - Framework CSS
- **Bootstrap Icons** - Ícones
- **Google Fonts (Poppins)** - Tipografia
- **JavaScript** - Interatividade e comandos de voz

### Funcionalidades Especiais
- **Web Speech API** - Reconhecimento de voz
- **AJAX** - Requisições assíncronas
- **Responsive Design** - Design responsivo

## 📁 Estrutura do Projeto

```
EDUCA SORRISO/
├── app/                          # Configurações do Django
│   ├── settings.py              # Configurações do projeto
│   ├── urls.py                  # URLs principais
│   └── ...
├── educa_sorriso/               # Aplicação principal
│   ├── models.py                # Modelos de dados
│   ├── views.py                 # Lógica de negócio
│   ├── forms.py                 # Formulários
│   ├── admin.py                 # Interface administrativa
│   └── urls.py                  # URLs da aplicação
├── templates/                   # Templates HTML
│   └── educa_sorriso/
│       ├── base.html            # Template base
│       ├── home.html            # Página inicial
│       ├── dashboard.html       # Dashboard do usuário
│       ├── cadastro.html        # Formulário de cadastro
│       ├── login.html           # Página de login
│       └── ...
├── static/                      # Arquivos estáticos
├── manage.py                    # Script de gerenciamento Django
├── requirements.txt             # Dependências Python
└── README.md                    # Documentação
```

## 🗄️ Modelos de Dados

### PerfilUsuario
- Dados pessoais (CPF, CadÚnico, tipo de usuário)
- Informações de contato e endereço
- Relacionamento com usuário Django

### Anamnese
- Dados gerais de saúde
- Informações odontológicas
- Histórico familiar

### Consulta
- Agendamento de consultas
- Status e observações
- Relacionamento com paciente

### Lembrete
- Sistema de notificações
- Tipos de lembrete
- Controle de leitura

### MensagemSuporte
- Canal de comunicação
- Sistema de status
- Relacionamento com estudantes

### Quiz e Componentes
- Quiz, PerguntaQuiz, AlternativaQuiz
- Sistema de pontuação
- ResultadoQuiz

### ConteudoEducativo
- Materiais educativos
- Categorização
- Controle de ativação

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd EDUCA-SORRISO
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

8. **Acesse o projeto**
- **Site principal**: http://127.0.0.1:8000/
- **Admin Django**: http://127.0.0.1:8000/admin/

## 👥 Usuários de Teste

### Superusuário (Admin)
- **Usuário**: admin
- **Senha**: (definida durante a criação)

### Tipos de Usuário Disponíveis
1. **Paciente** - Usuário comum que agenda consultas
2. **Responsável** - Responsável por crianças
3. **Estudante de Odontologia** - Pode responder mensagens de suporte
4. **Profissional de Saúde** - Acesso ampliado

## 🎨 Interface e Design

### Características do Design
- **Design responsivo** para todos os dispositivos
- **Paleta de cores** profissional e acessível
- **Ícones intuitivos** do Bootstrap Icons
- **Tipografia moderna** (Poppins)
- **Animações suaves** e transições
- **Cards interativos** com hover effects

### Cores Principais
- **Primária**: #2E86AB (Azul)
- **Secundária**: #A23B72 (Rosa)
- **Acento**: #F18F01 (Laranja)
- **Sucesso**: #C73E1D (Vermelho)

## 🔧 Funcionalidades Técnicas

### Sistema de Autenticação
- Login/logout integrado ao Django
- Redirecionamento automático
- Proteção de rotas com @login_required

### Validação de Formulários
- Validação client-side e server-side
- Máscaras para CPF, CEP, telefone
- Mensagens de erro personalizadas

### API de Comandos de Voz
- Endpoint `/api/voz/`
- Reconhecimento de comandos básicos
- Respostas em JSON

### Sistema de Paginação
- Paginação automática para listas
- Navegação intuitiva
- Performance otimizada

## 📊 Funcionalidades Administrativas

### Painel Admin Django
- Interface completa para gerenciamento
- Filtros e buscas avançadas
- Edição em lote
- Relatórios básicos

### Controles Disponíveis
- Gerenciamento de usuários e perfis
- Criação e edição de quizzes
- Controle de conteúdo educativo
- Monitoramento de consultas e mensagens

## 🔮 Próximas Implementações

### Funcionalidades Planejadas
- [ ] Integração com SUS (simulação)
- [ ] Integração com UBS (simulação)
- [ ] Sistema de notificações push
- [ ] Relatórios avançados
- [ ] Dashboard para profissionais
- [ ] Sistema de gamificação
- [ ] Chat em tempo real
- [ ] Upload de imagens
- [ ] Exportação de dados

### Melhorias Técnicas
- [ ] Testes automatizados
- [ ] Deploy em produção
- [ ] Banco de dados PostgreSQL
- [ ] Cache Redis
- [ ] API REST completa
- [ ] Documentação da API

## 🤝 Parceiros do Projeto

- **Prefeitura Municipal de Santo Antônio de Jesus**
- **Faculdade de Odontologia**
- **Unidades Básicas de Saúde (UBS)**

## 📞 Contato

- **Localização**: Santo Antônio de Jesus - BA
- **Email**: contato@educasorriso.com.br
- **Projeto**: EDUCA SORRISO - Saúde Bucal na Palma da Mão

## 📄 Licença

Este projeto foi desenvolvido como MVP para o projeto de inovação EDUCA SORRISO. Todos os direitos reservados.

---

**Desenvolvido com ❤️ para promover a saúde bucal na comunidade**
