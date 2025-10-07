#!/usr/bin/env python3
"""
Script para probar la nueva API Key de HubSpot desde el archivo .env
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_new_hubspot_api_key():
    """Prueba la nueva API Key de HubSpot"""
    
    print("🧪 PRUEBA DE LA NUEVA API KEY DE HUBSPOT")
    print("=" * 60)
    
    # Obtener API Key desde variables de entorno
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    
    if not hubspot_api_key:
        print("❌ No se encontró HUBSPOT_API_KEY en las variables de entorno")
        return False
    
    print(f"🔑 Nueva API Key: {hubspot_api_key[:20]}...{hubspot_api_key[-10:]}")
    
    try:
        # Probar endpoint de contacto por email
        email = "jenny.sichaca@grupobios.co"
        
        url = f"https://api.hubapi.com/crm/v3/objects/contacts/search"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email
                }]
            }],
            "properties": ["id", "email", "firstname", "lastname", "company", "jobtitle"]
        }
        
        print(f"📧 Buscando contacto: {email}")
        print(f"📡 URL: {url}")
        
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                print(f"✅ Contacto encontrado: {len(results)} resultado(s)")
                for contact in results:
                    props = contact.get('properties', {})
                    print(f"  - ID: {contact.get('id')}")
                    print(f"  - Email: {props.get('email')}")
                    print(f"  - Nombre: {props.get('firstname')} {props.get('lastname')}")
                    print(f"  - Empresa: {props.get('company')}")
                    print(f"  - Cargo: {props.get('jobtitle')}")
            else:
                print("⚠️ No se encontró el contacto en HubSpot")
                print("Esto es normal si es un contacto nuevo")
                
        elif response.status_code == 401:
            print("❌ Error de autenticación (401)")
            print("La nueva API Key no es válida o no tiene permisos")
            print(f"Response: {response.text}")
            
        elif response.status_code == 403:
            print("❌ Error de permisos (403)")
            print("La API Key no tiene permisos para acceder a contactos")
            print(f"Response: {response.text}")
            
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_hubspot_contacts_list():
    """Prueba listar contactos para verificar permisos"""
    
    print("\n📋 PROBANDO LISTA DE CONTACTOS")
    print("=" * 50)
    
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    
    try:
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "limit": 5,
            "properties": ["id", "email", "firstname", "lastname", "company"]
        }
        
        print("📋 Listando primeros 5 contactos...")
        
        response = requests.get(url, headers=headers, params=params)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print(f"✅ Se encontraron {len(results)} contactos")
            for i, contact in enumerate(results, 1):
                props = contact.get('properties', {})
                print(f"  {i}. {props.get('firstname', '')} {props.get('lastname', '')} - {props.get('email', '')}")
                if props.get('company'):
                    print(f"     Empresa: {props.get('company')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_create_contact():
    """Prueba crear un contacto de prueba"""
    
    print("\n➕ PROBANDO CREACIÓN DE CONTACTO")
    print("=" * 50)
    
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    
    try:
        url = "https://api.hubapi.com/crm/v3/objects/contacts"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        # Datos de contacto de prueba
        contact_data = {
            "properties": {
                "email": "test.apollo.hubspot@example.com",
                "firstname": "Test",
                "lastname": "Apollo HubSpot",
                "company": "Test Company",
                "jobtitle": "Test Role",
                "lifecyclestage": "lead",
                "hs_lead_status": "NEW"
            }
        }
        
        print("➕ Creando contacto de prueba...")
        
        response = requests.post(url, headers=headers, json=contact_data)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            contact_id = data.get('id')
            print(f"✅ Contacto creado exitosamente")
            print(f"   ID: {contact_id}")
            return True
        elif response.status_code == 409:
            print("⚠️ El contacto ya existe (409)")
            print("Esto indica que la API Key tiene permisos de escritura")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PRUEBA DE LA NUEVA API KEY DE HUBSPOT")
    print("=" * 80)
    
    test1_passed = test_new_hubspot_api_key()
    test2_passed = test_hubspot_contacts_list()
    test3_passed = test_create_contact()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 80)
    print(f"✅ Búsqueda de contacto: {'PASÓ' if test1_passed else 'FALLÓ'}")
    print(f"✅ Lista de contactos: {'PASÓ' if test2_passed else 'FALLÓ'}")
    print(f"✅ Creación de contacto: {'PASÓ' if test3_passed else 'FALLÓ'}")
    
    if test1_passed or test2_passed:
        print("\n🎉 ¡La nueva API Key de HubSpot está funcionando correctamente!")
        print("✅ Puedes proceder con el enriquecimiento completo")
    else:
        print("\n❌ La nueva API Key de HubSpot tiene problemas")
        print("💡 Verifica:")
        print("  - Que la API Key sea válida")
        print("  - Que tenga los permisos necesarios")
        print("  - Que no haya expirado")
