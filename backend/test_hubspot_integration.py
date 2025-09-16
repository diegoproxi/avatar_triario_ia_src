#!/usr/bin/env python3
"""
Script de prueba para la integración con HubSpot CRM
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
BACKEND_URL = "http://localhost:5003"
API_ENDPOINT = f"{BACKEND_URL}/api/prospect"

# Datos de prueba
test_prospect_data = {
    "nombres": "Juan",
    "apellidos": "Pérez",
    "compania": "Empresa de Prueba S.A.",
    "websiteUrl": "https://www.empresadeprueba.com",
    "emailCorporativo": "juan.perez@empresadeprueba.com",
    "rol": "Gerente de Ventas"
}

def test_hubspot_integration():
    """Prueba la integración con HubSpot"""
    
    print("🧪 Iniciando prueba de integración con HubSpot CRM...")
    print(f"📡 Endpoint: {API_ENDPOINT}")
    print(f"📊 Datos de prueba: {json.dumps(test_prospect_data, indent=2)}")
    print("-" * 50)
    
    try:
        # Verificar que el servidor esté funcionando
        health_response = requests.get(f"{BACKEND_URL}/health")
        if health_response.status_code == 200:
            print("✅ Servidor backend está funcionando")
        else:
            print("❌ Servidor backend no está respondiendo")
            return False
        
        # Enviar datos del prospecto
        print("\n📤 Enviando datos del prospecto...")
        response = requests.post(
            API_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=test_prospect_data
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Prospecto creado exitosamente en HubSpot")
            return True
        else:
            print("❌ Error creando prospecto en HubSpot")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor backend")
        print("💡 Asegúrate de que el servidor esté ejecutándose en el puerto 5003")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_validation():
    """Prueba la validación de campos requeridos"""
    
    print("\n🧪 Probando validación de campos requeridos...")
    
    # Datos incompletos
    incomplete_data = {
        "nombres": "Juan",
        "apellidos": "Pérez",
        # Faltan campos requeridos
    }
    
    try:
        response = requests.post(
            API_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=incomplete_data
        )
        
        if response.status_code == 400:
            print("✅ Validación funcionando correctamente")
            print(f"📄 Error esperado: {response.json()}")
            return True
        else:
            print("❌ La validación no está funcionando correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de validación: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de integración HubSpot CRM")
    print("=" * 60)
    
    # Verificar configuración
    hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
    if hubspot_api_key:
        print("✅ HUBSPOT_API_KEY configurada")
    else:
        print("⚠️  HUBSPOT_API_KEY no configurada - se usará modo simulación")
    
    # Ejecutar pruebas
    test1_passed = test_hubspot_integration()
    test2_passed = test_validation()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"✅ Integración HubSpot: {'PASÓ' if test1_passed else 'FALLÓ'}")
    print(f"✅ Validación de campos: {'PASÓ' if test2_passed else 'FALLÓ'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los logs arriba.")
