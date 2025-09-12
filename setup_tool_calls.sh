#!/bin/bash

# Script para configurar el sistema de tool calls de Tavus
# Este script configura tanto el frontend como el backend

echo "🚀 Configurando sistema de tool calls de Tavus"
echo "=============================================="

# Verificar que estamos en el directorio correcto
if [ ! -d "my-tavus-app" ] || [ ! -d "backend" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# 1. Configurar backend
echo ""
echo "📦 Configurando backend..."
cd backend

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env para el backend..."
    cp env.example .env
    echo "✅ Archivo .env creado. Por favor, edita las credenciales de email."
else
    echo "✅ Archivo .env ya existe"
fi

# Instalar dependencias
echo "📦 Instalando dependencias del backend..."
pip install -r requirements.txt

cd ..

# 2. Configurar frontend
echo ""
echo "🎨 Configurando frontend..."

cd my-tavus-app

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env para el frontend..."
    cp env.example .env
    echo "✅ Archivo .env creado. Por favor, configura las variables de Tavus y el webhook URL."
else
    echo "✅ Archivo .env ya existe"
fi

# Instalar dependencias
echo "📦 Instalando dependencias del frontend..."
npm install

cd ..

# 3. Mostrar instrucciones
echo ""
echo "✅ Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Configurar credenciales:"
echo "   - Edita backend/.env con tus credenciales de email"
echo "   - Edita my-tavus-app/.env con tu API key de Tavus y URL del webhook"
echo ""
echo "2. Ejecutar el backend:"
echo "   cd backend"
echo "   python run.py"
echo ""
echo "3. En otra terminal, ejecutar el frontend:"
echo "   cd my-tavus-app"
echo "   npm run dev"
echo ""
echo "4. Probar el webhook:"
echo "   cd backend"
echo "   python test_webhook.py"
echo ""
echo "🔗 URLs importantes:"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend: http://localhost:5000"
echo "   - Webhook: http://localhost:5000/webhook"
echo "   - Health Check: http://localhost:5000/health"
echo ""
echo "📚 Documentación: backend/README.md"
