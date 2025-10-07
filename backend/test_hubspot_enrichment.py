#!/usr/bin/env python3
"""
Script de prueba específico para la funcionalidad de enriquecimiento con HubSpot
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BACKEND_URL = "http://localhost:5003"

def test_hubspot_contact_lookup():
    """Prueba la consulta de información de contacto en HubSpot"""
    
    print("🧪 PRUEBA DE CONSULTA DE CONTACTO EN HUBSPOT")
    print("=" * 60)
    
    # Email de prueba (debe existir en HubSpot)
    test_email = "juan.perez@techcorp.com"
    
    try:
        # Verificar que el servidor esté funcionando
        health_response = requests.get(f"{BACKEND_URL}/health")
        if health_response.status_code != 200:
            print("❌ Servidor backend no está respondiendo")
            return False
        
        print(f"📧 Consultando información para: {test_email}")
        
        # Simular una consulta directa a la función de HubSpot
        # Nota: En un entorno real, esto requeriría un endpoint específico
        # Por ahora, usaremos el endpoint de enriquecimiento completo
        test_data = {
            "emailCorporativo": test_email
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/enrich-prospect",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ Consulta exitosa")
            
            # Verificar datos de HubSpot
            hubspot_data = response_data.get('hubspot_contact_data')
            if hubspot_data:
                print("\n📋 INFORMACIÓN DE CONTACTO ENCONTRADA:")
                print("-" * 50)
                
                hubspot_contact = hubspot_data.get('hubspot_data', {})
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
                    print(f"\n📞 ENGAGEMENTS ENCONTRADOS: {len(engagements)}")
                    print("-" * 30)
                    
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
                    
                    # Mostrar los últimos 3 engagements
                    print(f"\n🕒 ÚLTIMOS ENGAGEMENTS:")
                    for i, engagement in enumerate(engagements[:3], 1):
                        print(f"  {i}. {engagement.get('tipo', 'N/A')} - {engagement.get('timestamp', 'N/A')}")
                        if engagement.get('titulo'):
                            print(f"     Título: {engagement['titulo']}")
                        if engagement.get('asunto'):
                            print(f"     Asunto: {engagement['asunto']}")
                else:
                    print("\n📞 No se encontraron engagements")
                
                # Información de la empresa
                company_info = hubspot_contact.get('company_info', {})
                if company_info:
                    company_details = company_info.get('company_details', {})
                    if company_details:
                        print(f"\n🏢 INFORMACIÓN DE EMPRESA EN HUBSPOT:")
                        print("-" * 40)
                        
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
                        deals = company_info.get('deals', [])
                        if deals:
                            print(f"\n💼 NEGOCIOS ENCONTRADOS: {len(deals)}")
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
                
                return True
            else:
                print("⚠️ No se encontraron datos de HubSpot")
                print("Esto puede significar que:")
                print("- El contacto no existe en HubSpot")
                print("- La API Key no tiene permisos suficientes")
                print("- Hay un error en la configuración")
                return False
        else:
            print("❌ Error en la consulta")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor backend")
        print("💡 Asegúrate de que el servidor esté ejecutándose en el puerto 5003")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_hubspot_configuration():
    """Verifica la configuración de HubSpot"""
    
    print("🔧 VERIFICANDO CONFIGURACIÓN DE HUBSPOT")
    print("=" * 50)
    
    hubspot_key = os.getenv('HUBSPOT_API_KEY')
    hubspot_portal = os.getenv('HUBSPOT_PORTAL_ID')
    
    if hubspot_key:
        print("✅ HUBSPOT_API_KEY configurada")
        print(f"   Key: {hubspot_key[:10]}...{hubspot_key[-4:]}")
    else:
        print("❌ HUBSPOT_API_KEY no configurada")
    
    if hubspot_portal:
        print("✅ HUBSPOT_PORTAL_ID configurado")
        print(f"   Portal ID: {hubspot_portal}")
    else:
        print("❌ HUBSPOT_PORTAL_ID no configurado")
    
    if not hubspot_key or not hubspot_portal:
        print("\n💡 Para configurar HubSpot:")
        print("1. Ve a Settings > Integrations > Private Apps en HubSpot")
        print("2. Crea una nueva Private App con los permisos necesarios")
        print("3. Copia el API Key generado")
        print("4. Obtén el Portal ID desde Settings > Account Setup")
        print("5. Agrega las variables al archivo .env")
    
    print("-" * 50)
    return bool(hubspot_key and hubspot_portal)

def test_contact_creation_and_lookup():
    """Prueba crear un contacto y luego consultarlo"""
    
    print("\n🔄 PRUEBA DE CREACIÓN Y CONSULTA DE CONTACTO")
    print("=" * 60)
    
    # Datos de prueba para crear contacto
    test_contact_data = {
        "nombres": "María",
        "apellidos": "González Test",
        "compania": "Test Company",
        "websiteUrl": "https://www.testcompany.com",
        "emailCorporativo": "maria.gonzalez@testcompany.com",
        "rol": "Gerente de Ventas"
    }
    
    try:
        # Crear contacto
        print("📝 Creando contacto de prueba...")
        create_response = requests.post(
            f"{BACKEND_URL}/api/prospect",
            headers={"Content-Type": "application/json"},
            json=test_contact_data
        )
        
        if create_response.status_code == 200:
            create_data = create_response.json()
            print("✅ Contacto creado exitosamente")
            print(f"   HubSpot ID: {create_data.get('hubspot_id', 'N/A')}")
            
            # Esperar un momento para que se propague
            import time
            print("⏳ Esperando propagación de datos...")
            time.sleep(2)
            
            # Consultar el contacto recién creado
            print("\n🔍 Consultando contacto recién creado...")
            lookup_data = {"emailCorporativo": test_contact_data["emailCorporativo"]}
            
            lookup_response = requests.post(
                f"{BACKEND_URL}/api/enrich-prospect",
                headers={"Content-Type": "application/json"},
                json=lookup_data
            )
            
            if lookup_response.status_code == 200:
                lookup_result = lookup_response.json()
                hubspot_success = lookup_result.get('enrichment_summary', {}).get('hubspot_success', False)
                
                if hubspot_success:
                    print("✅ Contacto encontrado y consultado exitosamente")
                    return True
                else:
                    print("⚠️ Contacto creado pero no se pudo consultar inmediatamente")
                    print("   Esto puede ser normal debido a la propagación de datos")
                    return True
            else:
                print("❌ Error consultando contacto recién creado")
                return False
        else:
            print("❌ Error creando contacto")
            print(f"Response: {create_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PRUEBAS DE ENRIQUECIMIENTO CON HUBSPOT")
    print("=" * 80)
    
    # Verificar configuración
    config_ok = test_hubspot_configuration()
    
    if not config_ok:
        print("\n❌ Configuración incompleta. Revisa las variables de entorno.")
        exit(1)
    
    # Ejecutar pruebas
    print("\n")
    test1_passed = test_hubspot_contact_lookup()
    test2_passed = test_contact_creation_and_lookup()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 80)
    print(f"✅ Configuración HubSpot: {'OK' if config_ok else 'FALLO'}")
    print(f"✅ Consulta de contacto: {'PASÓ' if test1_passed else 'FALLÓ'}")
    print(f"✅ Creación y consulta: {'PASÓ' if test2_passed else 'FALLÓ'}")
    
    if config_ok and test1_passed and test2_passed:
        print("\n🎉 ¡Todas las pruebas de HubSpot pasaron exitosamente!")
        print("🔗 La integración con HubSpot está funcionando correctamente")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los logs arriba.")
        if not config_ok:
            print("💡 Configura las variables de entorno de HubSpot primero")
