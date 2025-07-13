#!/bin/bash

# Script de inicialização do Sistema de Manutenção
# Executa backend Django e abre opções para o frontend Flutter

set -e

PROJECT_DIR="/home/hendel/Documentos/API_aplicativo_relato"
FLUTTER_DIR="$PROJECT_DIR/flutter_app"

echo "🔧 Sistema de Manutenção - Inicialização"
echo "========================================"

# Função para verificar se uma porta está em uso
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Porta em uso
    else
        return 1  # Porta livre
    fi
}

# Verificar se o Django já está rodando
if check_port 8000; then
    echo "✅ Servidor Django já está rodando na porta 8000"
    
    # Testar se a API está respondendo
    if curl -s http://localhost:8000/api/auth/login/ >/dev/null 2>&1; then
        echo "✅ API respondendo corretamente"
    else
        echo "⚠️  API não está respondendo - pode haver um problema"
    fi
else
    echo "🚀 Iniciando servidor Django..."
    cd "$PROJECT_DIR"
    
    # Verificar se o ambiente virtual existe
    if [ -d "venv" ]; then
        echo "📦 Ativando ambiente virtual..."
        source venv/bin/activate
    fi
    
    # Iniciar servidor em background
    python manage.py runserver &
    DJANGO_PID=$!
    
    echo "⏳ Aguardando servidor inicializar..."
    sleep 3
    
    # Verificar se o servidor iniciou corretamente
    if check_port 8000; then
        echo "✅ Servidor Django iniciado com sucesso (PID: $DJANGO_PID)"
    else
        echo "❌ Falha ao iniciar servidor Django"
        exit 1
    fi
fi

echo ""
echo "📱 Opções do Frontend Flutter:"
echo "1) Executar no emulador/dispositivo"
echo "2) Compilar APK Android"
echo "3) Executar versão web"
echo "4) Apenas mostrar informações"
echo "5) Sair"

read -p "Escolha uma opção (1-5): " choice

cd "$FLUTTER_DIR"

case $choice in
    1)
        echo "🚀 Executando Flutter..."
        flutter devices
        echo ""
        echo "🔄 Iniciando aplicativo..."
        flutter run
        ;;
    2)
        echo "📦 Compilando APK..."
        flutter build apk --debug
        echo "✅ APK gerado em: build/app/outputs/flutter-apk/app-debug.apk"
        ;;
    3)
        echo "🌐 Executando versão web..."
        flutter run -d web-server --web-port 3000
        ;;
    4)
        echo ""
        echo "📊 Informações do Sistema:"
        echo "========================="
        echo "🔗 API Django: http://localhost:8000"
        echo "🔗 Admin: http://localhost:8000/admin"
        echo "🔗 Documentação: $PROJECT_DIR/README.md"
        echo ""
        echo "👥 Usuários de teste:"
        echo "- admin / admin123 (Administrador)"
        echo "- joao.silva / senha123 (Técnico)"
        echo "- maria.santos / senha123 (Supervisora)"
        echo ""
        echo "🛠️ Comandos úteis:"
        echo "- flutter run (executar app)"
        echo "- flutter build apk (compilar APK)"
        echo "- python manage.py runserver (Django)"
        ;;
    5)
        echo "👋 Saindo..."
        # Se iniciamos o Django, vamos parar ele
        if [ ! -z "$DJANGO_PID" ]; then
            echo "🛑 Parando servidor Django..."
            kill $DJANGO_PID 2>/dev/null || true
        fi
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "✨ Sistema pronto para uso!"
echo "📖 Consulte o README.md para mais informações"
