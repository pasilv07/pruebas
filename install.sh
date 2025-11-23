#!/bin/bash

# Script de instalación rápida para Visual Audit App

echo "=========================================="
echo "🎓 Visual Audit App - Instalación"
echo "=========================================="
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Por favor instala Python 3.8 o superior."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"
echo ""

# Crear entorno virtual (opcional pero recomendado)
read -p "¿Crear entorno virtual? (recomendado) [Y/n]: " CREATE_VENV
CREATE_VENV=${CREATE_VENV:-Y}

if [[ "$CREATE_VENV" =~ ^[Yy]$ ]]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv

    echo "🔄 Activando entorno virtual..."
    source venv/bin/activate

    echo "✅ Entorno virtual creado y activado"
    echo ""
fi

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi
echo ""

# Configurar .env
if [ ! -f .env ]; then
    echo "⚙️  Configurando .env..."
    cp .env.example .env
    echo "✅ .env creado desde .env.example"
    echo ""
    echo "⚠️  IMPORTANTE: Edita .env y añade tu ANTHROPIC_API_KEY"
    echo "   Obtén tu API key en: https://console.anthropic.com/"
else
    echo "✅ .env ya existe"
fi
echo ""

# Crear directorios
echo "📁 Creando directorios..."
mkdir -p output examples
echo "✅ Directorios creados"
echo ""

# Permisos de ejecución
echo "🔐 Configurando permisos..."
chmod +x main.py
echo "✅ Permisos configurados"
echo ""

# Prueba de configuración
echo "=========================================="
echo "🎉 Instalación completada"
echo "=========================================="
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Configura tu API key:"
echo "   nano .env"
echo "   (añade: ANTHROPIC_API_KEY=tu_api_key_aqui)"
echo ""
echo "2. Coloca imágenes en examples/"
echo ""
echo "3. Ejecuta el setup:"
echo "   python main.py setup"
echo ""
echo "4. Analiza tu primera imagen:"
echo "   python main.py analyze examples/tu_imagen.jpg"
echo ""
echo "5. O procesa un lote:"
echo "   python main.py batch examples/"
echo ""

if [[ "$CREATE_VENV" =~ ^[Yy]$ ]]; then
    echo "💡 Nota: Para activar el entorno virtual en el futuro:"
    echo "   source venv/bin/activate"
    echo ""
fi

echo "📖 Documentación completa en README.md"
echo "❓ Ayuda: python main.py --help"
echo ""
