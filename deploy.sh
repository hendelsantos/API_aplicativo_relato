#!/bin/bash

# Script de Deploy para Sistema de Manutenção
# Autor: Hendel Santos
# Versão: 1.0

set -e  # Parar se houver erro

echo "🚀 Deploy do Sistema de Manutenção"
echo "=================================="

# Verificar se está no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

# Função para instalar dependências do backend
install_backend() {
    echo "📦 Instalando dependências do Backend..."
    
    # Verificar se Python está instalado
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 não encontrado. Instale o Python 3.8+"
        exit 1
    fi
    
    # Criar ambiente virtual se não existir
    if [ ! -d "venv" ]; then
        echo "🔧 Criando ambiente virtual..."
        python3 -m venv venv
    fi
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Atualizar pip
    pip install --upgrade pip
    
    # Instalar dependências
    pip install -r requirements.txt
    
    echo "✅ Backend configurado com sucesso!"
}

# Função para configurar ambiente
setup_environment() {
    echo "⚙️ Configurando ambiente..."
    
    # Copiar arquivo de ambiente se não existir
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo "📝 Arquivo .env criado. Configure suas variáveis de ambiente!"
        echo "   Edite o arquivo .env com suas configurações."
    else
        echo "✅ Arquivo .env já existe"
    fi
}

# Função para configurar banco de dados
setup_database() {
    echo "🗄️ Configurando banco de dados..."
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Executar migrações
    python manage.py makemigrations
    python manage.py migrate
    
    # Criar superusuário se não existir
    echo "👤 Verificando superusuário..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Criando superusuário...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superusuário criado: admin/admin123')
else:
    print('✅ Superusuário já existe')
"
    
    echo "✅ Banco de dados configurado!"
}

# Função para criar dados de exemplo
create_sample_data() {
    echo "📊 Criando dados de exemplo..."
    
    source venv/bin/activate
    
    if [ -f "create_sample_data.py" ]; then
        python create_sample_data.py
        echo "✅ Dados de exemplo criados!"
    else
        echo "⚠️ Script de dados de exemplo não encontrado"
    fi
}

# Função para instalar dependências do Flutter
install_flutter() {
    echo "📱 Configurando Flutter App..."
    
    # Verificar se Flutter está instalado
    if ! command -v flutter &> /dev/null; then
        echo "⚠️ Flutter não encontrado. Instale o Flutter para continuar."
        echo "   Visite: https://flutter.dev/docs/get-started/install"
        return 1
    fi
    
    # Navegar para o diretório do Flutter
    if [ -d "flutter_app" ]; then
        cd flutter_app
        
        # Limpar cache e obter dependências
        flutter clean
        flutter pub get
        
        # Verificar configuração
        flutter doctor
        
        cd ..
        echo "✅ Flutter App configurado!"
    else
        echo "⚠️ Diretório flutter_app não encontrado"
    fi
}

# Função para executar testes
run_tests() {
    echo "🧪 Executando testes..."
    
    # Testes do Backend
    echo "Backend Tests:"
    source venv/bin/activate
    python manage.py test
    
    # Testes do Flutter (se disponível)
    if [ -d "flutter_app" ] && command -v flutter &> /dev/null; then
        echo "Flutter Tests:"
        cd flutter_app
        flutter test
        cd ..
    fi
    
    echo "✅ Testes concluídos!"
}

# Função para iniciar o servidor
start_server() {
    echo "🌐 Iniciando servidor de desenvolvimento..."
    
    source venv/bin/activate
    
    # Verificar se a porta está livre
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️ Porta 8000 já está em uso"
        echo "   Finalize o processo existente ou use outra porta"
        exit 1
    fi
    
    # Iniciar servidor
    echo "🚀 Servidor Django iniciando em http://localhost:8000"
    echo "📱 Para o app móvel, use: http://$(hostname -I | awk '{print $1}'):8000"
    python manage.py runserver 0.0.0.0:8000
}

# Menu principal
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1) 🔧 Configuração completa (recomendado para primeira instalação)"
    echo "2) 📦 Instalar apenas dependências do Backend"
    echo "3) 📱 Configurar Flutter App"
    echo "4) 🗄️ Configurar banco de dados"
    echo "5) 📊 Criar dados de exemplo"
    echo "6) 🧪 Executar testes"
    echo "7) 🌐 Iniciar servidor"
    echo "8) ❌ Sair"
    echo ""
}

# Configuração completa
full_setup() {
    echo "🔧 Iniciando configuração completa..."
    install_backend
    setup_environment
    setup_database
    create_sample_data
    install_flutter
    echo ""
    echo "🎉 Configuração completa finalizada!"
    echo ""
    echo "Próximos passos:"
    echo "1. Edite o arquivo .env com suas configurações"
    echo "2. Execute: ./deploy.sh -> opção 7 para iniciar o servidor"
    echo "3. Acesse http://localhost:8000/admin (admin/admin123)"
    echo ""
}

# Loop principal
while true; do
    show_menu
    read -p "Digite sua opção: " choice
    
    case $choice in
        1)
            full_setup
            ;;
        2)
            install_backend
            ;;
        3)
            install_flutter
            ;;
        4)
            setup_database
            ;;
        5)
            create_sample_data
            ;;
        6)
            run_tests
            ;;
        7)
            start_server
            ;;
        8)
            echo "👋 Tchau!"
            exit 0
            ;;
        *)
            echo "❌ Opção inválida. Tente novamente."
            ;;
    esac
    
    echo ""
    read -p "Pressione Enter para continuar..."
done
