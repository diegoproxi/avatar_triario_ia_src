#!/usr/bin/env python3
"""
Script para mostrar logs detallados del enriquecimiento de datos desde Apollo API
Este script demuestra qué información específica trae Apollo para diferentes empresas
"""

import os
import sys
import json
import logging
from datetime import datetime

# Agregar el directorio backend al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.apollo import enrich_company_data

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('apollo_detailed_logs.log')
    ]
)

logger = logging.getLogger(__name__)

def print_separator(title):
    """Imprime un separador visual para las secciones"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_json_pretty(data, title="Datos JSON"):
    """Imprime datos JSON de forma legible"""
    print(f"\n--- {title} ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_apollo_enrichment(domain, company_name=""):
    """
    Prueba el enriquecimiento de datos de Apollo para un dominio específico
    
    Args:
        domain (str): Dominio de la empresa
        company_name (str): Nombre de la empresa (opcional)
    """
    
    print_separator(f"ENRIQUECIMIENTO DE DATOS - {company_name or domain}")
    
    logger.info(f"🚀 Iniciando enriquecimiento para dominio: {domain}")
    print(f"🔍 Consultando Apollo API para: {domain}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Realizar la consulta a Apollo
    result = enrich_company_data(domain)
    
    print_separator("RESULTADO DE LA CONSULTA")
    
    if result.get('success'):
        print("✅ ÉXITO: Datos enriquecidos obtenidos correctamente")
        
        # Mostrar datos procesados
        enriched_data = result.get('data', {})
        print_separator("DATOS PROCESADOS Y ESTRUCTURADOS")
        
        # Información básica
        basic_info = enriched_data.get('informacion_basica', {})
        if basic_info:
            print("\n📊 INFORMACIÓN BÁSICA DE LA EMPRESA:")
            for key, value in basic_info.items():
                if value:
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Información de contacto
        contact_info = enriched_data.get('contacto', {})
        if contact_info:
            print("\n📞 INFORMACIÓN DE CONTACTO:")
            for key, value in contact_info.items():
                if value:
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Información financiera
        financial_info = enriched_data.get('financiera', {})
        if financial_info:
            print("\n💰 INFORMACIÓN FINANCIERA:")
            for key, value in financial_info.items():
                if value:
                    if key == 'tecnologias' and isinstance(value, list):
                        print(f"  • {key.replace('_', ' ').title()}: {', '.join(value[:10])}")  # Primeras 10
                    else:
                        print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        # Ubicaciones
        locations = enriched_data.get('ubicaciones', [])
        if locations:
            print("\n🌍 UBICACIONES:")
            for i, location in enumerate(locations, 1):
                location_str = f"  {i}. "
                if location.get('ciudad'):
                    location_str += location['ciudad']
                if location.get('estado'):
                    location_str += f", {location['estado']}"
                if location.get('pais'):
                    location_str += f", {location['pais']}"
                if location.get('direccion'):
                    location_str += f" - {location['direccion']}"
                print(location_str)
        
        # Empleados clave
        employees = enriched_data.get('empleados_clave', [])
        if employees:
            print("\n👥 EMPLEADOS CLAVE:")
            for i, employee in enumerate(employees, 1):
                if employee.get('nombre'):
                    employee_str = f"  {i}. {employee['nombre']}"
                    if employee.get('cargo'):
                        employee_str += f" - {employee['cargo']}"
                    if employee.get('departamento'):
                        employee_str += f" ({employee['departamento']})"
                    if employee.get('email'):
                        employee_str += f" - {employee['email']}"
                    print(employee_str)
        
        # Resumen ejecutivo
        if enriched_data.get('resumen_ejecutivo'):
            print("\n📝 RESUMEN EJECUTIVO:")
            print(f"  {enriched_data['resumen_ejecutivo']}")
        
        # Mostrar datos raw de Apollo
        raw_data = result.get('raw_data', {})
        if raw_data:
            print_separator("DATOS RAW DE APOLLO API")
            print("📋 Esta es la respuesta completa que devuelve Apollo API:")
            print_json_pretty(raw_data, "Respuesta completa de Apollo")
            
            # Análisis detallado de la respuesta
            print_separator("ANÁLISIS DETALLADO DE LA RESPUESTA")
            
            organization = raw_data.get('organization', {})
            if organization:
                print("\n🏢 CAMPOS DISPONIBLES EN 'organization':")
                for key, value in organization.items():
                    if value:
                        if isinstance(value, (list, dict)):
                            print(f"  • {key}: {type(value).__name__} con {len(value) if hasattr(value, '__len__') else 'N/A'} elementos")
                        else:
                            print(f"  • {key}: {value}")
            
            people = raw_data.get('people', [])
            if people:
                print(f"\n👤 EMPLEADOS ENCONTRADOS: {len(people)}")
                for i, person in enumerate(people[:3], 1):  # Mostrar solo los primeros 3
                    print(f"  {i}. {person.get('first_name', '')} {person.get('last_name', '')} - {person.get('title', '')}")
            
            # Mostrar todos los campos disponibles
            print("\n🔍 TODOS LOS CAMPOS DISPONIBLES EN LA RESPUESTA:")
            all_fields = set()
            def extract_fields(obj, prefix=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        field_name = f"{prefix}.{key}" if prefix else key
                        all_fields.add(field_name)
                        if isinstance(value, (dict, list)):
                            extract_fields(value, field_name)
                elif isinstance(obj, list) and obj:
                    extract_fields(obj[0], prefix)
            
            extract_fields(raw_data)
            for field in sorted(all_fields):
                print(f"  • {field}")
    
    else:
        print("❌ ERROR: No se pudieron obtener datos enriquecidos")
        print(f"   Código de error: {result.get('code', 'N/A')}")
        print(f"   Mensaje: {result.get('error', 'N/A')}")
        logger.error(f"Error en enriquecimiento: {result.get('error')}")
    
    print_separator("FIN DEL ENRIQUECIMIENTO")
    return result

def main():
    """Función principal para ejecutar las pruebas"""
    
    print_separator("SCRIPT DE LOGS DETALLADOS DE APOLLO API")
    print("Este script muestra información detallada sobre el enriquecimiento de datos")
    print("desde Apollo API para diferentes empresas.")
    
    # Lista de dominios para probar
    test_domains = [
        ("google.com", "Google"),
        ("microsoft.com", "Microsoft"),
        ("apple.com", "Apple"),
        ("openai.com", "OpenAI"),
        ("anthropic.com", "Anthropic"),
        ("github.com", "GitHub"),
        ("stackoverflow.com", "Stack Overflow"),
        ("salesforce.com", "Salesforce"),
        ("hubspot.com", "HubSpot"),
        ("apollo.io", "Apollo")
    ]
    
    print(f"\n📋 Se probarán {len(test_domains)} dominios:")
    for domain, name in test_domains:
        print(f"  • {name} ({domain})")
    
    # Preguntar al usuario qué dominios probar
    print("\n¿Qué dominios quieres probar?")
    print("1. Todos los dominios")
    print("2. Solo los primeros 3")
    print("3. Dominio personalizado")
    print("4. Solo Apollo (para ver la respuesta completa)")
    
    try:
        choice = input("\nIngresa tu opción (1-4): ").strip()
        
        if choice == "1":
            domains_to_test = test_domains
        elif choice == "2":
            domains_to_test = test_domains[:3]
        elif choice == "3":
            custom_domain = input("Ingresa el dominio (ej: example.com): ").strip()
            custom_name = input("Ingresa el nombre de la empresa (opcional): ").strip()
            domains_to_test = [(custom_domain, custom_name or custom_domain)]
        elif choice == "4":
            domains_to_test = [("apollo.io", "Apollo")]
        else:
            print("Opción inválida, probando solo Apollo...")
            domains_to_test = [("apollo.io", "Apollo")]
        
        # Ejecutar las pruebas
        results = []
        for domain, name in domains_to_test:
            result = test_apollo_enrichment(domain, name)
            results.append((domain, name, result))
            
            # Pausa entre consultas para no sobrecargar la API
            if len(domains_to_test) > 1:
                input("\n⏸️  Presiona Enter para continuar con el siguiente dominio...")
        
        # Resumen final
        print_separator("RESUMEN FINAL")
        print(f"📊 Total de dominios probados: {len(results)}")
        
        successful = sum(1 for _, _, result in results if result.get('success'))
        failed = len(results) - successful
        
        print(f"✅ Exitosos: {successful}")
        print(f"❌ Fallidos: {failed}")
        
        if successful > 0:
            print("\n🎯 DOMINIOS EXITOSOS:")
            for domain, name, result in results:
                if result.get('success'):
                    enriched_data = result.get('data', {})
                    basic_info = enriched_data.get('informacion_basica', {})
                    company_name = basic_info.get('nombre', name)
                    industry = basic_info.get('industria', 'N/A')
                    size = basic_info.get('tamaño', 'N/A')
                    print(f"  • {company_name} ({domain}) - {industry} - {size} empleados")
        
        if failed > 0:
            print("\n⚠️  DOMINIOS FALLIDOS:")
            for domain, name, result in results:
                if not result.get('success'):
                    error = result.get('error', 'Error desconocido')
                    print(f"  • {name} ({domain}) - {error}")
        
        print(f"\n📝 Logs detallados guardados en: apollo_detailed_logs.log")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando las pruebas: {str(e)}")
        logger.error(f"Error en main: {str(e)}")

if __name__ == "__main__":
    main()
