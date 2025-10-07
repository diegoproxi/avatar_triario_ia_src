#!/usr/bin/env python3
"""
Script para probar directamente el módulo de HubSpot
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio actual al path para importar el módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.hubspot import get_contact_info

def test_hubspot_module():
    """Prueba el módulo de HubSpot directamente"""
    
    print("🧪 PRUEBA DIRECTA DEL MÓDULO HUBSPOT")
    print("=" * 60)
    
    # Verificar variables de entorno
    hubspot_key = os.getenv('HUBSPOT_API_KEY')
    hubspot_portal = os.getenv('HUBSPOT_PORTAL_ID')
    
    print(f"🔑 API Key: {hubspot_key[:20]}...{hubspot_key[-10:] if hubspot_key else 'NO_CONFIGURADA'}")
    print(f"🏢 Portal ID: {hubspot_portal}")
    
    if not hubspot_key:
        print("❌ HUBSPOT_API_KEY no configurada")
        return False
    
    # Probar búsqueda de contacto
    email = "jenny.sichaca@grupobios.co"
    print(f"\n📧 Buscando contacto: {email}")
    
    try:
        result = get_contact_info(email)
        
        print(f"📊 Resultado: {result.get('success', False)}")
        
        if result.get('success'):
            print("✅ Contacto encontrado exitosamente")
            
            data = result.get('data', {})
            contact_info = data.get('contact_info', {})
            
            if contact_info:
                contact_basic = contact_info.get('informacion_basica', {})
                print(f"  - ID: {contact_basic.get('id', 'N/A')}")
                print(f"  - Nombre: {contact_basic.get('nombre', 'N/A')}")
                print(f"  - Email: {contact_basic.get('email', 'N/A')}")
                print(f"  - Empresa: {contact_basic.get('empresa', 'N/A')}")
                print(f"  - Cargo: {contact_basic.get('cargo', 'N/A')}")
            
            # Engagements
            engagements = data.get('engagements', [])
            print(f"  - Engagements: {len(engagements)}")
            
            # Información de empresa
            company_info = data.get('company_info', {})
            if company_info:
                print(f"  - Empresa asociada: Sí")
                deals = company_info.get('deals', [])
                print(f"  - Negocios: {len(deals)}")
            else:
                print(f"  - Empresa asociada: No")
            
            return True
        else:
            error = result.get('error', 'Error desconocido')
            print(f"❌ Error: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        return False

def test_enrich_prospect_function():
    """Prueba la función de enriquecimiento de prospecto"""
    
    print("\n🔄 PRUEBA DE ENRIQUECIMIENTO DE PROSPECTO")
    print("=" * 60)
    
    from api.hubspot import enrich_prospect_with_hubspot_data
    
    prospect_data = {
        "emailCorporativo": "jenny.sichaca@grupobios.co",
        "nombres": "Jenny",
        "apellidos": "Sichaca",
        "compania": "Grupo Bios",
        "rol": "Contacto de Prueba"
    }
    
    try:
        result = enrich_prospect_with_hubspot_data(prospect_data)
        
        print(f"📊 Resultado: {result.get('success', False)}")
        
        if result.get('success'):
            print("✅ Enriquecimiento exitoso")
            
            data = result.get('data', {})
            hubspot_data = data.get('hubspot_data', {})
            
            if hubspot_data:
                contact_info = hubspot_data.get('contact_info', {})
                if contact_info:
                    contact_basic = contact_info.get('informacion_basica', {})
                    print(f"  - Contacto encontrado: {contact_basic.get('nombre', 'N/A')}")
                
                engagements = hubspot_data.get('engagements', [])
                print(f"  - Engagements: {len(engagements)}")
                
                company_info = hubspot_data.get('company_info', {})
                if company_info:
                    print(f"  - Empresa asociada: Sí")
                else:
                    print(f"  - Empresa asociada: No")
            else:
                print("  - No se encontraron datos de HubSpot")
            
            return True
        else:
            error = result.get('error', 'Error desconocido')
            print(f"❌ Error: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 PRUEBA DIRECTA DEL MÓDULO HUBSPOT")
    print("=" * 80)
    
    test1_passed = test_hubspot_module()
    test2_passed = test_enrich_prospect_function()
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 80)
    print(f"✅ Módulo HubSpot: {'PASÓ' if test1_passed else 'FALLÓ'}")
    print(f"✅ Enriquecimiento: {'PASÓ' if test2_passed else 'FALLÓ'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ¡El módulo HubSpot está funcionando correctamente!")
    else:
        print("\n❌ El módulo HubSpot tiene problemas")
        print("💡 Revisa la configuración y permisos de la API Key")
