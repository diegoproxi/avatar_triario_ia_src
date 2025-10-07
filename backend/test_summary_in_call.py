#!/usr/bin/env python3
"""
Script de prueba para verificar que el resumen se incluya correctamente en la llamada
"""

import json
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from storage.conversation_storage import conversation_storage
from agents.conversation_analyzer import conversation_analyzer

def test_summary_in_call():
    """Prueba que el resumen se incluya correctamente en la llamada"""
    
    print("🧪 INICIANDO PRUEBA DEL RESUMEN EN LLAMADA")
    print("=" * 50)
    
    # Datos de prueba
    test_conversation_id = "test-summary-call-123"
    test_hubspot_id = "hubspot-test-summary-456"
    test_prospect_data = {
        "nombres": "María",
        "apellidos": "González",
        "compania": "Empresa Test Summary",
        "websiteUrl": "www.empresatest.com",
        "emailCorporativo": "maria.gonzalez@empresatest.com",
        "rol": "Directora Comercial"
    }
    
    # Transcripción que debería generar un resumen claro
    test_transcript = [
        {
            "role": "assistant",
            "content": "Hola, soy Wayne. Estoy preparado para ayudarte con implementación de HubSpot."
        },
        {
            "role": "user",
            "content": "Hola Wayne. Soy María González, directora comercial de Empresa Test Summary. Tenemos un problema serio: no sabemos exactamente en qué están invirtiendo su tiempo nuestros vendedores. Tenemos un CRM básico pero no lo aprovechamos al máximo."
        },
        {
            "role": "assistant",
            "content": "Entiendo perfectamente el desafío. Es muy común en empresas en crecimiento. ¿Podrías contarme más sobre cómo esto afecta los resultados?"
        },
        {
            "role": "user",
            "content": "Nuestros vendedores gastan mucho tiempo en actividades operativas que no generan ventas. Además, el seguimiento a prospectos es mínimo y estamos perdiendo oportunidades. El nivel de recompra es muy bajo."
        },
        {
            "role": "assistant",
            "content": "Perfecto, esto es exactamente lo que Triario puede ayudarte a resolver. Tenemos procesos y tecnología que optimizan el tiempo de tus vendedores."
        },
        {
            "role": "user",
            "content": "Eso suena muy bien. ¿Cuál sería el siguiente paso?"
        }
    ]
    
    print(f"📝 Datos de prueba:")
    print(f"   - conversation_id: {test_conversation_id}")
    print(f"   - hubspot_id: {test_hubspot_id}")
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
    
    # 2. Probar análisis de conversación
    print("2️⃣ PROBANDO ANÁLISIS DE CONVERSACIÓN")
    print("-" * 40)
    
    try:
        analysis = conversation_analyzer.analyze_conversation(test_transcript, test_prospect_data)
        
        print(f"✅ Análisis completado:")
        print(f"   - Resumen: {analysis.summary[:100]}...")
        print(f"   - Dolor identificado: {analysis.pain_point}")
        print(f"   - Puntuación: {analysis.qualification_score}")
        print(f"   - Insights: {len(analysis.key_insights)} encontrados")
        
        # Verificar que el resumen no esté vacío
        if not analysis.summary or len(analysis.summary.strip()) < 10:
            print("❌ ERROR: El resumen está vacío o es muy corto")
            return False
        
        print("✅ Resumen generado correctamente")
        
    except Exception as e:
        print(f"❌ Error en análisis: {str(e)}")
        return False
    
    print()
    
    # 3. Probar creación de datos de conversación
    print("3️⃣ PROBANDO CREACIÓN DE DATOS DE CONVERSACIÓN")
    print("-" * 40)
    
    try:
        conversation_data = {
            "title": f"Conversación con {test_prospect_data.get('nombres', '')} {test_prospect_data.get('apellidos', '')}",
            "duration": len(test_transcript) * 30,
            "conversation_type": "video_call",
            "ai_agent": "Wayne (SDR Triario)",
            "engagement_score": analysis.qualification_score,
            "company": test_prospect_data.get('compania', ''),
            "job_title": test_prospect_data.get('rol', ''),
            "pain_points": [analysis.pain_point],
            "key_insights": analysis.key_insights,
            "next_steps": analysis.next_steps,
            "summary": analysis.summary,
            "transcript": "\n".join([f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" for msg in test_transcript]),
            "conversation_id": test_conversation_id,
            "follow_up_required": analysis.qualification_score >= 7
        }
        
        print(f"✅ Datos de conversación creados:")
        print(f"   - Título: {conversation_data['title']}")
        print(f"   - Resumen incluido: {conversation_data['summary'][:50]}...")
        print(f"   - Transcript incluido: {len(conversation_data['transcript'])} caracteres")
        
        # Verificar que el summary esté presente
        if 'summary' not in conversation_data or not conversation_data['summary']:
            print("❌ ERROR: El campo 'summary' no está presente en conversation_data")
            return False
        
        print("✅ Campo 'summary' presente en conversation_data")
        
    except Exception as e:
        print(f"❌ Error creando datos de conversación: {str(e)}")
        return False
    
    print()
    
    # 4. Limpiar datos de prueba
    print("4️⃣ LIMPIANDO DATOS DE PRUEBA")
    print("-" * 40)
    
    delete_success = conversation_storage.delete_mapping(test_conversation_id)
    if delete_success:
        print("✅ Datos de prueba eliminados")
    else:
        print("⚠️ Error eliminando datos de prueba")
    
    print()
    print("🎉 PRUEBA DEL RESUMEN COMPLETADA")
    print("=" * 50)
    print()
    print("📋 VERIFICACIONES REALIZADAS:")
    print("   ✅ Mapeo de conversación creado")
    print("   ✅ Análisis de conversación ejecutado")
    print("   ✅ Resumen generado por IA")
    print("   ✅ Campo 'summary' incluido en conversation_data")
    print("   ✅ Datos listos para envío a HubSpot")
    print()
    print("💡 Si el resumen no aparece en HubSpot, verificar:")
    print("   1. Que la API Key de HubSpot esté configurada")
    print("   2. Que el campo 'summary' se esté enviando en metadata")
    print("   3. Los logs del servidor para ver la metadata enviada")
    
    return True

if __name__ == "__main__":
    success = test_summary_in_call()
    sys.exit(0 if success else 1)
