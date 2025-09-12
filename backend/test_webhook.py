#!/usr/bin/env python3
"""
Script para probar el webhook de tool calls
"""

import requests
import json
import resend

def test_webhook():
    """Prueba el webhook con diferentes tool calls"""
    
    webhook_url = "http://localhost:5003/webhook"
    
    # Test 1: Tool call schedule_meeting
    print("🧪 Probando tool call: schedule_meeting")
    
    payload = {
        "event_type": "conversation.tool_call",
        "properties": {
            "function": {
                "name": "schedule_meeting",
                "arguments": {
                    "email": "diegoalejandro19@gmail.com"
                }
            }
        }
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose?")
        print("Ejecuta: python run.py")
        return
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Tool call no implementada
    print("🧪 Probando tool call: tool_no_existe")
    
    payload2 = {
        "event_type": "conversation.tool_call",
        "properties": {
            "function": {
                "name": "tool_no_existe",
                "arguments": {
                    "param": "valor"
                }
            }
        }
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=payload2,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Evento no reconocido
    print("🧪 Probando evento no reconocido")
    
    payload3 = {
        "event_type": "otro_evento",
        "data": "test"
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=payload3,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health():
    """Prueba el endpoint de health check"""
    
    print("🏥 Probando health check")
    
    try:
        response = requests.get("http://localhost:5003/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":

    resend.api_key = "re_VM2R7H6E_CSDFFLm2unTXp77EzurDy7Lw"

    params: resend.Emails.SendParams = {
    "from": "Acme <diegoalejandro19@gmail.com>",
    "to": ["diegoalejandro19@gmail.com"],
    "subject": "hello world",
    "html": "<p>it works!</p>"
    }

    email = resend.Emails.send(params)
    print(email)


    # print("🚀 Iniciando pruebas del webhook de Tavus")
    # print("="*50)
    
    # # Probar health check primero
    # test_health()
    # print("\n" + "="*50 + "\n")
    
    # # Probar webhook
    # test_webhook()
    
    # print("\n✅ Pruebas completadas")
