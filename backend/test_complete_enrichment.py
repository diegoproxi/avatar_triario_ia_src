#!/usr/bin/env python3
"""
Script de prueba para la integración completa Apollo + HubSpot
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BACKEND_URL = "http://localhost:5003"

# Datos de prueba
test_prospect_data = {
    "nombres": "Juan Carlos",
    "apellidos": "Pérez García",
    "compania": "TechCorp Solutions",
    "websiteUrl": "https://www.techcorp.com",
    "emailCorporativo": "juan.perez@techcorp.com",
    "rol": "Director de Tecnología"
}

def test_complete_enrichment():
    """Prueba el enriquecimiento completo con Apollo y HubSpot"""
    
    print("🧪 PRUEBA DE ENRIQUECIMIENTO COMPLETO APOLLO + HUBSPOT")
    print("=" * 70)
    print(f"📡 Backend URL: {BACKEND_URL}")
    print(f"📊 Datos de prueba: {json.dumps(test_prospect_data, indent=2, ensure_ascii=False)}")
    print("-" * 70)
    
    try:
        # Verificar que el servidor esté funcionando
        print("🔍 Verificando servidor backend...")
        health_response = requests.get(f"{BACKEND_URL}/health")
        if health_response.status_code == 200:
            print("✅ Servidor backend está funcionando")
        else:
            print("❌ Servidor backend no está respondiendo")
            return False
        
        # Probar enriquecimiento completo
        print("\n🔄 Probando enriquecimiento completo...")
        enrichment_response = requests.post(
            f"{BACKEND_URL}/api/enrich-prospect",
            headers={"Content-Type": "application/json"},
            json=test_prospect_data
        )
        
        print(f"📊 Status Code: {enrichment_response.status_code}")
        
        if enrichment_response.status_code == 200:
            response_data = enrichment_response.json()
            print("✅ Enriquecimiento completo exitoso")
            
            # Mostrar resumen
            print("\n📋 RESUMEN DEL ENRIQUECIMIENTO:")
            print("-" * 50)
            summary = response_data.get('enrichment_summary', {})
            print(f"✅ Apollo éxito: {summary.get('apollo_success', False)}")
            print(f"✅ HubSpot éxito: {summary.get('hubspot_success', False)}")
            print(f"📊 Datos de empresa: {summary.get('has_company_data', False)}")
            print(f"👤 Datos de contacto: {summary.get('has_contact_data', False)}")
            print(f"📞 Engagements: {summary.get('has_engagements', False)}")
            print(f"💰 Negocios: {summary.get('has_company_deals', False)}")
            
            # Mostrar resumen ejecutivo combinado
            print("\n📝 RESUMEN EJECUTIVO COMBINADO:")
            print("-" * 50)
            combined_summary = response_data.get('combined_executive_summary', '')
            print(combined_summary)
            
            # Mostrar detalles de Apollo si están disponibles
            if response_data.get('apollo_company_data'):
                print("\n🏢 DATOS DE APOLLO (EMPRESA):")
                print("-" * 50)
                apollo_data = response_data['apollo_company_data']
                company_info = apollo_data.get('informacion_basica', {})
                print(f"Empresa: {company_info.get('nombre', 'N/A')}")
                print(f"Industria: {company_info.get('industria', 'N/A')}")
                print(f"Empleados: {company_info.get('tamaño', 'N/A')}")
                print(f"Sitio web: {company_info.get('sitio_web', 'N/A')}")
                
                financial_info = apollo_data.get('financiera', {})
                if financial_info.get('ingresos_anuales'):
                    print(f"Ingresos anuales: {financial_info['ingresos_anuales']}")
                
                employees = apollo_data.get('empleados_clave', [])
                if employees:
                    print(f"Empleados clave encontrados: {len(employees)}")
                    for i, emp in enumerate(employees[:3], 1):
                        print(f"  {i}. {emp.get('nombre', 'N/A')} - {emp.get('cargo', 'N/A')}")
            
            # Mostrar detalles de HubSpot si están disponibles
            if response_data.get('hubspot_contact_data'):
                print("\n👤 DATOS DE HUBSPOT (CONTACTO):")
                print("-" * 50)
                hubspot_data = response_data['hubspot_contact_data']
                hubspot_contact = hubspot_data.get('hubspot_data', {})
                
                # Información del contacto
                contact_info = hubspot_contact.get('contact_info', {})
                if contact_info:
                    contact_basic = contact_info.get('informacion_basica', {})
                    print(f"Contacto ID: {contact_basic.get('id', 'N/A')}")
                    print(f"Email: {contact_basic.get('email', 'N/A')}")
                    print(f"Teléfono: {contact_basic.get('telefono', 'N/A')}")
                    
                    # Actividad
                    activity = contact_info.get('actividad', {})
                    if activity.get('ultima_actividad'):
                        print(f"Última actividad: {activity['ultima_actividad']}")
                    
                    # Analíticas
                    analytics = contact_info.get('analiticas', {})
                    if analytics.get('num_visitas'):
                        print(f"Visitas al sitio: {analytics['num_visitas']}")
                    if analytics.get('num_paginas_vistas'):
                        print(f"Páginas vistas: {analytics['num_paginas_vistas']}")
                
                # Engagements
                engagements = hubspot_contact.get('engagements', [])
                if engagements:
                    print(f"\n📞 ENGAGEMENTS ENCONTRADOS: {len(engagements)}")
                    meeting_count = len([e for e in engagements if e.get('tipo') == 'MEETING'])
                    call_count = len([e for e in engagements if e.get('tipo') == 'CALL'])
                    email_count = len([e for e in engagements if e.get('tipo') == 'EMAIL'])
                    
                    if meeting_count > 0:
                        print(f"  📅 Reuniones: {meeting_count}")
                    if call_count > 0:
                        print(f"  📞 Llamadas: {call_count}")
                    if email_count > 0:
                        print(f"  📧 Emails: {email_count}")
                
                # Información de la empresa en HubSpot
                company_info_hubspot = hubspot_contact.get('company_info', {})
                if company_info_hubspot:
                    company_details = company_info_hubspot.get('company_details', {})
                    if company_details:
                        company_basic = company_details.get('informacion_basica', {})
                        print(f"\n🏢 EMPRESA EN HUBSPOT:")
                        print(f"Empresa ID: {company_basic.get('id', 'N/A')}")
                        print(f"Nombre: {company_basic.get('nombre', 'N/A')}")
                        print(f"Dominio: {company_basic.get('dominio', 'N/A')}")
                        
                        # Negocios
                        deals = company_info_hubspot.get('deals', [])
                        if deals:
                            print(f"Negocios encontrados: {len(deals)}")
                            for i, deal in enumerate(deals[:3], 1):
                                deal_basic = deal.get('informacion_basica', {})
                                print(f"  {i}. {deal_basic.get('nombre', 'N/A')} - ${deal_basic.get('monto', 'N/A')}")
            
            return True
        else:
            print("❌ Error en enriquecimiento completo")
            print(f"📄 Response: {enrichment_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor backend")
        print("💡 Asegúrate de que el servidor esté ejecutándose en el puerto 5003")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_prospect_creation():
    """Prueba la creación de prospecto con enriquecimiento integrado"""
    
    print("\n🔄 PROBANDO CREACIÓN DE PROSPECTO CON ENRIQUECIMIENTO INTEGRADO")
    print("=" * 70)
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/prospect",
            headers={"Content-Type": "application/json"},
            json=test_prospect_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ Prospecto creado exitosamente")
            
            # Verificar si se incluyeron datos enriquecidos
            has_apollo = 'apollo_company_data' in response_data
            has_hubspot = 'hubspot_contact_data' in response_data
            
            print(f"📊 Datos de Apollo incluidos: {has_apollo}")
            print(f"👤 Datos de HubSpot incluidos: {has_hubspot}")
            
            if has_apollo:
                print("✅ Apollo: Datos de empresa enriquecidos")
            if has_hubspot:
                print("✅ HubSpot: Datos de contacto enriquecidos")
            
            return True
        else:
            print("❌ Error creando prospecto")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def check_configuration():
    """Verifica la configuración de las APIs"""
    
    print("🔧 VERIFICANDO CONFIGURACIÓN DE APIs")
    print("=" * 50)
    
    # Verificar Apollo
    apollo_key = os.getenv('APOLLO_API_KEY')
    if apollo_key:
        print("✅ APOLLO_API_KEY configurada")
    else:
        print("⚠️  APOLLO_API_KEY no configurada")
    
    # Verificar HubSpot
    hubspot_key = os.getenv('HUBSPOT_API_KEY')
    if hubspot_key:
        print("✅ HUBSPOT_API_KEY configurada")
    else:
        print("⚠️  HUBSPOT_API_KEY no configurada")
    
    hubspot_portal = os.getenv('HUBSPOT_PORTAL_ID')
    if hubspot_portal:
        print("✅ HUBSPOT_PORTAL_ID configurado")
    else:
        print("⚠️  HUBSPOT_PORTAL_ID no configurado")
    
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE INTEGRACIÓN COMPLETA APOLLO + HUBSPOT")
    print("=" * 80)
    
    # Verificar configuración
    check_configuration()
    
    # Ejecutar pruebas
    print("\n")
    test1_passed = test_complete_enrichment()
    test2_passed = test_prospect_creation()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 80)
    print(f"✅ Enriquecimiento completo: {'PASÓ' if test1_passed else 'FALLÓ'}")
    print(f"✅ Creación de prospecto: {'PASÓ' if test2_passed else 'FALLÓ'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("🔗 La integración Apollo + HubSpot está funcionando correctamente")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los logs arriba.")
        print("💡 Asegúrate de que las APIs estén configuradas correctamente")
