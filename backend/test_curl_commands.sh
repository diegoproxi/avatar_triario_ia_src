#!/bin/bash

# Script para probar la integración Apollo API usando curl
# Dominio de prueba: triario.com

echo "🧪 Script de Pruebas - Apollo API Integration"
echo "=============================================="
echo "🕐 $(date)"
echo "🎯 Dominio: triario.com"
echo ""

# Configuración
BACKEND_URL="http://localhost:5003"
DOMAIN="triario.com"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_separator() {
    echo ""
    echo "=============================================="
    echo "$1"
    echo "=============================================="
    echo ""
}

# Función para formatear JSON
format_json() {
    if command -v jq &> /dev/null; then
        jq .
    else
        cat
    fi
}

# Prueba 1: Health Check del Backend
test_backend_health() {
    print_separator "PRUEBA 1: Backend Health Check"
    
    print_step "Verificando estado del backend..."
    
    response=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/health" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -eq 200 ]; then
        print_success "Backend está funcionando"
        echo "Respuesta:"
        echo "$body" | format_json
        return 0
    else
        print_error "Backend no responde (HTTP $http_code)"
        echo "Respuesta: $body"
        return 1
    fi
}

# Prueba 2: Apollo API Directa
test_apollo_direct() {
    print_separator "PRUEBA 2: Apollo API Directa"
    
    print_step "Consultando Apollo API para $DOMAIN..."
    
    response=$(curl -s -w "\n%{http_code}" \
        --request GET \
        --url "https://api.apollo.io/api/v1/organizations/enrich?domain=$DOMAIN" \
        --header 'Cache-Control: no-cache' \
        --header 'Content-Type: application/json' \
        --header 'accept: application/json' \
        --header 'x-api-key: ATpjar6DGtZOKVJWSTiGXQ' \
        2>/dev/null)
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -eq 200 ]; then
        print_success "Apollo API responde correctamente"
        echo "Datos obtenidos:"
        echo "$body" | format_json
        
        # Extraer información básica
        org_name=$(echo "$body" | format_json | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
        industry=$(echo "$body" | format_json | grep -o '"industry":"[^"]*"' | head -1 | cut -d'"' -f4)
        employees=$(echo "$body" | format_json | grep -o '"estimated_num_employees":"[^"]*"' | head -1 | cut -d'"' -f4)
        
        if [ ! -z "$org_name" ]; then
            echo ""
            echo "📋 Información extraída:"
            echo "   Empresa: $org_name"
            echo "   Industria: $industry"
            echo "   Empleados: $employees"
        fi
        
        return 0
    else
        print_error "Error de Apollo API (HTTP $http_code)"
        echo "Respuesta: $body"
        return 1
    fi
}

# Prueba 3: Endpoint de Enriquecimiento de Contexto
test_enrich_context() {
    print_separator "PRUEBA 3: Endpoint Enrich Context"
    
    print_step "Probando enriquecimiento de contexto..."
    
    payload='{
        "websiteUrl": "'$DOMAIN'",
        "nombres": "Juan",
        "apellidos": "Pérez",
        "compania": "Triario",
        "emailCorporativo": "juan@triario.com",
        "rol": "CEO"
    }'
    
    response=$(curl -s -w "\n%{http_code}" \
        -X POST "$BACKEND_URL/api/enrich-context" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        2>/dev/null)
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -eq 200 ]; then
        print_success "Contexto enriquecido exitosamente"
        echo "Respuesta:"
        echo "$body" | format_json
        
        # Verificar si el contexto fue generado
        if echo "$body" | grep -q "context"; then
            print_success "Contexto generado para el agente"
        fi
        
        return 0
    else
        print_error "Error enriqueciendo contexto (HTTP $http_code)"
        echo "Respuesta: $body"
        return 1
    fi
}

# Prueba 4: Endpoint de Prospecto con Enriquecimiento
test_prospect_enrichment() {
    print_separator "PRUEBA 4: Endpoint Prospect + Enrichment"
    
    print_step "Probando creación de prospecto con enriquecimiento..."
    
    payload='{
        "nombres": "Juan",
        "apellidos": "Pérez",
        "compania": "Triario",
        "websiteUrl": "https://'$DOMAIN'",
        "emailCorporativo": "juan@triario.com",
        "rol": "CEO"
    }'
    
    response=$(curl -s -w "\n%{http_code}" \
        -X POST "$BACKEND_URL/api/prospect" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        2>/dev/null)
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -eq 200 ]; then
        print_success "Prospecto creado exitosamente"
        echo "Respuesta:"
        echo "$body" | format_json
        
        # Verificar si se incluyeron datos enriquecidos
        if echo "$body" | grep -q "enriched_company_data"; then
            print_success "Datos enriquecidos incluidos en la respuesta"
        else
            print_warning "No se incluyeron datos enriquecidos"
        fi
        
        return 0
    else
        print_error "Error creando prospecto (HTTP $http_code)"
        echo "Respuesta: $body"
        return 1
    fi
}

# Función principal
main() {
    echo "🚀 Iniciando pruebas de integración..."
    echo ""
    
    # Contador de pruebas exitosas
    passed=0
    total=4
    
    # Ejecutar pruebas
    if test_backend_health; then
        ((passed++))
        
        if test_enrich_context; then
            ((passed++))
        fi
        
        if test_prospect_enrichment; then
            ((passed++))
        fi
    else
        print_warning "Saltando pruebas de backend - servidor no disponible"
        print_warning "Para ejecutar el backend: cd backend && python run.py"
    fi
    
    # Apollo API siempre se puede probar independientemente
    if test_apollo_direct; then
        ((passed++))
    fi
    
    # Resumen final
    print_separator "RESUMEN FINAL"
    
    echo "📊 Resultado: $passed/$total pruebas exitosas"
    echo ""
    
    if [ $passed -eq $total ]; then
        print_success "🎉 ¡Todas las pruebas pasaron! La integración está funcionando correctamente."
    elif [ $passed -gt 0 ]; then
        print_warning "⚠️ Algunas pruebas fallaron. Revisa los errores arriba."
    else
        print_error "❌ Todas las pruebas fallaron. Verifica la configuración."
    fi
    
    echo ""
    echo "💡 Comandos útiles:"
    echo "   - Ejecutar backend: cd backend && python run.py"
    echo "   - Ver logs: tail -f backend/logs/app.log"
    echo "   - Probar solo Apollo: python backend/test_apollo_quick.py"
    echo ""
}

# Ejecutar si se llama directamente
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi
