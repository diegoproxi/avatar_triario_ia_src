#!/bin/bash

echo "🚂 Desplegando a Railway..."

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encontró app.py en el directorio actual"
    exit 1
fi

# Verificar que Railway CLI está disponible
if ! command -v railway &> /dev/null; then
    echo "📦 Instalando Railway CLI..."
    npm install -g @railway/cli
fi

# Iniciar sesión en Railway
echo "🔐 Iniciando sesión en Railway..."
railway login

# Inicializar proyecto Railway
echo "🏗️ Inicializando proyecto Railway..."
railway init

# Desplegar
echo "🚀 Desplegando aplicación..."
railway up

echo "✅ Despliegue completado!"
echo "🌐 Tu aplicación estará disponible en: https://tu-proyecto.railway.app"



