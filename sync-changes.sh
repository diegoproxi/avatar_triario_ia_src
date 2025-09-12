#!/bin/bash

# Script para sincronizar cambios de my-tavus-app a my-tavus-app-clean
# Uso: ./sync-changes.sh

echo "🔄 Sincronizando cambios de my-tavus-app a my-tavus-app-clean..."

# Ir a la carpeta de desarrollo
cd my-tavus-app

# Copiar archivos modificados
echo "📁 Copiando archivos modificados..."
cp src/components/ModernDarkChat.tsx ../my-tavus-app-clean/src/components/
cp src/components/ModernDarkChat.module.css ../my-tavus-app-clean/src/components/
cp src/components/cvi/components/conversation/conversation.module.css ../my-tavus-app-clean/src/components/cvi/components/conversation/
cp src/components/cvi/components/conversation/index.tsx ../my-tavus-app-clean/src/components/cvi/components/conversation/
cp src/components/cvi/hooks/use-cvi-call.tsx ../my-tavus-app-clean/src/components/cvi/hooks/
cp src/components/cvi/hooks/use-text-message.tsx ../my-tavus-app-clean/src/components/cvi/hooks/

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
