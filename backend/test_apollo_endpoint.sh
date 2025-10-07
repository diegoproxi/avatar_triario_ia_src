#!/bin/bash

# Script para probar el endpoint de enriquecimiento de Apollo
# Este script muestra logs detallados de la información que trae Apollo

echo "🧪 SCRIPT DE PRUEBA - LOGS DETALLADOS DE APOLLO API"
echo "=================================================="
echo ""

# Configuración
BASE_URL="http://localhost:5003"
ENDPOINT="/api/test-apollo"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para hacer petición y mostrar resultado
test_domain() {
    local domain=$1
    local company_name=$2
    
    echo -e "${BLUE}🔍 Probando dominio: $company_name ($domain)${NC}"
    echo "------------------------------------------------------------"
    
    # Hacer la petición
    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "{\"domain\": \"$domain\"}" \
        "$BASE_URL$ENDPOINT")
    
    # Verificar si la petición fue exitosa
    if [ $? -eq 0 ]; then
        # Extraer el status de la respuesta JSON
        status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        
        if [ "$status" = "success" ]; then
            echo -e "${GREEN}✅ ÉXITO: Datos enriquecidos obtenidos${NC}"
            
            # Mostrar resumen
            echo ""
            echo -e "${YELLOW}📊 RESUMEN:${NC}"
            echo "$response" | grep -o '"summary":{[^}]*}' | sed 's/"/ /g' | sed 's/,/\n/g' | sed 's/^/  /'
            
            # Mostrar información básica
            echo ""
            echo -e "${YELLOW}🏢 INFORMACIÓN BÁSICA:${NC}"
            echo "$response" | grep -o '"informacion_basica":{[^}]*}' | sed 's/"/ /g' | sed 's/,/\n/g' | sed 's/^/  /'
            
            # Mostrar información financiera
            echo ""
            echo -e "${YELLOW}💰 INFORMACIÓN FINANCIERA:${NC}"
            echo "$response" | grep -o '"financiera":{[^}]*}' | sed 's/"/ /g' | sed 's/,/\n/g' | sed 's/^/  /'
            
            # Mostrar empleados clave
            echo ""
            echo -e "${YELLOW}👥 EMPLEADOS CLAVE:${NC}"
            echo "$response" | grep -o '"empleados_clave":\[[^]]*\]' | sed 's/"/ /g' | sed 's/,/\n/g' | sed 's/^/  /'
            
            # Mostrar ubicaciones
            echo ""
            echo -e "${YELLOW}🌍 UBICACIONES:${NC}"
            echo "$response" | grep -o '"ubicaciones":\[[^]]*\]' | sed 's/"/ /g' | sed 's/,/\n/g' | sed 's/^/  /'
            
        else
            echo -e "${RED}❌ ERROR: No se pudieron obtener datos${NC}"
            echo "$response" | grep -o '"error":"[^"]*"' | cut -d'"' -f4
        fi
    else
        echo -e "${RED}❌ ERROR: No se pudo conectar al servidor${NC}"
        echo "Asegúrate de que el servidor esté ejecutándose en $BASE_URL"
    fi
    
    echo ""
    echo "============================================================"
    echo ""
}

# Verificar si el servidor está ejecutándose
echo -e "${BLUE}🔧 Verificando conexión al servidor...${NC}"
health_response=$(curl -s "$BASE_URL/health")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Servidor conectado correctamente${NC}"
    echo ""
else
    echo -e "${RED}❌ No se puede conectar al servidor en $BASE_URL${NC}"
    echo "Por favor, asegúrate de que el servidor esté ejecutándose:"
    echo "  cd backend && python app.py"
    exit 1
fi

# Lista de dominios para probar
echo -e "${YELLOW}📋 Dominios disponibles para probar:${NC}"
echo "1. Google (google.com)"
echo "2. Microsoft (microsoft.com)"
echo "3. Apple (apple.com)"
echo "4. OpenAI (openai.com)"
echo "5. Apollo (apollo.io)"
echo "6. GitHub (github.com)"
echo "7. Salesforce (salesforce.com)"
echo "8. HubSpot (hubspot.com)"
echo "9. Dominio personalizado"
echo "10. Todos los dominios"
echo ""

# Solicitar opción al usuario
read -p "Selecciona una opción (1-10): " choice

case $choice in
    1)
        test_domain "google.com" "Google"
        ;;
    2)
        test_domain "microsoft.com" "Microsoft"
        ;;
    3)
        test_domain "apple.com" "Apple"
        ;;
    4)
        test_domain "openai.com" "OpenAI"
        ;;
    5)
        test_domain "apollo.io" "Apollo"
        ;;
    6)
        test_domain "github.com" "GitHub"
        ;;
    7)
        test_domain "salesforce.com" "Salesforce"
        ;;
    8)
        test_domain "hubspot.com" "HubSpot"
        ;;
    9)
        read -p "Ingresa el dominio (ej: example.com): " custom_domain
        read -p "Ingresa el nombre de la empresa (opcional): " custom_name
        test_domain "$custom_domain" "${custom_name:-$custom_domain}"
        ;;
    10)
        echo -e "${YELLOW}🔄 Probando todos los dominios...${NC}"
        test_domain "google.com" "Google"
        test_domain "microsoft.com" "Microsoft"
        test_domain "apple.com" "Apple"
        test_domain "openai.com" "OpenAI"
        test_domain "apollo.io" "Apollo"
        test_domain "github.com" "GitHub"
        test_domain "salesforce.com" "Salesforce"
        test_domain "hubspot.com" "HubSpot"
        ;;
    *)
        echo -e "${RED}Opción inválida. Probando Apollo por defecto...${NC}"
        test_domain "apollo.io" "Apollo"
        ;;
esac

echo -e "${GREEN}🎉 Pruebas completadas${NC}"
echo ""
echo -e "${BLUE}💡 Para ver logs más detallados, revisa la consola del servidor${NC}"
echo -e "${BLUE}📝 Los logs también se guardan en el archivo de log del servidor${NC}"
