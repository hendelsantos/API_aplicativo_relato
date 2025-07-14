# Sistema de Relatório de Manutenção 🔧

**API Django REST + Flutter App** para sistema de relatórios de manutenção industrial.

Desenvolvido para **substituir relatórios via WhatsApp** por um sistema robusto e rastreável para equipes de manutenção industrial.

## 🎯 Problema Resolvido

- ❌ **Antes:** Equipe de 3 turnos relatava peças e atividades via WhatsApp
- ❌ **Problemas:** Esquecimentos, furos de estoque, falta de padronização
- ✅ **Agora:** Sistema digital com QR codes, rastreabilidade e controle total

## 🚀 Funcionalidades

### 🔐 **Autenticação & Segurança**
- Sistema de login com JWT
- Controle de usuários por turno
- Permissões granulares

### 📦 **Gestão de Peças**
- Cadastro de peças com QR codes automáticos
- Controle de estoque em tempo real
- Categorização organizada
- Scanner QR integrado no app

### 📍 **Estrutura de Locais**
- Hierarquia em árvore (Setor → Máquina → Componente)
- Navegação intuitiva
- Localização precisa de atividades

### 📋 **Atividades de Manutenção**
- Formulários padronizados
- Upload de fotos (antes/durante/depois)
- Histórico completo de manutenções
- Relatórios automatizados

### 📱 **App Mobile**
- Interface moderna Material Design 3
- Scanner QR nativo
- Funcionamento offline
- Sincronização automática

## 🛠️ Tecnologias

### **Backend (Django)**
- **Django 5.2** + REST Framework
- **JWT Authentication** (SimpleJWT)
- **SQLite** (desenvolvimento) / **PostgreSQL** (produção)
- **CORS** para integração mobile
- **QR Code** generation

### **Frontend (Flutter)**
- **Flutter 3.32.5** (cross-platform)
- **Provider** para gerenciamento de estado
- **Dio** para requisições HTTP
- **Mobile Scanner** para QR codes
- **Material Design 3**

## 🚀 Instalação e Execução

### **Pré-requisitos**
```bash
- Python 3.12+
- Flutter 3.32.5+
- Android Studio (para desenvolvimento Android)
```

### **1. Configurar Backend Django**

```bash
# Clone o repositório
git clone https://github.com/[seu-usuario]/API_aplicativo_relato.git
cd API_aplicativo_relato

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar o arquivo .env com suas configurações

# Executar migrações
python manage.py migrate

# Criar dados de exemplo
python create_sample_data.py

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

### **2. Configurar App Flutter**

```bash
# Entrar no diretório Flutter
cd flutter_app

# Instalar dependências
flutter pub get

# Verificar dispositivos
flutter devices

# Executar no dispositivo/emulador
flutter run
```

### **3. Credenciais de Teste**
```
Usuário: joao.silva
Senha: senha123
```

## 📁 Estrutura do Projeto

```
API_aplicativo_relato/
├── 🐍 Backend Django
│   ├── authentication/     # Gestão de usuários
│   ├── parts/             # Peças e QR codes
│   ├── locations/         # Estrutura de locais
│   ├── activities/        # Atividades de manutenção
│   └── maintenance_api/   # Configurações principais
├── 📱 Flutter App
│   ├── lib/
│   │   ├── screens/       # Telas do app
│   │   ├── providers/     # Gerenciamento de estado
│   │   ├── services/      # API services
│   │   └── models/        # Modelos de dados
│   └── android/           # Configurações Android
└── 📋 Documentação
    ├── README.md
    └── requirements.txt
```

## 🔧 Configuração de Rede

Para usar o app em dispositivos físicos:

1. **Descobrir IP da máquina:**
```bash
ip addr show  # Linux
ipconfig      # Windows
```

2. **Atualizar configuração do Flutter:**
```dart
// lib/services/api_service.dart
static const String baseUrl = 'http://SEU_IP:8000/api';
```

3. **Configurar Django:**
```python
# settings.py
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'SEU_IP', '*']
```

## 📊 Endpoints da API

```
POST   /api/auth/login/           # Login
POST   /api/auth/refresh/         # Refresh token
GET    /api/parts/                # Listar peças
POST   /api/parts/                # Criar peça
GET    /api/locations/            # Listar locais
POST   /api/activities/           # Criar atividade
GET    /api/activities/           # Listar atividades
```

## 🐳 Docker (Deployment Simplificado)

### **Desenvolvimento Rápido**
```bash
# Executar com Docker Compose
docker-compose up -d

# Acessar aplicação
http://localhost:8000
```

### **Produção Completa**
```bash
# Com PostgreSQL + Redis + Nginx
docker-compose --profile production up -d

# Verificar status
docker-compose ps
```

### **Scripts Automatizados**
```bash
# Script interativo de instalação
./deploy.sh

# Gerenciamento Docker
./docker-manager.sh
```

## 📋 Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `./deploy.sh` | Setup completo interativo |
| `./docker-manager.sh` | Gerenciar containers Docker |
| `./start.sh` | Inicialização para produção |

## 🎯 Próximas Implementações

- [ ] Relatórios automáticos por email
- [ ] Dashboard web para supervisores
- [ ] Notificações push
- [ ] Integração com sistemas ERP
- [ ] Backup automático
- [ ] Logs de auditoria

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte, abra uma issue no GitHub.

---

**Desenvolvido para modernizar a manutenção industrial** 🏭✨

### 🏗️ Backend Django (100% Funcional)
- ✅ API REST completa com Django REST Framework
- ✅ Autenticação JWT com refresh tokens
- ✅ 4 apps Django: authentication, parts, locations, activities
- ✅ Banco SQLite com dados de teste
- ✅ QR codes automáticos para peças
- ✅ Estrutura hierárquica de locais
- ✅ Servidor rodando em http://localhost:8000

### 📱 Frontend Flutter (100% Funcional)
- ✅ App cross-platform (Android, iOS, Windows, Linux)
- ✅ 5 telas implementadas: Login, Dashboard, Atividades, Peças, Perfil
- ✅ Scanner QR Code integrado
- ✅ Gerenciamento de estado com Provider
- ✅ Cliente HTTP Dio com interceptors JWT
- ✅ Interface Material Design moderna

## 🚀 Como Executar

### Backend Django
```bash
cd /home/hendel/Documentos/API_aplicativo_relato
python manage.py runserver
```

### Frontend Flutter
```bash
cd /home/hendel/Documentos/API_aplicativo_relato/flutter_app
flutter run
```

## 👥 Usuários de Teste

| Usuário | Senha | Função | Turno |
|---------|-------|--------|-------|
| `admin` | `admin123` | Administrador | - |
| `joao.silva` | `senha123` | Técnico | Manhã (6h-14h) |
| `maria.santos` | `senha123` | Supervisora | Tarde (14h-22h) |

## Funcionalidades

### 🔧 Gestão de Peças
- Cadastro de peças com categorias
- QR codes automáticos para cada peça
- Controle de estoque com alertas de reposição
- Leitura de QR code pelo app

### 📍 Estrutura de Locais
- Hierarquia em árvore (Fábrica > Setor > Equipamento > Componente)
- Navegação intuitiva para seleção de local
- Busca e filtros avançados

### 👥 Gestão de Técnicos
- 3 turnos de trabalho (Manhã, Tarde, Noite)
- Níveis de acesso (Técnico/Supervisor)
- Autenticação JWT

### 📋 Atividades de Manutenção
- Tipos de atividade com perguntas padronizadas
- Formulários dinâmicos (Sim/Não, Texto, Número)
- Upload de fotos (antes/durante/depois)
- Controle de status (Pendente/Em Andamento/Concluída)
- Registro automático de peças utilizadas

## Tecnologias

- **Backend:** Django 5.2 + Django REST Framework
- **Banco:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação:** JWT (Simple JWT)
- **Upload:** Pillow para imagens
- **QR Codes:** python-qrcode

## Estrutura da API

```
/api/auth/
├── login/          # JWT login
├── refresh/        # Refresh token
├── profile/        # Perfil do usuário
├── users/          # Lista técnicos
└── stats/          # Estatísticas do usuário

/api/parts/
├── /               # CRUD peças
├── categories/     # Categorias
├── scan-qr/        # Leitura QR code
├── low-stock/      # Peças em falta
└── search/         # Busca avançada

/api/locations/
├── /               # CRUD locais
├── tree/           # Árvore completa
├── {id}/children/  # Filhos de um local
└── search/         # Busca avançada

/api/activities/
├── /               # CRUD atividades
├── types/          # Tipos de atividade
├── {id}/start/     # Iniciar atividade
├── {id}/complete/  # Finalizar atividade
├── {id}/upload-photo/ # Upload foto
└── my-activities/  # Minhas atividades
```

## Instalação

1. **Clone e configure ambiente:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure o banco:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

3. **Execute o servidor:**
```bash
python manage.py runserver
```

4. **Acesse:**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## Configuração

Edite o arquivo `.env`:
```env
SECRET_KEY=sua_chave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.0/24
```

## Próximos Passos

1. **Aplicativo Flutter** (cliente móvel)
2. **Relatórios e dashboards** 
3. **Notificações push**
4. **Integração com sistemas ERP**
5. **Backup automático**

## Fluxo de Trabalho

1. **Técnico faz login** no app móvel
2. **Seleciona local** na estrutura hierárquica
3. **Escaneia QR code** da peça (opcional)
4. **Preenche formulário** padronizado da atividade
5. **Tira fotos** da situação/problema
6. **Registra peças utilizadas** (atualiza estoque)
7. **Finaliza atividade** com observações

## Benefícios

✅ **Controle rigoroso** de estoque  
✅ **Histórico completo** das atividades  
✅ **Padronização** dos relatórios  
✅ **Redução de falhas** humanas  
✅ **Relatórios automáticos** por email  
✅ **Rastreabilidade** completa  
✅ **Interface intuitiva** para técnicos  

---

**Desenvolvido para resolver o problema de relatórios falhos via WhatsApp, criando um sistema profissional e confiável para equipes de manutenção.**
