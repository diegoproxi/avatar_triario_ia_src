#!/bin/bash

# Script de prueba para los endpoints de conversación
# Asegúrate de que el servidor backend esté ejecutándose en localhost:5003

echo "🧪 INICIANDO PRUEBAS DE ENDPOINTS DE CONVERSACIÓN"
echo "=================================================="

BASE_URL="http://localhost:5003"
TEST_CONVERSATION_ID="test-conv-$(date +%s)"
TEST_HUBSPOT_ID="hubspot-test-$(date +%s)"

echo "📝 Datos de prueba:"
echo "   - BASE_URL: $BASE_URL"
echo "   - TEST_CONVERSATION_ID: $TEST_CONVERSATION_ID"
echo "   - TEST_HUBSPOT_ID: $TEST_HUBSPOT_ID"
echo ""

# Función para hacer peticiones HTTP
make_request() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    
    echo "🔍 $description"
    echo "   URL: $method $url"
    
    if [ -n "$data" ]; then
        echo "   Data: $data"
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$url")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url")
    fi
    
    # Separar respuesta y código HTTP
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    echo "   Status: $http_code"
    echo "   Response: $body"
    echo ""
    
    return $http_code
}

# 1. Probar health check
echo "1️⃣ PROBANDO HEALTH CHECK"
echo "------------------------"
make_request "GET" "$BASE_URL/health" "" "Health check del servidor"

# 2. Crear un prospecto con conversation_id (simulado)
echo "2️⃣ PROBANDO CREACIÓN DE PROSPECTO CON CONVERSATION_ID"
echo "----------------------------------------------------"
PROSPECT_DATA='{
    "nombres": "María",
    "apellidos": "González",
    "compania": "Empresa Demo",
    "websiteUrl": "https://empresademo.com",
    "emailCorporativo": "maria.gonzalez@empresademo.com",
    "rol": "CTO",
    "conversation_id": "'$TEST_CONVERSATION_ID'"
}'

make_request "POST" "$BASE_URL/api/prospect" "$PROSPECT_DATA" "Crear prospecto con conversation_id"

# 3. Consultar mapeo completo
echo "3️⃣ PROBANDO CONSULTA DE MAPEO COMPLETO"
echo "--------------------------------------"
make_request "GET" "$BASE_URL/api/conversation/$TEST_CONVERSATION_ID" "" "Consultar mapeo completo"

# 4. Consultar solo hubspot_id
echo "4️⃣ PROBANDO CONSULTA DE HUBSPOT_ID"
echo "----------------------------------"
make_request "GET" "$BASE_URL/api/conversation/$TEST_CONVERSATION_ID/hubspot" "" "Consultar solo hubspot_id"

# 5. Listar todas las conversaciones
echo "5️⃣ PROBANDO LISTADO DE CONVERSACIONES"
echo "-------------------------------------"
make_request "GET" "$BASE_URL/api/conversations?limit=10" "" "Listar conversaciones"

# 6. Probar consulta de conversation_id inexistente
echo "6️⃣ PROBANDO CONSULTA DE ID INEXISTENTE"
echo "--------------------------------------"
make_request "GET" "$BASE_URL/api/conversation/non-existent-id" "" "Consultar ID inexistente"

echo "🎉 PRUEBAS DE ENDPOINTS COMPLETADAS"
echo "==================================="
echo ""
echo "📋 RESUMEN:"
echo "   - Health check: Verificar que el servidor esté funcionando"
echo "   - Crear prospecto: Debería almacenar el mapeo conversation_id -> hubspot_id"
echo "   - Consultar mapeo: Debería retornar toda la información almacenada"
echo "   - Consultar hubspot_id: Debería retornar solo el ID de HubSpot"
echo "   - Listar conversaciones: Debería mostrar todas las conversaciones almacenadas"
echo "   - ID inexistente: Debería retornar 404"
echo ""
echo "💡 NOTA: Si el servidor no está ejecutándose, inicia el backend con:"
echo "   cd backend && python app.py"
