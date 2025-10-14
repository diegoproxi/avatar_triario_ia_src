#!/bin/bash

# Script para sincronizar cambios de my-tavus-app a my-tavus-app-clean
# Uso: ./sync-changes.sh

echo "🔄 Sincronizando cambios de my-tavus-app a my-tavus-app-clean..."

# Ir a la carpeta de desarrollo
cd my-tavus-app

# Crear directorios necesarios en destino si no existen
echo "📁 Creando directorios necesarios..."
mkdir -p ../my-tavus-app-clean/src/components/cvi/components/conversation
mkdir -p ../my-tavus-app-clean/src/components/cvi/hooks
mkdir -p ../my-tavus-app-clean/src/contexts

# Copiar TODOS los archivos modificados y nuevos
echo "📁 Copiando archivos modificados..."
cp src/App.tsx ../my-tavus-app-clean/src/
cp src/components/ModernDarkChat.tsx ../my-tavus-app-clean/src/components/
cp src/components/ModernDarkChat.module.css ../my-tavus-app-clean/src/components/
cp src/components/cvi/components/conversation/conversation.module.css ../my-tavus-app-clean/src/components/cvi/components/conversation/
cp src/components/cvi/components/conversation/index.tsx ../my-tavus-app-clean/src/components/cvi/components/conversation/
cp src/components/cvi/hooks/use-cvi-call.tsx ../my-tavus-app-clean/src/components/cvi/hooks/

# Copiar archivos nuevos
echo "📁 Copiando archivos nuevos..."
cp LANGUAGE_FEATURE.md ../my-tavus-app-clean/
cp env.example ../my-tavus-app-clean/
cp src/components/LanguageSelector.module.css ../my-tavus-app-clean/src/components/
cp src/components/LanguageSelector.tsx ../my-tavus-app-clean/src/components/
cp src/components/ProspectForm.module.css ../my-tavus-app-clean/src/components/
cp src/components/ProspectForm.tsx ../my-tavus-app-clean/src/components/
cp src/components/cvi/hooks/use-text-message.tsx ../my-tavus-app-clean/src/components/cvi/hooks/

# Copiar carpeta de contextos completa
echo "📁 Copiando carpeta de contextos..."
cp -r src/contexts/ ../my-tavus-app-clean/src/

# Copiar archivos de configuración si han cambiado
echo "📁 Copiando archivos de configuración..."
if [ -f package.json ]; then
    cp package.json ../my-tavus-app-clean/
fi
if [ -f package-lock.json ]; then
    cp package-lock.json ../my-tavus-app-clean/
fi
if [ -f .gitignore ]; then
    cp .gitignore ../my-tavus-app-clean/
fi

# Ir a la carpeta del repositorio
cd ../my-tavus-app-clean

# Verificar cambios
echo "📊 Verificando cambios..."
git status

# Preguntar si hacer commit
read -p "¿Hacer commit y push de los cambios? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "💾 Haciendo commit..."
    git add .
    git commit -m "Sync changes from development - $(date '+%Y-%m-%d %H:%M')"
    
    echo "🚀 Subiendo al repositorio..."
    git push origin main
    
    echo "✅ ¡Cambios sincronizados y subidos exitosamente!"
else
    echo "⏸️ Cambios preparados pero no subidos. Ejecuta manualmente:"
    echo "   cd my-tavus-app-clean"
    echo "   git add ."
    echo "   git commit -m 'Sync changes'"
    echo "   git push origin main"
fi
