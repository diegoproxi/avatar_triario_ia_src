#!/usr/bin/env python3
"""
Script de prueba para crear una llamada con un contacto real de HubSpot
"""

import json
import requests
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_real_contact_call():
    """Prueba la creación de llamadas con un contacto real"""
    
    print("🧪 PRUEBA DE LLAMADA CON CONTACTO REAL")
    print("=" * 50)
    
    # Configuración
    HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
    HUBSPOT_BASE_URL = 'https://api.hubapi.com'
    
    if not HUBSPOT_API_KEY:
        print("❌ HUBSPOT_API_KEY no está configurada")
        print("   Configura la variable de entorno antes de ejecutar la prueba")
        return False
    
    # Buscar un contacto real en HubSpot
    print("1️⃣ BUSCANDO CONTACTO REAL EN HUBSPOT")
    print("-" * 40)
    
    try:
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Buscar contactos existentes
        contacts_response = requests.get(
            f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts",
            headers=headers,
            params={
                "limit": 1,
                "properties": "email,firstname,lastname,company"
            }
        )
        
        if contacts_response.status_code == 200:
            contacts_data = contacts_response.json()
            results = contacts_data.get('results', [])
            
            if results:
                contact = results[0]
                contact_id = contact['id']
                contact_props = contact.get('properties', {})
                
                print(f"✅ Contacto encontrado:")
                print(f"   - ID: {contact_id}")
                print(f"   - Nombre: {contact_props.get('firstname', 'N/A')} {contact_props.get('lastname', 'N/A')}")
                print(f"   - Email: {contact_props.get('email', 'N/A')}")
                print(f"   - Empresa: {contact_props.get('company', 'N/A')}")
                
                # 2. Crear llamada para este contacto
                print("\n2️⃣ CREANDO LLAMADA PARA EL CONTACTO")
                print("-" * 40)
                
                call_data = {
                    "properties": {
                        "hs_timestamp": int(datetime.now().timestamp() * 1000),
                        "hs_call_title": "Conversación con IA - Triario (Prueba)",
                        "hs_call_body": f"""Conversación de prueba con {contact_props.get('firstname', 'Contacto')} {contact_props.get('lastname', '')}

==================================================

RESUMEN:
Se realizó una conversación inicial para evaluar las necesidades del prospecto en cuanto a optimización de procesos de ventas y marketing.

TRANSCRIPCIÓN:
PROSPECTO: Hola, estoy interesado en mejorar nuestros procesos de ventas...
AGENTE: Perfecto, me alegra saber de tu interés. ¿Podrías contarme más sobre los desafíos actuales que enfrentas?

DOLOR IDENTIFICADO: No se en que invierte el tiempo mis vendedores

INSIGHTS CLAVE:
- Prospecto interesado en optimización
- Empresa: {contact_props.get('company', 'No especificada')}
- Cargo: {contact_props.get('jobtitle', 'No especificado')}

PRÓXIMOS PASOS: Agendar reunión de calificación con especialista comercial

PUNTUACIÓN DE CALIFICACIÓN: 7/10

EMPRESA: {contact_props.get('company', 'N/A')}
CARGO: {contact_props.get('jobtitle', 'N/A')}
ID CONVERSACIÓN: test_real_contact_{int(datetime.now().timestamp())}""",
                        "hs_call_duration": 900000,  # 15 minutos
                        "hs_call_status": "COMPLETED",
                        "hs_call_direction": "INBOUND",
                        "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7",  # Connected
                        "hs_call_source": "INTEGRATIONS_PLATFORM"
                    },
                    "associations": [
                        {
                            "to": {
                                "id": contact_id
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
                
                print(f"📤 Enviando llamada para contacto {contact_id}...")
                
                call_response = requests.post(
                    f"{HUBSPOT_BASE_URL}/crm/v3/objects/calls",
                    headers=headers,
                    json=call_data,
                    timeout=30
                )
                
                print(f"📥 Status Code: {call_response.status_code}")
                
                if call_response.status_code in [200, 201]:
                    call_data_response = call_response.json()
                    call_id = call_data_response.get('id')
                    print(f"✅ Llamada creada exitosamente. ID: {call_id}")
                    
                    # 3. Verificar la llamada
                    print("\n3️⃣ VERIFICANDO LLAMADA CREADA")
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
                        
                        print(f"✅ Llamada verificada:")
                        print(f"   - Título: {properties.get('hs_call_title', 'N/A')}")
                        print(f"   - Estado: {properties.get('hs_call_status', 'N/A')}")
                        print(f"   - Duración: {properties.get('hs_call_duration', 'N/A')} ms")
                        print(f"   - Dirección: {properties.get('hs_call_direction', 'N/A')}")
                        
                        # Verificar el resumen
                        summary = properties.get('hs_call_body', '')
                        if summary and len(summary.strip()) > 50:
                            print("✅ Resumen incluido correctamente")
                            print(f"   - Longitud del resumen: {len(summary)} caracteres")
                            print(f"   - Contiene transcripción: {'✅' if 'TRANSCRIPCIÓN:' in summary else '❌'}")
                            print(f"   - Contiene dolor: {'✅' if 'DOLOR IDENTIFICADO:' in summary else '❌'}")
                            print(f"   - Contiene insights: {'✅' if 'INSIGHTS CLAVE:' in summary else '❌'}")
                        else:
                            print("❌ Resumen no encontrado o muy corto")
                    
                    print(f"\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
                    print(f"   - Contacto ID: {contact_id}")
                    print(f"   - Llamada ID: {call_id}")
                    print(f"   - Puedes verificar en HubSpot: https://app.hubspot.com/contacts/711526/contact/{contact_id}")
                    
                    return True
                    
                else:
                    print(f"❌ Error creando llamada: {call_response.status_code}")
                    print(f"   Error: {call_response.text}")
                    return False
            else:
                print("❌ No se encontraron contactos en HubSpot")
                print("   Crea al menos un contacto en HubSpot antes de ejecutar esta prueba")
                return False
        else:
            print(f"❌ Error buscando contactos: {contacts_response.status_code}")
            print(f"   Error: {contacts_response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_real_contact_call()
    sys.exit(0 if success else 1)
