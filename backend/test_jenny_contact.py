#!/usr/bin/env python3
"""
Script de prueba específico para el contacto de Jenny Sichaca
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BACKEND_URL = "http://localhost:5003"

# Datos del contacto a probar
test_contact = {
    "emailCorporativo": "jenny.sichaca@grupobios.co",
    "websiteUrl": "grupobios.co",
    "nombres": "Jenny",
    "apellidos": "Sichaca",
    "compania": "Grupo Bios",
    "rol": "Contacto de Prueba"
}

def test_jenny_contact():
    """Prueba el enriquecimiento completo para Jenny Sichaca"""
    
    print("🧪 PRUEBA DE ENRIQUECIMIENTO PARA JENNY SICHACA")
    print("=" * 70)
    print(f"📧 Email: {test_contact['emailCorporativo']}")
    print(f"🌐 Dominio: {test_contact['websiteUrl']}")
    print(f"🏢 Empresa: {test_contact['compania']}")
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
        print(f"\n🔄 Iniciando enriquecimiento completo...")
        print(f"📡 Consultando Apollo para dominio: {test_contact['websiteUrl']}")
        print(f"📡 Consultando HubSpot para email: {test_contact['emailCorporativo']}")
        
        enrichment_response = requests.post(
            f"{BACKEND_URL}/api/enrich-prospect",
            headers={"Content-Type": "application/json"},
            json=test_contact
        )
        
        print(f"📊 Status Code: {enrichment_response.status_code}")
        
        if enrichment_response.status_code == 200:
            response_data = enrichment_response.json()
            print("✅ Enriquecimiento exitoso")
            
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
            
            # Mostrar datos de Apollo (empresa)
            apollo_data = response_data.get('apollo_company_data')
            if apollo_data:
                print("\n🏢 DATOS DE APOLLO (GRUPO BIOS):")
                print("-" * 50)
                
                company_info = apollo_data.get('informacion_basica', {})
                print(f"Empresa: {company_info.get('nombre', 'N/A')}")
                print(f"Industria: {company_info.get('industria', 'N/A')}")
                print(f"Empleados: {company_info.get('tamaño', 'N/A')}")
                print(f"Sitio web: {company_info.get('sitio_web', 'N/A')}")
                print(f"LinkedIn: {company_info.get('linkedin', 'N/A')}")
                
                financial_info = apollo_data.get('financiera', {})
                if financial_info.get('ingresos_anuales'):
                    print(f"Ingresos anuales: {financial_info['ingresos_anuales']}")
                if financial_info.get('total_funding'):
                    print(f"Financiación total: {financial_info['total_funding']}")
                
                # Tecnologías
                technologies = financial_info.get('tecnologias', [])
                if technologies:
                    print(f"Tecnologías: {', '.join(technologies[:10])}")
                
                # Ubicaciones
                locations = apollo_data.get('ubicaciones', [])
                if locations:
                    print(f"\n📍 UBICACIONES:")
                    for i, location in enumerate(locations, 1):
                        print(f"  {i}. {location.get('ciudad', 'N/A')}, {location.get('estado', 'N/A')}, {location.get('pais', 'N/A')}")
                
                # Empleados clave
                employees = apollo_data.get('empleados_clave', [])
                if employees:
                    print(f"\n👥 EMPLEADOS CLAVE ENCONTRADOS ({len(employees)}):")
                    for i, emp in enumerate(employees[:5], 1):
                        print(f"  {i}. {emp.get('nombre', 'N/A')} - {emp.get('cargo', 'N/A')}")
                        if emp.get('email'):
                            print(f"     Email: {emp['email']}")
                        if emp.get('linkedin'):
                            print(f"     LinkedIn: {emp['linkedin']}")
            else:
                print("\n⚠️ No se encontraron datos de Apollo para Grupo Bios")
                print("Esto puede significar que:")
                print("- El dominio no está en la base de datos de Apollo")
                print("- La API Key de Apollo no tiene permisos suficientes")
                print("- Hay un error en la configuración de Apollo")
            
            # Mostrar datos de HubSpot (contacto)
            hubspot_data = response_data.get('hubspot_contact_data')
            if hubspot_data:
                print("\n👤 DATOS DE HUBSPOT (JENNY SICHACA):")
                print("-" * 50)
                
                hubspot_contact = hubspot_data.get('hubspot_data', {})
                
                # Información del contacto
                contact_info = hubspot_contact.get('contact_info', {})
                if contact_info:
                    contact_basic = contact_info.get('informacion_basica', {})
                    print(f"ID de Contacto: {contact_basic.get('id', 'N/A')}")
                    print(f"Nombre: {contact_basic.get('nombre', 'N/A')}")
                    print(f"Email: {contact_basic.get('email', 'N/A')}")
                    print(f"Empresa: {contact_basic.get('empresa', 'N/A')}")
                    print(f"Cargo: {contact_basic.get('cargo', 'N/A')}")
                    print(f"Teléfono: {contact_basic.get('telefono', 'N/A')}")
                    
                    # Actividad
                    activity = contact_info.get('actividad', {})
                    print(f"\n📅 ACTIVIDAD:")
                    print(f"Fecha de creación: {activity.get('fecha_creacion', 'N/A')}")
                    print(f"Última modificación: {activity.get('ultima_modificacion', 'N/A')}")
                    print(f"Última actividad: {activity.get('ultima_actividad', 'N/A')}")
                    print(f"Último contacto: {activity.get('ultimo_contacto', 'N/A')}")
                    
                    # Analíticas
                    analytics = contact_info.get('analiticas', {})
                    print(f"\n📊 ANALÍTICAS:")
                    print(f"Fuente: {analytics.get('fuente', 'N/A')}")
                    print(f"Número de visitas: {analytics.get('num_visitas', 'N/A')}")
                    print(f"Páginas vistas: {analytics.get('num_paginas_vistas', 'N/A')}")
                    print(f"Última visita: {analytics.get('ultima_visita', 'N/A')}")
                    
                    # Estado
                    estado = contact_info.get('estado', {})
                    print(f"\n🎯 ESTADO:")
                    print(f"Estado del lead: {estado.get('estado_lead', 'N/A')}")
                    print(f"Etapa del ciclo: {estado.get('etapa_ciclo_vida', 'N/A')}")
                    print(f"Puntaje de lead: {estado.get('puntaje_lead', 'N/A')}")
                
                # Engagements
                engagements = hubspot_contact.get('engagements', [])
                if engagements:
                    print(f"\n📞 ENGAGEMENTS ENCONTRADOS ({len(engagements)}):")
                    print("-" * 40)
                    
                    # Contar por tipo
                    meeting_count = len([e for e in engagements if e.get('tipo') == 'MEETING'])
                    call_count = len([e for e in engagements if e.get('tipo') == 'CALL'])
                    email_count = len([e for e in engagements if e.get('tipo') == 'EMAIL'])
                    task_count = len([e for e in engagements if e.get('tipo') == 'TASK'])
                    note_count = len([e for e in engagements if e.get('tipo') == 'NOTE'])
                    
                    print(f"📅 Reuniones: {meeting_count}")
                    print(f"📞 Llamadas: {call_count}")
                    print(f"📧 Emails: {email_count}")
                    print(f"✅ Tareas: {task_count}")
                    print(f"📝 Notas: {note_count}")
                    
                    # Mostrar los últimos 5 engagements
                    print(f"\n🕒 ÚLTIMOS ENGAGEMENTS:")
                    for i, engagement in enumerate(engagements[:5], 1):
                        print(f"  {i}. {engagement.get('tipo', 'N/A')} - {engagement.get('timestamp', 'N/A')}")
                        if engagement.get('titulo'):
                            print(f"     Título: {engagement['titulo']}")
                        if engagement.get('asunto'):
                            print(f"     Asunto: {engagement['asunto']}")
                        if engagement.get('duracion'):
                            print(f"     Duración: {engagement['duracion']}ms")
                else:
                    print("\n📞 No se encontraron engagements")
                
                # Información de la empresa en HubSpot
                company_info_hubspot = hubspot_contact.get('company_info', {})
                if company_info_hubspot:
                    company_details = company_info_hubspot.get('company_details', {})
                    if company_details:
                        print(f"\n🏢 EMPRESA EN HUBSPOT:")
                        print("-" * 30)
                        
                        company_basic = company_details.get('informacion_basica', {})
                        print(f"ID de Empresa: {company_basic.get('id', 'N/A')}")
                        print(f"Nombre: {company_basic.get('nombre', 'N/A')}")
                        print(f"Dominio: {company_basic.get('dominio', 'N/A')}")
                        print(f"Industria: {company_basic.get('industria', 'N/A')}")
                        print(f"Sitio web: {company_basic.get('sitio_web', 'N/A')}")
                        
                        # Información financiera
                        financial_info = company_details.get('informacion_financiera', {})
                        if financial_info:
                            print(f"\n💰 INFORMACIÓN FINANCIERA:")
                            print(f"Número de empleados: {financial_info.get('num_empleados', 'N/A')}")
                            print(f"Ingresos anuales: {financial_info.get('ingresos_anuales', 'N/A')}")
                            print(f"Ingresos totales: {financial_info.get('ingresos_totales', 'N/A')}")
                        
                        # Negocios
                        deals = company_info_hubspot.get('deals', [])
                        if deals:
                            print(f"\n💼 NEGOCIOS ENCONTRADOS ({len(deals)}):")
                            for i, deal in enumerate(deals[:3], 1):
                                deal_basic = deal.get('informacion_basica', {})
                                print(f"  {i}. {deal_basic.get('nombre', 'N/A')}")
                                print(f"     Monto: {deal_basic.get('monto', 'N/A')}")
                                print(f"     Etapa: {deal_basic.get('etapa', 'N/A')}")
                                print(f"     Fecha de cierre: {deal_basic.get('fecha_cierre', 'N/A')}")
                        else:
                            print("\n💼 No se encontraron negocios")
                    else:
                        print("\n🏢 No se encontró información de empresa")
                else:
                    print("\n🏢 No se encontró información de empresa")
            else:
                print("\n⚠️ No se encontraron datos de HubSpot para Jenny Sichaca")
                print("Esto puede significar que:")
                print("- El contacto no existe en HubSpot")
                print("- La API Key de HubSpot no tiene permisos suficientes")
                print("- Hay un error en la configuración de HubSpot")
            
            return True
        else:
            print("❌ Error en el enriquecimiento")
            print(f"Response: {enrichment_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor backend")
        print("💡 Asegúrate de que el servidor esté ejecutándose en el puerto 5003")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_prospect_creation():
    """Prueba crear el prospecto en HubSpot"""
    
    print("\n🔄 PROBANDO CREACIÓN DE PROSPECTO EN HUBSPOT")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/prospect",
            headers={"Content-Type": "application/json"},
            json=test_contact
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
                print("✅ Apollo: Datos de empresa Grupo Bios enriquecidos")
            if has_hubspot:
                print("✅ HubSpot: Datos de contacto Jenny Sichaca enriquecidos")
            
            return True
        else:
            print("❌ Error creando prospecto")
            print(f"Response: {response.text}")
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
    print("🚀 PRUEBA ESPECÍFICA PARA JENNY SICHACA - GRUPO BIOS")
    print("=" * 80)
    
    # Verificar configuración
    check_configuration()
    
    # Ejecutar pruebas
    print("\n")
    test1_passed = test_jenny_contact()
    test2_passed = test_prospect_creation()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBAS PARA JENNY SICHACA")
    print("=" * 80)
    print(f"✅ Enriquecimiento completo: {'PASÓ' if test1_passed else 'FALLÓ'}")
    print(f"✅ Creación de prospecto: {'PASÓ' if test2_passed else 'FALLÓ'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ¡Pruebas exitosas para Jenny Sichaca!")
        print("🔗 La integración Apollo + HubSpot está funcionando correctamente")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los logs arriba.")
        print("💡 Asegúrate de que las APIs estén configuradas correctamente")
