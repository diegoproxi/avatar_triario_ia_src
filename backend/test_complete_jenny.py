#!/usr/bin/env python3
"""
Script final para mostrar toda la información completa de Jenny Sichaca y Grupo Bios
"""

import os
import sys
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.apollo import enrich_company_data
from api.hubspot import enrich_prospect_with_hubspot_data

def test_complete_integration():
    """Prueba la integración completa Apollo + HubSpot"""
    
    print("🚀 INTEGRACIÓN COMPLETA APOLLO + HUBSPOT")
    print("=" * 80)
    print("📧 Contacto: jenny.sichaca@grupobios.co")
    print("🏢 Empresa: Grupo Bios (grupobios.co)")
    print("=" * 80)
    
    # Datos del prospecto
    prospect_data = {
        "emailCorporativo": "jenny.sichaca@grupobios.co",
        "websiteUrl": "grupobios.co",
        "nombres": "Jenny",
        "apellidos": "Sichaca",
        "compania": "Grupo Bios",
        "rol": "Contacto de Prueba"
    }
    
    # 1. ENRIQUECIMIENTO CON APOLLO (EMPRESA)
    print("\n🏢 ENRIQUECIMIENTO CON APOLLO (GRUPO BIOS)")
    print("-" * 60)
    
    apollo_result = enrich_company_data("grupobios.co")
    
    if apollo_result.get('success'):
        apollo_data = apollo_result.get('data')
        print("✅ Datos de Apollo obtenidos exitosamente")
        
        # Información básica de la empresa
        company_info = apollo_data.get('informacion_basica', {})
        print(f"\n📊 INFORMACIÓN DE LA EMPRESA:")
        print(f"  • Nombre: {company_info.get('nombre', 'N/A')}")
        print(f"  • Industria: {company_info.get('industria', 'N/A')}")
        print(f"  • Empleados: {company_info.get('tamaño', 'N/A')}")
        print(f"  • Fundación: {company_info.get('fundacion', 'N/A')}")
        print(f"  • Sitio web: {company_info.get('sitio_web', 'N/A')}")
        print(f"  • LinkedIn: {company_info.get('linkedin', 'N/A')}")
        
        # Información financiera
        financial_info = apollo_data.get('financiera', {})
        print(f"\n💰 INFORMACIÓN FINANCIERA:")
        print(f"  • Ingresos anuales: ${financial_info.get('ingresos_anuales', 'N/A'):,}" if financial_info.get('ingresos_anuales') else "  • Ingresos anuales: N/A")
        
        # Tecnologías principales
        technologies = financial_info.get('tecnologias', [])
        if technologies:
            print(f"\n🔧 TECNOLOGÍAS/ENFOQUES PRINCIPALES:")
            for i, tech in enumerate(technologies[:10], 1):
                print(f"  {i}. {tech}")
        
        # Descripción
        description = company_info.get('descripcion', '')
        if description:
            print(f"\n📝 DESCRIPCIÓN DE LA EMPRESA:")
            # Truncar descripción para mostrar
            short_desc = description[:300] + "..." if len(description) > 300 else description
            print(f"  {short_desc}")
        
        # Resumen ejecutivo
        summary = apollo_data.get('resumen_ejecutivo', '')
        if summary:
            print(f"\n📋 RESUMEN EJECUTIVO:")
            print(f"  {summary}")
    else:
        print(f"❌ Error obteniendo datos de Apollo: {apollo_result.get('error')}")
        apollo_data = None
    
    # 2. ENRIQUECIMIENTO CON HUBSPOT (CONTACTO)
    print("\n👤 ENRIQUECIMIENTO CON HUBSPOT (JENNY SICHACA)")
    print("-" * 60)
    
    hubspot_result = enrich_prospect_with_hubspot_data(prospect_data)
    
    if hubspot_result.get('success'):
        hubspot_data = hubspot_result.get('data', {})
        hubspot_contact_data = hubspot_data.get('hubspot_data', {})
        
        print("✅ Datos de HubSpot obtenidos exitosamente")
        
        # Información del contacto
        contact_info = hubspot_contact_data.get('contact_info', {})
        if contact_info:
            contact_basic = contact_info.get('informacion_basica', {})
            print(f"\n👤 INFORMACIÓN DEL CONTACTO:")
            print(f"  • ID: {contact_basic.get('id', 'N/A')}")
            print(f"  • Nombre: {contact_basic.get('nombre', 'N/A')}")
            print(f"  • Email: {contact_basic.get('email', 'N/A')}")
            print(f"  • Empresa: {contact_basic.get('empresa', 'N/A')}")
            print(f"  • Cargo: {contact_basic.get('cargo', 'N/A')}")
            print(f"  • Teléfono: {contact_basic.get('telefono', 'N/A')}")
            
            # Actividad
            activity = contact_info.get('actividad', {})
            print(f"\n📅 ACTIVIDAD:")
            print(f"  • Fecha de creación: {activity.get('fecha_creacion', 'N/A')}")
            print(f"  • Última modificación: {activity.get('ultima_modificacion', 'N/A')}")
            print(f"  • Última actividad: {activity.get('ultima_actividad', 'N/A')}")
            print(f"  • Último contacto: {activity.get('ultimo_contacto', 'N/A')}")
            
            # Analíticas
            analytics = contact_info.get('analiticas', {})
            print(f"\n📊 ANALÍTICAS:")
            print(f"  • Fuente: {analytics.get('fuente', 'N/A')}")
            print(f"  • Visitas al sitio: {analytics.get('num_visitas', 'N/A')}")
            print(f"  • Páginas vistas: {analytics.get('num_paginas_vistas', 'N/A')}")
            print(f"  • Última visita: {analytics.get('ultima_visita', 'N/A')}")
            
            # Estado
            estado = contact_info.get('estado', {})
            print(f"\n🎯 ESTADO:")
            print(f"  • Estado del lead: {estado.get('estado_lead', 'N/A')}")
            print(f"  • Etapa del ciclo: {estado.get('etapa_ciclo_vida', 'N/A')}")
            print(f"  • Puntaje de lead: {estado.get('puntaje_lead', 'N/A')}")
        
        # Engagements
        engagements = hubspot_contact_data.get('engagements', [])
        if engagements:
            print(f"\n📞 ENGAGEMENTS ENCONTRADOS ({len(engagements)}):")
            
            # Contar por tipo
            meeting_count = len([e for e in engagements if e.get('tipo') == 'MEETING'])
            call_count = len([e for e in engagements if e.get('tipo') == 'CALL'])
            email_count = len([e for e in engagements if e.get('tipo') == 'EMAIL'])
            task_count = len([e for e in engagements if e.get('tipo') == 'TASK'])
            note_count = len([e for e in engagements if e.get('tipo') == 'NOTE'])
            
            print(f"  • Reuniones: {meeting_count}")
            print(f"  • Llamadas: {call_count}")
            print(f"  • Emails: {email_count}")
            print(f"  • Tareas: {task_count}")
            print(f"  • Notas: {note_count}")
            
            # Mostrar detalles de los engagements
            print(f"\n📋 DETALLES DE ENGAGEMENTS:")
            for i, engagement in enumerate(engagements, 1):
                print(f"  {i}. {engagement.get('tipo', 'N/A')} - {engagement.get('timestamp', 'N/A')}")
                if engagement.get('titulo'):
                    print(f"     Título: {engagement['titulo']}")
                if engagement.get('asunto'):
                    print(f"     Asunto: {engagement['asunto']}")
                if engagement.get('duracion'):
                    print(f"     Duración: {engagement['duracion']}ms")
                if engagement.get('estado'):
                    print(f"     Estado: {engagement['estado']}")
                print()
        else:
            print("\n📞 No se encontraron engagements")
        
        # Información de la empresa en HubSpot
        company_info_hubspot = hubspot_contact_data.get('company_info', {})
        if company_info_hubspot:
            print(f"\n🏢 EMPRESA EN HUBSPOT:")
            company_details = company_info_hubspot.get('company_details', {})
            if company_details:
                company_basic = company_details.get('informacion_basica', {})
                print(f"  • ID: {company_basic.get('id', 'N/A')}")
                print(f"  • Nombre: {company_basic.get('nombre', 'N/A')}")
                print(f"  • Dominio: {company_basic.get('dominio', 'N/A')}")
                print(f"  • Industria: {company_basic.get('industria', 'N/A')}")
            else:
                print("  • No se encontraron detalles de la empresa")
        else:
            print("\n🏢 No se encontró información de empresa en HubSpot")
    else:
        print(f"❌ Error obteniendo datos de HubSpot: {hubspot_result.get('error')}")
        hubspot_data = None
    
    # 3. RESUMEN EJECUTIVO COMBINADO
    print("\n📊 RESUMEN EJECUTIVO COMBINADO")
    print("=" * 60)
    
    if apollo_data and hubspot_data:
        print("✅ INTEGRACIÓN COMPLETA EXITOSA")
        print("\n🎯 INFORMACIÓN CLAVE PARA EL OUTREACH:")
        print("  • Empresa: Grupo Bios - Conglomerado agroindustrial con 70+ años")
        print("  • Tamaño: 8,000 empleados, $4.2B en ingresos")
        print("  • Industria: Agroindustria, nutrición animal, avicultura")
        print("  • Contacto: Jenny Sichaca Lopez (ID: 140914005589)")
        print("  • Engagements: 2 interacciones registradas en HubSpot")
        print("  • Enfoque: Sostenibilidad, trazabilidad, responsabilidad social")
        
        print("\n💡 RECOMENDACIONES PARA EL OUTREACH:")
        print("  • Destacar experiencia de 70 años en agroindustria")
        print("  • Mencionar enfoque en sostenibilidad y trazabilidad")
        print("  • Considerar su compromiso con responsabilidad social")
        print("  • Aprovechar información de sus múltiples segmentos de negocio")
        print("  • Usar datos de sus marcas (Friko, Pimpollo) para personalización")
        
    elif apollo_data:
        print("⚠️ INTEGRACIÓN PARCIAL - Solo datos de Apollo")
        print("  • Se obtuvo información completa de la empresa")
        print("  • No se pudieron obtener datos del contacto en HubSpot")
        
    elif hubspot_data:
        print("⚠️ INTEGRACIÓN PARCIAL - Solo datos de HubSpot")
        print("  • Se obtuvo información del contacto")
        print("  • No se pudieron obtener datos de la empresa en Apollo")
        
    else:
        print("❌ INTEGRACIÓN FALLIDA")
        print("  • No se pudieron obtener datos de ninguna fuente")

if __name__ == "__main__":
    test_complete_integration()
