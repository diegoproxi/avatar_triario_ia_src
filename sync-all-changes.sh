#!/bin/bash

# Script mejorado para sincronizar TODOS los cambios de my-tavus-app a my-tavus-app-clean
# Uso: ./sync-all-changes.sh

echo "🔄 Sincronizando TODOS los cambios de my-tavus-app a my-tavus-app-clean..."

# Ir a la carpeta de desarrollo
cd my-tavus-app

# Crear directorios necesarios en destino si no existen
echo "📁 Creando directorios necesarios..."
mkdir -p ../my-tavus-app-clean/src/components/cvi/components/conversation
mkdir -p ../my-tavus-app-clean/src/components/cvi/hooks
mkdir -p ../my-tavus-app-clean/src/contexts

# Función para copiar archivos de manera segura
copy_file() {
    local source="$1"
    local dest="$2"
    
    if [ -f "$source" ]; then
        echo "  📄 Copiando: $source -> $dest"
        mkdir -p "$(dirname "$dest")"
        cp "$source" "$dest"
    else
        echo "  ⚠️  Archivo no encontrado: $source"
    fi
}

# Copiar archivos modificados (según git status)
echo "📁 Copiando archivos modificados..."
copy_file "src/App.tsx" "../my-tavus-app-clean/src/App.tsx"
copy_file "src/components/ModernDarkChat.tsx" "../my-tavus-app-clean/src/components/ModernDarkChat.tsx"
copy_file "src/components/cvi/components/conversation/conversation.module.css" "../my-tavus-app-clean/src/components/cvi/components/conversation/conversation.module.css"
copy_file "src/components/cvi/components/conversation/index.tsx" "../my-tavus-app-clean/src/components/cvi/components/conversation/index.tsx"
copy_file "src/components/cvi/hooks/use-cvi-call.tsx" "../my-tavus-app-clean/src/components/cvi/hooks/use-cvi-call.tsx"

# Copiar archivos nuevos
echo "📁 Copiando archivos nuevos..."
copy_file "LANGUAGE_FEATURE.md" "../my-tavus-app-clean/LANGUAGE_FEATURE.md"
copy_file "env.example" "../my-tavus-app-clean/env.example"
copy_file "src/components/LanguageSelector.module.css" "../my-tavus-app-clean/src/components/LanguageSelector.module.css"
copy_file "src/components/LanguageSelector.tsx" "../my-tavus-app-clean/src/components/LanguageSelector.tsx"
copy_file "src/components/ModernDarkChat.module.css" "../my-tavus-app-clean/src/components/ModernDarkChat.module.css"
copy_file "src/components/ProspectForm.module.css" "../my-tavus-app-clean/src/components/ProspectForm.module.css"
copy_file "src/components/ProspectForm.tsx" "../my-tavus-app-clean/src/components/ProspectForm.tsx"
copy_file "src/components/cvi/hooks/use-text-message.tsx" "../my-tavus-app-clean/src/components/cvi/hooks/use-text-message.tsx"

# Copiar carpeta de contextos completa
echo "📁 Copiando carpeta de contextos..."
if [ -d "src/contexts" ]; then
    echo "  📁 Copiando directorio: src/contexts/"
    cp -r src/contexts/ ../my-tavus-app-clean/src/
else
    echo "  ⚠️  Directorio no encontrado: src/contexts"
fi

# Copiar archivos de configuración si han cambiado
echo "📁 Copiando archivos de configuración..."
copy_file "package.json" "../my-tavus-app-clean/package.json"
copy_file "package-lock.json" "../my-tavus-app-clean/package-lock.json"
copy_file ".gitignore" "../my-tavus-app-clean/.gitignore"

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
    git commit -m "Sync ALL changes from development - $(date '+%Y-%m-%d %H:%M')"
    
    echo "🚀 Subiendo al repositorio..."
    git push origin main
    
    echo "✅ ¡Todos los cambios sincronizados y subidos exitosamente!"
else
    echo "⏸️ Cambios preparados pero no subidos. Ejecuta manualmente:"
    echo "   cd my-tavus-app-clean"
    echo "   git add ."
    echo "   git commit -m 'Sync ALL changes'"
    echo "   git push origin main"
fi
