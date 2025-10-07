#!/usr/bin/env python3
"""
Script para probar solo Apollo con el dominio de Grupo Bios
"""

import requests
import json

# Configuración
BACKEND_URL = "http://localhost:5003"

def test_apollo_grupobios():
    """Prueba solo Apollo para el dominio de Grupo Bios"""
    
    print("🧪 PRUEBA SOLO APOLLO PARA GRUPO BIOS")
    print("=" * 60)
    
    test_data = {
        "domain": "grupobios.co"
    }
    
    try:
        # Verificar que el servidor esté funcionando
        print("🔍 Verificando servidor backend...")
        health_response = requests.get(f"{BACKEND_URL}/health")
        if health_response.status_code == 200:
            print("✅ Servidor backend está funcionando")
        else:
            print("❌ Servidor backend no está respondiendo")
            return False
        
        # Probar Apollo directamente
        print(f"\n🔍 Consultando Apollo para dominio: {test_data['domain']}")
        apollo_response = requests.post(
            f"{BACKEND_URL}/api/test-apollo",
            headers={"Content-Type": "application/json"},
            json=test_data
        )
        
        print(f"📊 Status Code: {apollo_response.status_code}")
        
        if apollo_response.status_code == 200:
            response_data = apollo_response.json()
            print("✅ Consulta a Apollo exitosa")
            
            # Mostrar resumen
            print("\n📋 RESUMEN DE APOLLO:")
            print("-" * 40)
            summary = response_data.get('summary', {})
            print(f"Empresa: {summary.get('company_name', 'N/A')}")
            print(f"Industria: {summary.get('industry', 'N/A')}")
            print(f"Empleados: {summary.get('employees', 'N/A')}")
            print(f"Ingresos: {summary.get('revenue', 'N/A')}")
            print(f"Ubicaciones: {summary.get('locations_count', 'N/A')}")
            print(f"Empleados clave: {summary.get('employees_count', 'N/A')}")
            print(f"Tecnologías: {summary.get('technologies', 'N/A')}")
            
            # Mostrar datos enriquecidos
            enriched_data = response_data.get('enriched_data', {})
            if enriched_data:
                print("\n🏢 INFORMACIÓN DETALLADA DE GRUPO BIOS:")
                print("-" * 50)
                
                company_info = enriched_data.get('informacion_basica', {})
                print(f"Nombre: {company_info.get('nombre', 'N/A')}")
                print(f"Descripción: {company_info.get('descripcion', 'N/A')}")
                print(f"Industria: {company_info.get('industria', 'N/A')}")
                print(f"Tamaño: {company_info.get('tamaño', 'N/A')}")
                print(f"Fundación: {company_info.get('fundacion', 'N/A')}")
                print(f"Sede principal: {company_info.get('sede_principal', 'N/A')}")
                print(f"Sitio web: {company_info.get('sitio_web', 'N/A')}")
                print(f"LinkedIn: {company_info.get('linkedin', 'N/A')}")
                
                # Información financiera
                financial_info = enriched_data.get('financiera', {})
                print(f"\n💰 INFORMACIÓN FINANCIERA:")
                print(f"Ingresos anuales: {financial_info.get('ingresos_anuales', 'N/A')}")
                print(f"Financiación total: {financial_info.get('total_funding', 'N/A')}")
                print(f"Última financiación: {financial_info.get('ultima_financiacion', 'N/A')}")
                
                # Tecnologías
                technologies = financial_info.get('tecnologias', [])
                if technologies:
                    print(f"\n🔧 TECNOLOGÍAS/ENFOQUES:")
                    for i, tech in enumerate(technologies[:15], 1):
                        print(f"  {i}. {tech}")
                
                # Ubicaciones
                locations = enriched_data.get('ubicaciones', [])
                if locations:
                    print(f"\n📍 UBICACIONES:")
                    for i, location in enumerate(locations, 1):
                        print(f"  {i}. {location.get('ciudad', 'N/A')}, {location.get('estado', 'N/A')}, {location.get('pais', 'N/A')}")
                        if location.get('direccion'):
                            print(f"     Dirección: {location['direccion']}")
                
                # Empleados clave
                employees = enriched_data.get('empleados_clave', [])
                if employees:
                    print(f"\n👥 EMPLEADOS CLAVE ({len(employees)}):")
                    for i, emp in enumerate(employees[:10], 1):
                        print(f"  {i}. {emp.get('nombre', 'N/A')}")
                        print(f"     Cargo: {emp.get('cargo', 'N/A')}")
                        if emp.get('email'):
                            print(f"     Email: {emp['email']}")
                        if emp.get('linkedin'):
                            print(f"     LinkedIn: {emp['linkedin']}")
                        print()
                
                # Resumen ejecutivo
                summary_text = enriched_data.get('resumen_ejecutivo', '')
                if summary_text:
                    print(f"\n📝 RESUMEN EJECUTIVO:")
                    print("-" * 30)
                    print(summary_text)
            
            return True
        else:
            print("❌ Error consultando Apollo")
            print(f"Response: {apollo_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor backend")
        print("💡 Asegúrate de que el servidor esté ejecutándose en el puerto 5003")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PRUEBA SOLO APOLLO PARA GRUPO BIOS")
    print("=" * 80)
    
    success = test_apollo_grupobios()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBA")
    print("=" * 80)
    print(f"✅ Apollo para Grupo Bios: {'PASÓ' if success else 'FALLÓ'}")
    
    if success:
        print("\n🎉 ¡Apollo está funcionando correctamente!")
        print("📊 Se obtuvieron datos valiosos sobre Grupo Bios")
    else:
        print("\n❌ La prueba falló. Revisa los logs arriba.")
