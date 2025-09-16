#!/bin/bash

# Script para desplegar en Vercel
echo "🚀 Preparando despliegue en Vercel..."

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encontró app.py. Ejecuta este script desde el directorio backend/"
    exit 1
fi

# Verificar que git está configurado
if ! git status &> /dev/null; then
    echo "❌ Error: No se encontró repositorio git. Inicializa git primero."
    exit 1
fi

# Verificar que Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "📦 Instalando Vercel CLI..."
    npm install -g vercel
fi

echo "📋 Verificando archivos de configuración..."

# Verificar archivos necesarios
required_files=("app.py" "requirements.txt" "vercel.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Archivo requerido no encontrado: $file"
        exit 1
    fi
done

echo "✅ Archivos de configuración encontrados"

# Hacer commit de cambios
echo "📝 Haciendo commit de cambios..."
git add .
git commit -m "Preparar para despliegue en Vercel" || echo "⚠️ No hay cambios para commitear"

# Push a GitHub
echo "📤 Enviando cambios a GitHub..."
git push origin main

echo "🌐 Iniciando despliegue en Vercel..."
echo "📋 Sigue estos pasos:"
echo "1. Ve a https://vercel.com"
echo "2. Conecta tu cuenta de GitHub"
echo "3. Selecciona tu repositorio 'tavus_ensayo'"
echo "4. Configura Root Directory como 'backend'"
echo "5. Agrega las variables de entorno:"
echo "   - HUBSPOT_API_KEY"
echo "   - HUBSPOT_PORTAL_ID"
echo "   - RESEND_API_KEY"
echo "   - FROM_EMAIL"
echo "   - FLASK_ENV=production"
echo "6. Haz clic en 'Deploy'"

echo ""
echo "🎉 ¡Despliegue iniciado! Tu backend estará disponible en:"
echo "   https://tu-proyecto.vercel.app"
echo ""
echo "📚 Para más detalles, consulta VERCEL_SETUP.md"
