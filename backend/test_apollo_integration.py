#!/usr/bin/env python3
"""
Script para probar la integración con Apollo API usando el dominio triario.com
"""

import requests
import json
import sys
import os
from datetime import datetime

# Configuración
BACKEND_URL = "http://localhost:5003"
DOMAIN_TO_TEST = "triario.com"

def print_separator(title=""):
    """Imprime un separador visual"""
    print("\n" + "="*60)
    if title:
        print(f" {title}")
        print("="*60)

def test_apollo_direct():
    """Prueba directa de Apollo API"""
    print_separator("PRUEBA DIRECTA DE APOLLO API")
    
    apollo_url = "https://api.apollo.io/api/v1/organizations/enrich"
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'x-api-key': 'ATpjar6DGtZOKVJWSTiGXQ'
    }
    
    params = {'domain': DOMAIN_TO_TEST}
    
    print(f"🔍 Consultando Apollo API para dominio: {DOMAIN_TO_TEST}")
    print(f"📡 URL: {apollo_url}")
    
    try:
        response = requests.get(apollo_url, headers=headers, params=params, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa de Apollo API")
            
            # Mostrar información básica
            org = data.get('organization', {})
            print(f"\n📋 INFORMACIÓN BÁSICA:")
            print(f"   Nombre: {org.get('name', 'N/A')}")
            print(f"   Descripción: {org.get('short_description', 'N/A')}")
            print(f"   Industria: {org.get('industry', 'N/A')}")
            print(f"   Empleados: {org.get('estimated_num_employees', 'N/A')}")
            print(f"   Sitio web: {org.get('website_url', 'N/A')}")
            
            # Mostrar tecnologías si están disponibles
            keywords = org.get('keywords', [])
            if keywords:
                print(f"   Tecnologías: {', '.join(keywords[:10])}")
            
            # Mostrar empleados si están disponibles
            people = data.get('people', [])
            if people:
                print(f"\n👥 EMPLEADOS ENCONTRADOS: {len(people)}")
                for i, person in enumerate(people[:3]):
                    name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
                    title = person.get('title', 'N/A')
                    print(f"   {i+1}. {name} - {title}")
            
            return data
        else:
            print(f"❌ Error de Apollo API: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout consultando Apollo API")
        return None
    except Exception as e:
        print(f"💥 Error consultando Apollo API: {str(e)}")
        return None

def test_backend_enrich_context():
    """Prueba el endpoint de enriquecimiento de contexto del backend"""
    print_separator("PRUEBA ENDPOINT BACKEND - ENRICH CONTEXT")
    
    url = f"{BACKEND_URL}/api/enrich-context"
    payload = {
        "websiteUrl": DOMAIN_TO_TEST,
        "nombres": "Juan",
        "apellidos": "Pérez",
        "compania": "Triario",
        "emailCorporativo": "juan@triario.com",
        "rol": "CEO"
    }
    
    print(f"🔍 Consultando backend: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa del backend")
            
            if data.get('status') == 'success':
                print("\n📋 CONTEXTO GENERADO:")
                print("-" * 40)
                print(data.get('context', ''))
                print("-" * 40)
                
                # Mostrar datos enriquecidos estructurados
                enriched_data = data.get('enriched_data', {})
                if enriched_data:
                    print("\n🏢 DATOS ESTRUCTURADOS:")
                    company_info = enriched_data.get('informacion_basica', {})
                    if company_info:
                        print(f"   Nombre: {company_info.get('nombre', 'N/A')}")
                        print(f"   Industria: {company_info.get('industria', 'N/A')}")
                        print(f"   Tamaño: {company_info.get('tamaño', 'N/A')}")
                    
                    financial_info = enriched_data.get('financiera', {})
                    if financial_info.get('tecnologias'):
                        print(f"   Tecnologías: {', '.join(financial_info['tecnologias'][:5])}")
                
                return data
            else:
                print(f"❌ Error en respuesta: {data.get('message', 'Unknown error')}")
                return None
        else:
            print(f"❌ Error del backend: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("🔌 Error de conexión - ¿Está el backend ejecutándose?")
        return None
    except Exception as e:
        print(f"💥 Error consultando backend: {str(e)}")
        return None

def test_backend_prospect_with_enrichment():
    """Prueba el endpoint de prospecto con enriquecimiento"""
    print_separator("PRUEBA ENDPOINT BACKEND - PROSPECT CON ENRIQUECIMIENTO")
    
    url = f"{BACKEND_URL}/api/prospect"
    payload = {
        "nombres": "Juan",
        "apellidos": "Pérez",
        "compania": "Triario",
        "websiteUrl": DOMAIN_TO_TEST,
        "emailCorporativo": "juan@triario.com",
        "rol": "CEO"
    }
    
    print(f"🔍 Consultando backend: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa del backend")
            
            if data.get('status') == 'success':
                print(f"\n📋 RESULTADO:")
                print(f"   HubSpot ID: {data.get('hubspot_id', 'N/A')}")
                print(f"   Mensaje: {data.get('message', 'N/A')}")
                
                # Mostrar si se incluyeron datos enriquecidos
                enriched_data = data.get('enriched_company_data')
                if enriched_data:
                    print("✅ Datos enriquecidos incluidos en la respuesta")
                    
                    company_info = enriched_data.get('informacion_basica', {})
                    if company_info.get('nombre'):
                        print(f"   Empresa enriquecida: {company_info['nombre']}")
                    if company_info.get('industria'):
                        print(f"   Industria: {company_info['industria']}")
                else:
                    print("⚠️ No se incluyeron datos enriquecidos")
                
                return data
            else:
                print(f"❌ Error en respuesta: {data.get('message', 'Unknown error')}")
                return None
        else:
            print(f"❌ Error del backend: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("🔌 Error de conexión - ¿Está el backend ejecutándose?")
        return None
    except Exception as e:
        print(f"💥 Error consultando backend: {str(e)}")
        return None

def test_backend_health():
    """Prueba el endpoint de salud del backend"""
    print_separator("PRUEBA HEALTH CHECK")
    
    url = f"{BACKEND_URL}/health"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend está funcionando")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Service: {data.get('service', 'N/A')}")
            return True
        else:
            print(f"❌ Backend no responde correctamente: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("🔌 Backend no está ejecutándose")
        return False
    except Exception as e:
        print(f"💥 Error consultando health check: {str(e)}")
        return False

def main():
    """Función principal del script de pruebas"""
    print_separator("SCRIPT DE PRUEBAS - APOLLO API INTEGRATION")
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Dominio a probar: {DOMAIN_TO_TEST}")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    
    results = {
        'apollo_direct': False,
        'backend_health': False,
        'backend_enrich': False,
        'backend_prospect': False
    }
    
    # 1. Probar Apollo API directamente
    apollo_data = test_apollo_direct()
    if apollo_data:
        results['apollo_direct'] = True
    
    # 2. Probar health check del backend
    if test_backend_health():
        results['backend_health'] = True
        
        # 3. Probar endpoint de enriquecimiento
        enrich_data = test_backend_enrich_context()
        if enrich_data:
            results['backend_enrich'] = True
        
        # 4. Probar endpoint de prospecto con enriquecimiento
        prospect_data = test_backend_prospect_with_enrichment()
        if prospect_data:
            results['backend_prospect'] = True
    else:
        print("\n⚠️ Saltando pruebas de backend - servidor no disponible")
        print("💡 Para ejecutar el backend: python run.py")
    
    # Resumen final
    print_separator("RESUMEN DE PRUEBAS")
    
    tests = [
        ("Apollo API Directa", results['apollo_direct']),
        ("Backend Health Check", results['backend_health']),
        ("Endpoint Enrich Context", results['backend_enrich']),
        ("Endpoint Prospect + Enrichment", results['backend_prospect'])
    ]
    
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\n📊 RESULTADO FINAL: {total_passed}/{total_tests} pruebas exitosas")
    
    if total_passed == total_tests:
        print("🎉 ¡Todas las pruebas pasaron! La integración está funcionando correctamente.")
    elif results['apollo_direct']:
        print("✅ Apollo API funciona correctamente")
        if not results['backend_health']:
            print("💡 Para probar la integración completa, ejecuta el backend: python run.py")
    else:
        print("❌ Hay problemas con la integración que necesitan ser resueltos")
    
    print_separator()

if __name__ == "__main__":
    main()
