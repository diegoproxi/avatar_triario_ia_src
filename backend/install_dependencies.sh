#!/bin/bash

# Script para instalar dependencias del sistema de análisis de conversaciones

echo "🔧 INSTALANDO DEPENDENCIAS PARA ANÁLISIS DE CONVERSACIONES"
echo "=========================================================="

# Verificar si estamos en un entorno virtual
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Entorno virtual detectado: $VIRTUAL_ENV"
else
    echo "⚠️  No se detectó entorno virtual. Se recomienda usar uno."
    read -p "¿Continuar de todos modos? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Instalación cancelada"
        exit 1
    fi
fi

echo ""
echo "📦 Instalando dependencias principales..."

# Instalar dependencias base
pip install --upgrade pip

# Instalar dependencias de LangChain y OpenAI
echo "🤖 Instalando LangChain y OpenAI..."
pip install langchain==0.1.0
pip install langchain-openai==0.0.5
pip install openai==1.6.1

# Instalar dependencias existentes
echo "📋 Instalando dependencias existentes..."
pip install -r requirements.txt

echo ""
echo "🔍 Verificando instalación..."

# Verificar instalaciones críticas
python -c "import langchain; print('✅ LangChain instalado correctamente')" 2>/dev/null || echo "❌ Error instalando LangChain"
python -c "import openai; print('✅ OpenAI instalado correctamente')" 2>/dev/null || echo "❌ Error instalando OpenAI"
python -c "import pydantic; print('✅ Pydantic instalado correctamente')" 2>/dev/null || echo "❌ Error instalando Pydantic"

echo ""
echo "🔧 Configuración de variables de entorno..."

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# HubSpot Configuration  
HUBSPOT_API_KEY=your_hubspot_api_key_here
HUBSPOT_PORTAL_ID=your_hubspot_portal_id_here

# Resend Configuration
RESEND_API_KEY=your_resend_api_key_here
FROM_EMAIL=your_from_email_here

# Flask Configuration
FLASK_ENV=development
PORT=5003
EOF
    echo "✅ Archivo .env creado"
    echo "⚠️  IMPORTANTE: Configura las variables de entorno en el archivo .env"
else
    echo "✅ Archivo .env ya existe"
fi

echo ""
echo "🧪 Ejecutando pruebas básicas..."

# Probar importaciones
python -c "
try:
    from agents.conversation_analyzer import conversation_analyzer
    from api.hubspot_fields import update_contact_pain_field
    from storage.conversation_storage import conversation_storage
    print('✅ Todas las importaciones funcionan correctamente')
except ImportError as e:
    print(f'❌ Error en importaciones: {e}')
"

echo ""
echo "📚 Documentación disponible:"
echo "   - CONVERSATION_ANALYSIS.md: Sistema de análisis de conversaciones"
echo "   - CONVERSATION_STORAGE.md: Sistema de almacenamiento de mapeos"
echo ""
echo "🧪 Scripts de prueba disponibles:"
echo "   - test_conversation_storage.py: Pruebas del sistema de almacenamiento"
echo "   - test_transcript_webhook.py: Pruebas del webhook de transcripciones"
echo "   - test_conversation_endpoints.sh: Pruebas de endpoints REST"
echo ""
echo "🎉 INSTALACIÓN COMPLETADA"
echo "=========================="
echo ""
echo "Próximos pasos:"
echo "1. Configura las variables de entorno en .env"
echo "2. Ejecuta 'python app.py' para iniciar el servidor"
echo "3. Ejecuta las pruebas para verificar el funcionamiento"
echo ""
echo "Para probar el sistema:"
echo "   python test_transcript_webhook.py"
