#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de HubSpot
"""

def test_hubspot_api():
    """Prueba la API de HubSpot directamente"""
    
    print("🧪 PRUEBA DIRECTA DE LA API DE HUBSPOT")
    print("=" * 60)
    
    # API Key de HubSpot desde el archivo .env
    from dotenv import load_dotenv
    import os
    load_dotenv()
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    
    if not hubspot_api_key:
        print("❌ Error: HUBSPOT_API_KEY no encontrada en variables de entorno")
        print("Asegúrate de tener un archivo .env con HUBSPOT_API_KEY configurada")
        return
    
    print(f"✅ API Key encontrada: {hubspot_api_key[:10]}...")
    
    try:
        # Probar endpoint de contacto por email
        email = "jenny.sichaca@grupobios.co"
        
        url = f"https://api.hubapi.com/crm/v3/objects/contacts/search"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email
                        }
                    ]
                }
            ],
            "properties": ["email", "firstname", "lastname", "company", "phone"]
        }
        
        print(f"🔍 Buscando contacto: {email}")
        print(f"📡 URL: {url}")
        
        import requests
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            contacts = data.get('results', [])
            
            if contacts:
                contact = contacts[0]
                print("✅ Contacto encontrado:")
                print(f"   📧 Email: {contact.get('properties', {}).get('email', 'N/A')}")
                print(f"   👤 Nombre: {contact.get('properties', {}).get('firstname', 'N/A')} {contact.get('properties', {}).get('lastname', 'N/A')}")
                print(f"   🏢 Empresa: {contact.get('properties', {}).get('company', 'N/A')}")
                print(f"   📞 Teléfono: {contact.get('properties', {}).get('phone', 'N/A')}")
                print(f"   🆔 ID: {contact.get('id', 'N/A')}")
            else:
                print("⚠️  No se encontró el contacto")
        else:
            print(f"❌ Error en la respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_hubspot_contacts_list():
    """Prueba listar contactos para verificar permisos"""
    
    print("\n📋 PROBANDO LISTA DE CONTACTOS")
    print("=" * 50)
    
    from dotenv import load_dotenv
    import os
    load_dotenv()
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    
    if not hubspot_api_key:
        print("❌ Error: HUBSPOT_API_KEY no encontrada en variables de entorno")
        return
    
    try:
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "limit": 5,
            "properties": ["email", "firstname", "lastname"]
        }
        
        print("📡 Solicitando lista de contactos...")
        
        import requests
        response = requests.get(url, headers=headers, params=params)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            contacts = data.get('results', [])
            
            print(f"✅ Encontrados {len(contacts)} contactos:")
            for contact in contacts:
                props = contact.get('properties', {})
                print(f"   📧 {props.get('email', 'N/A')} - {props.get('firstname', 'N/A')} {props.get('lastname', 'N/A')}")
        else:
            print(f"❌ Error en la respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_hubspot_api()
    test_hubspot_contacts_list()