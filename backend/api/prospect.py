import json
import os
import requests

def handler(request):
    # Configurar CORS
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }
    
    # Manejar preflight OPTIONS
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }
    
    try:
        # Solo procesar POST
        if request.method != "POST":
            return {
                "statusCode": 405,
                "headers": headers,
                "body": json.dumps({"error": "Method not allowed"})
            }
        
        # Obtener datos del body
        data = request.json if hasattr(request, 'json') else json.loads(request.body)
        
        # Validar datos requeridos
        required_fields = ['nombres', 'apellidos', 'compania', 'emailCorporativo', 'rol']
        for field in required_fields:
            if not data.get(field):
                return {
                    "statusCode": 400,
                    "headers": headers,
                    "body": json.dumps({"error": f"Campo requerido faltante: {field}"})
                }
        
        # Simular creación de contacto (por ahora)
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "status": "success",
                "message": "Prospecto creado exitosamente",
                "hubspot_id": "simulated_contact_id"
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"status": "error", "message": str(e)})
        }