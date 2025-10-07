#!/usr/bin/env python3
"""
Script de prueba para el webhook de transcripciones
"""

import json
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from storage.conversation_storage import conversation_storage

def test_transcript_webhook():
    """Prueba el webhook con datos de transcripción simulados"""
    
    print("🧪 INICIANDO PRUEBA DEL WEBHOOK DE TRANSCRIPCIONES")
    print("=" * 60)
    
    # Datos de prueba
    test_conversation_id = "r92debe21318"
    test_hubspot_id = "hubspot-test-12345"
    test_prospect_data = {
        "nombres": "Alexander",
        "apellidos": "Arango",
        "compania": "Azimut",
        "websiteUrl": "www.azimutenergia.co",
        "emailCorporativo": "alexander.arango@azimut.co",
        "rol": "Comercial"
    }
    
    # Simular transcripción de conversación
    test_transcript = [
        {
            "role": "system",
            "content": "You are in a live video conference call with a user..."
        },
        {
            "role": "assistant",
            "content": "Hola, soy Wayne. Estoy preparado para ayudarte en cualquier inquietud que tengas sobre implementación de Hubspot en tus procesos de ventas, marketing y servicio."
        },
        {
            "role": "user",
            "content": "Hola, Wayne. Soy el director comercial de una compañía que se llama Simut. Hoy estamos enfrentando un desafío muy grande en la generación de demanda y me dijeron que Triario de pronto era la compañía que me podía ayudar a resolver ese problema."
        },
        {
            "role": "assistant",
            "content": "¡Claro! Entiendo que estás enfrentando desafíos en la generación de demanda y estás explorando cómo Triario podría ayudar. Para que podamos evaluar mejor si Triario es la solución ideal para tus necesidades, necesitaré que completes un formulario en la pantalla."
        },
        {
            "role": "user",
            "content": "Datos del prospecto: {\"nombres\":\"Alexander\",\"apellidos\":\"Arango\",\"compania\":\"Azimut\",\"websiteUrl\":\"www.azimutenergia.co\",\"emailCorporativo\":\"alexander.arango@azimut.co\",\"rol\":\"Comercial\"}"
        },
        {
            "role": "assistant",
            "content": "Gracias, Alexander. Con la información que has proporcionado, ahora procederemos a entender un poco más sobre tu negocio y tus desafíos actuales en la generación de demanda."
        },
        {
            "role": "user",
            "content": "El problema principal es que no sabemos exactamente en qué están invirtiendo su tiempo nuestros vendedores. Tenemos un CRM básico pero no lo estamos aprovechando al máximo. El seguimiento a los prospectos es muy mínimo y creo que estamos perdiendo muchas oportunidades."
        },
        {
            "role": "assistant",
            "content": "Entiendo perfectamente el desafío que describes. Es muy común en empresas en crecimiento tener estos problemas de visibilidad y seguimiento. ¿Podrías contarme más sobre cómo esto está afectando los resultados de ventas?"
        },
        {
            "role": "user",
            "content": "Nuestros vendedores gastan mucho tiempo en actividades operativas que no generan ventas directamente. Además, el nivel de recompra de nuestros clientes es muy bajo porque no tenemos un seguimiento adecuado post-venta."
        },
        {
            "role": "assistant",
            "content": "Perfecto, esto es exactamente lo que Triario puede ayudarte a resolver. Tenemos procesos y tecnología que pueden optimizar el tiempo de tus vendedores y mejorar significativamente el seguimiento y la recompra."
        }
    ]
    
    # Preparar datos del webhook
    webhook_data = {
        "replica_id": test_conversation_id,
        "transcript": test_transcript
    }
    
    print(f"📝 Datos de prueba:")
    print(f"   - conversation_id: {test_conversation_id}")
    print(f"   - hubspot_id: {test_hubspot_id}")
    print(f"   - prospect_data: {json.dumps(test_prospect_data, indent=2)}")
    print(f"   - transcript_length: {len(test_transcript)} mensajes")
    print()
    
    # 1. Crear mapeo en el almacenamiento
    print("1️⃣ CREANDO MAPEO EN ALMACENAMIENTO")
    print("-" * 40)
    
    storage_success = conversation_storage.store_mapping(
        conversation_id=test_conversation_id,
        hubspot_id=test_hubspot_id,
        prospect_data=test_prospect_data
    )
    
    if storage_success:
        print("✅ Mapeo creado exitosamente")
    else:
        print("❌ Error creando mapeo")
        return False
    
    print()
    
    # 2. Enviar webhook al backend
    print("2️⃣ ENVIANDO WEBHOOK AL BACKEND")
    print("-" * 40)
    
    backend_url = "http://localhost:5003/webhook"
    
    try:
        print(f"🌐 Enviando a: {backend_url}")
        print(f"📤 Datos: {json.dumps(webhook_data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(
            backend_url,
            headers={"Content-Type": "application/json"},
            json=webhook_data,
            timeout=30
        )
        
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('status') == 'success':
                print("✅ Webhook procesado exitosamente")
                
                # Mostrar análisis
                analysis = response_data.get('analysis', {})
                print(f"   - Resumen: {analysis.get('summary', 'N/A')[:100]}...")
                print(f"   - Dolor identificado: {analysis.get('pain_point', 'N/A')}")
                print(f"   - Puntuación de calificación: {analysis.get('qualification_score', 'N/A')}")
                print(f"   - Confianza en dolor: {analysis.get('pain_confidence', 'N/A')}")
                
                # Mostrar actualizaciones
                updates = response_data.get('updates', {})
                print(f"   - Campo dolor actualizado: {updates.get('pain_field_updated', False)}")
                print(f"   - Llamada creada: {updates.get('call_created', False)}")
                print(f"   - ID de llamada: {updates.get('call_id', 'N/A')}")
                
            else:
                print(f"⚠️ Respuesta con estado: {response_data.get('status')}")
                print(f"   Mensaje: {response_data.get('message', 'N/A')}")
        else:
            print(f"❌ Error en webhook: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al backend")
        print("   Asegúrate de que el servidor esté ejecutándose en localhost:5003")
        return False
    except Exception as e:
        print(f"❌ Error enviando webhook: {str(e)}")
        return False
    
    print()
    
    # 3. Limpiar datos de prueba
    print("3️⃣ LIMPIANDO DATOS DE PRUEBA")
    print("-" * 40)
    
    delete_success = conversation_storage.delete_mapping(test_conversation_id)
    if delete_success:
        print("✅ Datos de prueba eliminados")
    else:
        print("⚠️ Error eliminando datos de prueba")
    
    print()
    print("🎉 PRUEBA DEL WEBHOOK COMPLETADA")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_transcript_webhook()
    sys.exit(0 if success else 1)
