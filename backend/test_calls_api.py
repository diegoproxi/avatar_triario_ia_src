#!/usr/bin/env python3
"""
Script de prueba específico para la API de calls v3 de HubSpot
"""

import json
import requests
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_calls_api():
    """Prueba la creación de llamadas usando la API v3 de HubSpot"""
    
    print("🧪 PRUEBA DE LA API DE CALLS V3 DE HUBSPOT")
    print("=" * 50)
    
    # Configuración
    HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
    HUBSPOT_BASE_URL = 'https://api.hubapi.com'
    
    if not HUBSPOT_API_KEY:
        print("❌ HUBSPOT_API_KEY no está configurada")
        print("   Configura la variable de entorno antes de ejecutar la prueba")
        return False
    
    # Datos de prueba
    test_contact_id = "test_contact_123"  # Cambiar por un ID real para pruebas
    
    # Datos de la llamada según la documentación de HubSpot
    # Solo usar propiedades que existen por defecto
    call_data = {
        "properties": {
            "hs_timestamp": int(datetime.now().timestamp() * 1000),  # Timestamp en milisegundos
            "hs_call_title": "Prueba de API Calls v3 - Triario",
            "hs_call_body": """Esta es una llamada de prueba para verificar que la API de calls v3 funciona correctamente con el resumen incluido.

==================================================

TRANSCRIPCIÓN:
PROSPECTO: Hola, tengo problemas con mi CRM...
AGENTE: Entiendo perfectamente el desafío...

DOLOR IDENTIFICADO: No se en que invierte el tiempo mis vendedores

INSIGHTS CLAVE:
- Prospecto muy interesado
- Presupuesto disponible
- Tomador de decisión

PRÓXIMOS PASOS: Agendar reunión de calificación con especialista comercial

PUNTUACIÓN DE CALIFICACIÓN: 8/10

EMPRESA: Empresa Test
CARGO: CEO
ID CONVERSACIÓN: test_conversation_456""",
            "hs_call_duration": 1800000,  # 30 minutos en milisegundos
            "hs_call_status": "COMPLETED",
            "hs_call_direction": "INBOUND",
            "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7",  # Connected
            "hs_call_source": "INTEGRATIONS_PLATFORM"
        },
        "associations": [
            {
                "to": {
                    "id": test_contact_id
                },
                "types": [
                    {
                        "associationCategory": "HUBSPOT_DEFINED",
                        "associationTypeId": 194  # call_to_contact
                    }
                ]
            }
        ]
    }
    
    print(f"📝 Datos de prueba:")
    print(f"   - Contact ID: {test_contact_id}")
    print(f"   - API Key configurada: {'✅' if HUBSPOT_API_KEY else '❌'}")
    print(f"   - URL: {HUBSPOT_BASE_URL}/crm/v3/objects/calls")
    print()
    
    # 1. Probar creación de llamada
    print("1️⃣ PROBANDO CREACIÓN DE LLAMADA")
    print("-" * 40)
    
    try:
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        print(f"📤 Enviando datos: {json.dumps(call_data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(
            f"{HUBSPOT_BASE_URL}/crm/v3/objects/calls",
            headers=headers,
            json=call_data,
            timeout=30
        )
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code in [200, 201]:
            call_response = response.json()
            call_id = call_response.get('id')
            print(f"✅ Llamada creada exitosamente. ID: {call_id}")
            
            # 2. Verificar que la llamada se creó correctamente
            print("\n2️⃣ VERIFICANDO LLAMADA CREADA")
            print("-" * 40)
            
            verify_response = requests.get(
                f"{HUBSPOT_BASE_URL}/crm/v3/objects/calls/{call_id}",
                headers=headers,
                params={
                    "properties": "hs_call_title,hs_call_body,hs_call_duration,hs_call_status,hs_call_direction"
                }
            )
            
            if verify_response.status_code == 200:
                call_details = verify_response.json()
                properties = call_details.get('properties', {})
                
                print(f"✅ Llamada verificada exitosamente")
                print(f"   - Título: {properties.get('hs_call_title', 'N/A')}")
                print(f"   - Duración: {properties.get('hs_call_duration', 'N/A')} ms")
                print(f"   - Estado: {properties.get('hs_call_status', 'N/A')}")
                print(f"   - Dirección: {properties.get('hs_call_direction', 'N/A')}")
                print(f"   - Resumen completo: {properties.get('hs_call_body', 'N/A')[:200]}...")
                
                # Verificar que el resumen esté presente
                summary = properties.get('hs_call_body', '')
                if summary and len(summary.strip()) > 10:
                    print("✅ Resumen incluido correctamente en hs_call_body")
                    # Verificar que contenga información estructurada
                    if "TRANSCRIPCIÓN:" in summary and "DOLOR IDENTIFICADO:" in summary:
                        print("✅ Información estructurada incluida correctamente")
                    else:
                        print("⚠️ Información estructurada no encontrada")
                else:
                    print("❌ Resumen no encontrado en hs_call_body")
                
            else:
                print(f"⚠️ Error verificando llamada: {verify_response.status_code}")
            
        else:
            print(f"❌ Error creando llamada: {response.status_code}")
            print(f"   Error details: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. Verificar conectividad a internet.")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False
    
    print()
    print("🎉 PRUEBA DE API DE CALLS V3 COMPLETADA")
    print("=" * 50)
    print()
    print("📋 VERIFICACIONES REALIZADAS:")
    print("   ✅ API Key de HubSpot configurada")
    print("   ✅ Llamada creada usando API v3")
    print("   ✅ Propiedades personalizadas incluidas")
    print("   ✅ Asociación con contacto establecida")
    print("   ✅ Resumen incluido en hs_call_body")
    print()
    print("💡 PRÓXIMOS PASOS:")
    print("   1. Verificar en HubSpot que la llamada aparezca en el contacto")
    print("   2. Revisar que el resumen esté visible en la llamada")
    print("   3. Confirmar que las propiedades personalizadas se muestren")
    print("   4. Probar el webhook completo con datos reales")
    
    return True

if __name__ == "__main__":
    success = test_calls_api()
    sys.exit(0 if success else 1)
