#!/usr/bin/env python3
"""
Script para debuggear el problema de obtención de empresa en HubSpot
"""

import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def debug_company_associations():
    """Debug de las asociaciones de empresa para el contacto"""
    
    print("🔍 DEBUG: ASOCIACIONES DE EMPRESA EN HUBSPOT")
    print("=" * 60)
    
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    contact_id = "140914005589"  # ID de Jenny Sichaca
    
    if not hubspot_api_key:
        print("❌ HUBSPOT_API_KEY no configurada")
        return
    
    try:
        # Obtener asociaciones del contacto con empresas
        url = f"https://api.hubapi.com/crm/v4/objects/contacts/{contact_id}/associations/companies"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"📡 URL: {url}")
        print(f"👤 Contacto ID: {contact_id}")
        
        response = requests.get(url, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            company_associations = data.get('results', [])
            
            print(f"\n📋 ANÁLISIS DE LA RESPUESTA:")
            print(f"  • Número de asociaciones: {len(company_associations)}")
            
            if company_associations:
                print(f"\n🔍 ESTRUCTURA DE LA PRIMERA ASOCIACIÓN:")
                first_association = company_associations[0]
                print(f"  • Tipo: {type(first_association)}")
                print(f"  • Claves disponibles: {list(first_association.keys())}")
                
                for key, value in first_association.items():
                    print(f"  • {key}: {value}")
                
                # Intentar diferentes formas de obtener el ID
                print(f"\n🆔 INTENTANDO OBTENER ID DE EMPRESA:")
                print(f"  • company_associations[0]: {company_associations[0]}")
                
                # Verificar diferentes campos posibles
                possible_id_fields = ['id', 'toObjectId', 'company_id', 'associatedCompanyId']
                for field in possible_id_fields:
                    if field in first_association:
                        print(f"  • {field}: {first_association[field]}")
                    else:
                        print(f"  • {field}: NO ENCONTRADO")
            else:
                print("  • No se encontraron asociaciones de empresa")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_contact_associations_direct():
    """Prueba directa de asociaciones usando la API v3"""
    
    print("\n🔍 DEBUG: ASOCIACIONES USANDO API V3")
    print("=" * 60)
    
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    contact_id = "140914005589"
    
    try:
        # Usar API v3 para obtener asociaciones
        url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/companies"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"📡 URL: {url}")
        
        response = requests.get(url, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def test_companies_search():
    """Buscar empresas que puedan estar asociadas"""
    
    print("\n🔍 DEBUG: BÚSQUEDA DE EMPRESAS")
    print("=" * 60)
    
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    
    try:
        # Buscar empresas que contengan "bios" en el nombre
        url = "https://api.hubapi.com/crm/v3/objects/companies/search"
        
        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "name",
                    "operator": "CONTAINS_TOKEN",
                    "value": "bios"
                }]
            }],
            "properties": ["id", "name", "domain", "industry"],
            "limit": 10
        }
        
        print(f"📡 Buscando empresas con 'bios' en el nombre...")
        
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print(f"📄 Empresas encontradas: {len(results)}")
            for i, company in enumerate(results, 1):
                props = company.get('properties', {})
                print(f"  {i}. ID: {company.get('id')} - Nombre: {props.get('name')} - Dominio: {props.get('domain')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    print("🚀 DEBUG DE PROBLEMA DE EMPRESA EN HUBSPOT")
    print("=" * 80)
    
    debug_company_associations()
    test_contact_associations_direct()
    test_companies_search()
