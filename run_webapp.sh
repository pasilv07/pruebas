#!/bin/bash

# Script para iniciar la web app

echo "=========================================="
echo "🎓 Visual Audit App - Web Interface"
echo "=========================================="
echo ""

# Verificar que streamlit esté instalado
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit no encontrado. Instalando dependencias..."
    pip install -r requirements.txt
    echo ""
fi

# Verificar .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "💡 Crea el archivo .env y añade tu ANTHROPIC_API_KEY"
    echo ""
fi

# Iniciar streamlit
echo "🚀 Iniciando Visual Audit App Web..."
echo ""
echo "📱 La aplicación se abrirá en tu navegador"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "⏹️  Presiona Ctrl+C para detener el servidor"
echo ""

streamlit run app.py
