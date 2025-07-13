#!/bin/bash

# Script Docker para Sistema de Manutenção
# Facilita o uso do Docker Compose

set -e

echo "🐳 Docker Manager - Sistema de Manutenção"
echo "========================================"

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Instale o Docker Compose primeiro."
    exit 1
fi

# Função para iniciar em modo desenvolvimento
dev_start() {
    echo "🚀 Iniciando em modo desenvolvimento..."
    docker-compose up --build
}

# Função para iniciar em background
dev_start_detached() {
    echo "🚀 Iniciando em modo desenvolvimento (background)..."
    docker-compose up -d --build
    echo "✅ Serviços iniciados!"
    echo "🌐 API: http://localhost:8000"
    echo "📊 Admin: http://localhost:8000/admin"
}

# Função para iniciar em modo produção
prod_start() {
    echo "🚀 Iniciando em modo produção..."
    docker-compose --profile production up -d --build
    echo "✅ Serviços de produção iniciados!"
    echo "🌐 Site: http://localhost"
}

# Função para parar serviços
stop_services() {
    echo "⏹️ Parando serviços..."
    docker-compose down
    echo "✅ Serviços parados!"
}

# Função para limpar containers e volumes
clean_all() {
    echo "🧹 Limpando containers e volumes..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    echo "✅ Limpeza concluída!"
}

# Função para ver logs
show_logs() {
    echo "📝 Mostrando logs..."
    docker-compose logs -f
}

# Função para executar migrações
run_migrations() {
    echo "🗄️ Executando migrações..."
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    echo "✅ Migrações executadas!"
}

# Função para criar superusuário
create_superuser() {
    echo "👤 Criando superusuário..."
    docker-compose exec web python manage.py createsuperuser
}

# Função para carregar dados de exemplo
load_sample_data() {
    echo "📊 Carregando dados de exemplo..."
    docker-compose exec web python create_sample_data.py
    echo "✅ Dados de exemplo carregados!"
}

# Função para backup do banco
backup_database() {
    echo "💾 Fazendo backup do banco de dados..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    docker-compose exec db pg_dump -U maintenance_user maintenance_db > "backup_${timestamp}.sql"
    echo "✅ Backup salvo como backup_${timestamp}.sql"
}

# Função para verificar status
check_status() {
    echo "📊 Status dos serviços:"
    docker-compose ps
    echo ""
    echo "🔍 Logs recentes:"
    docker-compose logs --tail=10
}

# Menu principal
show_menu() {
    echo ""
    echo "Escolha uma opção:"
    echo "1) 🚀 Iniciar desenvolvimento (interativo)"
    echo "2) 🚀 Iniciar desenvolvimento (background)"
    echo "3) 🏭 Iniciar produção"
    echo "4) ⏹️ Parar serviços"
    echo "5) 📝 Ver logs"
    echo "6) 📊 Status dos serviços"
    echo "7) 🗄️ Executar migrações"
    echo "8) 👤 Criar superusuário"
    echo "9) 📊 Carregar dados de exemplo"
    echo "10) 💾 Backup do banco"
    echo "11) 🧹 Limpar tudo"
    echo "12) ❌ Sair"
    echo ""
}

# Loop principal
while true; do
    show_menu
    read -p "Digite sua opção: " choice
    
    case $choice in
        1)
            dev_start
            ;;
        2)
            dev_start_detached
            ;;
        3)
            prod_start
            ;;
        4)
            stop_services
            ;;
        5)
            show_logs
            ;;
        6)
            check_status
            ;;
        7)
            run_migrations
            ;;
        8)
            create_superuser
            ;;
        9)
            load_sample_data
            ;;
        10)
            backup_database
            ;;
        11)
            clean_all
            ;;
        12)
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
