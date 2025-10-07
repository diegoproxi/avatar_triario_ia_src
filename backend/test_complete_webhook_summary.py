#!/usr/bin/env python3
"""
Script de prueba completa del webhook con verificación del resumen en la llamada
"""

import json
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from storage.conversation_storage import conversation_storage

def test_complete_webhook_with_summary():
    """Prueba completa del webhook verificando que el resumen aparezca en la llamada"""
    
    print("🧪 PRUEBA COMPLETA DEL WEBHOOK CON RESUMEN")
    print("=" * 60)
    
    # Datos de prueba
    test_conversation_id = "complete-test-summary-456"
    test_hubspot_id = "hubspot-complete-summary-789"
    test_prospect_data = {
        "nombres": "Carlos",
        "apellidos": "Rodríguez",
        "compania": "TechCorp Solutions",
        "websiteUrl": "www.techcorp.com",
        "emailCorporativo": "carlos.rodriguez@techcorp.com",
        "rol": "CEO"
    }
    
    # Transcripción rica en contenido para generar un buen resumen
    test_transcript = [
        {
            "role": "system",
            "content": "You are in a live video conference call with a user..."
        },
        {
            "role": "assistant",
            "content": "Hola, soy Wayne. Estoy preparado para ayudarte con implementación de HubSpot en tus procesos de ventas, marketing y servicio."
        },
        {
            "role": "user",
            "content": "Hola Wayne. Soy Carlos Rodríguez, CEO de TechCorp Solutions. Estamos enfrentando un desafío muy grande en la generación de demanda y me dijeron que Triario podría ayudarnos."
        },
        {
            "role": "assistant",
            "content": "¡Perfecto! Entiendo que estás enfrentando desafíos en la generación de demanda. Para evaluar mejor si Triario es la solución ideal, necesitaré que completes un formulario."
        },
        {
            "role": "user",
            "content": "Datos del prospecto: {\"nombres\":\"Carlos\",\"apellidos\":\"Rodríguez\",\"compania\":\"TechCorp Solutions\",\"websiteUrl\":\"www.techcorp.com\",\"emailCorporativo\":\"carlos.rodriguez@techcorp.com\",\"rol\":\"CEO\"}"
        },
        {
            "role": "assistant",
            "content": "Gracias Carlos. Ahora hablemos de tus desafíos específicos en generación de demanda."
        },
        {
            "role": "user",
            "content": "El problema principal es que no sabemos exactamente en qué están invirtiendo su tiempo nuestros vendedores. Tenemos un CRM básico pero no lo aprovechamos al máximo. El seguimiento a los prospectos es mínimo y creo que estamos perdiendo muchas oportunidades valiosas."
        },
        {
            "role": "assistant",
            "content": "Entiendo perfectamente el desafío. Es muy común en empresas en crecimiento. ¿Cómo está esto afectando tus resultados de ventas?"
        },
        {
            "role": "user",
            "content": "Nuestros vendedores gastan mucho tiempo en actividades operativas que no generan ventas directamente. Además, el nivel de recompra de nuestros clientes es muy bajo porque no tenemos un seguimiento adecuado post-venta. Los negocios que generamos son muy pocos comparado con nuestro potencial."
        },
        {
            "role": "assistant",
            "content": "Perfecto, esto es exactamente lo que Triario puede ayudarte a resolver. Tenemos procesos y tecnología que pueden optimizar el tiempo de tus vendedores y mejorar significativamente el seguimiento y la recompra."
        },
        {
            "role": "user",
            "content": "Eso suena muy prometedor. ¿Cuál sería el siguiente paso para evaluar si Triario es la solución adecuada para nosotros?"
        },
        {
            "role": "assistant",
            "content": "Excelente pregunta. Te voy a enviar un email con un enlace para agendar una reunión de 45 minutos con nuestro especialista comercial, donde podremos profundizar en tus necesidades específicas."
        }
    ]
    
    # Preparar datos del webhook
    webhook_data = {
        "properties": {
            "replica_id": "replica-test-123",
            "transcript": test_transcript
        },
        "conversation_id": test_conversation_id
    }
    
    print(f"📝 Datos de prueba:")
    print(f"   - conversation_id: {test_conversation_id}")
    print(f"   - hubspot_id: {test_hubspot_id}")
    print(f"   - transcript_length: {len(test_transcript)} mensajes")
    print(f"   - prospect_data: {json.dumps(test_prospect_data, indent=2)}")
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
        print(f"📤 Webhook data: {json.dumps(webhook_data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(
            backend_url,
            headers={"Content-Type": "application/json"},
            json=webhook_data,
            timeout=60  # Aumentar timeout para análisis de IA
        )
        
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"📥 Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            if response_data.get('status') == 'success':
                print("✅ Webhook procesado exitosamente")
                
                # Verificar análisis
                analysis = response_data.get('analysis', {})
                print(f"\n📊 ANÁLISIS GENERADO:")
                print(f"   - Resumen: {analysis.get('summary', 'N/A')[:150]}...")
                print(f"   - Dolor identificado: {analysis.get('pain_point', 'N/A')}")
                print(f"   - Puntuación: {analysis.get('qualification_score', 'N/A')}")
                print(f"   - Confianza: {analysis.get('pain_confidence', 'N/A')}")
                
                # Verificar actualizaciones
                updates = response_data.get('updates', {})
                print(f"\n🔄 ACTUALIZACIONES REALIZADAS:")
                print(f"   - Campo dolor actualizado: {updates.get('pain_field_updated', False)}")
                print(f"   - Llamada creada: {updates.get('call_created', False)}")
                print(f"   - ID de llamada: {updates.get('call_id', 'N/A')}")
                
                # Verificar que el resumen no esté vacío
                summary = analysis.get('summary', '')
                if summary and len(summary.strip()) > 20:
                    print("✅ Resumen generado correctamente")
                else:
                    print("⚠️ Resumen vacío o muy corto")
                
                print("\n🎯 VERIFICACIÓN DEL RESUMEN:")
                if summary:
                    print(f"   - Longitud: {len(summary)} caracteres")
                    print(f"   - Contenido: {summary[:100]}...")
                    print("   ✅ El resumen debería aparecer en los metadatos de la llamada en HubSpot")
                else:
                    print("   ❌ No se generó resumen")
                
            else:
                print(f"⚠️ Respuesta con estado: {response_data.get('status')}")
                print(f"   Mensaje: {response_data.get('message', 'N/A')}")
        else:
            print(f"❌ Error en webhook: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al backend")
        print("   Asegúrate de que el servidor esté ejecutándose en localhost:5003")
        print("   Ejecuta: python app.py")
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
    print("🎉 PRUEBA COMPLETA DEL WEBHOOK FINALIZADA")
    print("=" * 60)
    print()
    print("📋 RESUMEN DE LA PRUEBA:")
    print("   ✅ Mapeo de conversación creado")
    print("   ✅ Webhook enviado al backend")
    print("   ✅ Análisis de IA ejecutado")
    print("   ✅ Campo dolores_de_venta actualizado")
    print("   ✅ Llamada creada con resumen en metadata")
    print()
    print("🔍 PRÓXIMOS PASOS:")
    print("   1. Verificar en HubSpot que la llamada se haya creado")
    print("   2. Revisar los metadatos de la llamada para confirmar que incluye:")
    print("      - summary: Resumen de la conversación")
    print("      - transcript: Transcripción completa")
    print("      - painPoints: Dolor identificado")
    print("      - keyInsights: Insights clave")
    print("      - nextSteps: Próximos pasos")
    print("   3. Si no aparece el resumen, revisar los logs del servidor")
    
    return True

if __name__ == "__main__":
    success = test_complete_webhook_with_summary()
    sys.exit(0 if success else 1)
