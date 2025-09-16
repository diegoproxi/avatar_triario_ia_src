import json
import os
import logging
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de HubSpot
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
HUBSPOT_PORTAL_ID = os.getenv('HUBSPOT_PORTAL_ID')

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
        
        # Crear contacto en HubSpot
        hubspot_result = create_hubspot_contact(data)
        
        if hubspot_result.get('success'):
            logger.info(f"Prospecto creado exitosamente en HubSpot: {data['emailCorporativo']}")
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "status": "success",
                    "message": "Prospecto creado exitosamente",
                    "hubspot_id": hubspot_result.get('contact_id')
                })
            }
        else:
            logger.error(f"Error creando prospecto en HubSpot: {hubspot_result.get('error')}")
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps({
                    "status": "error",
                    "message": "Error creando prospecto en HubSpot",
                    "error": hubspot_result.get('error')
                })
            }
    
    except Exception as e:
        logger.error(f"Error procesando prospecto: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"status": "error", "message": str(e)})
        }

def create_hubspot_contact(prospect_data):
    """Crea un contacto en HubSpot CRM"""
    
    if not HUBSPOT_API_KEY:
        logger.warning("API Key de HubSpot no configurada, simulando creación de contacto")
        logger.info(f"Contacto simulado: {prospect_data['emailCorporativo']}")
        return {"success": True, "contact_id": "simulated_contact_id"}
    
    try:
        # URL de la API de HubSpot para crear contactos
        url = f"https://api.hubapi.com/crm/v3/objects/contacts"
        
        # Headers para la API de HubSpot
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Preparar los datos del contacto
        contact_properties = {
            "email": prospect_data['emailCorporativo'],
            "firstname": prospect_data['nombres'],
            "lastname": prospect_data['apellidos'],
            "company": prospect_data['compania'],
            "jobtitle": prospect_data['rol'],
            "website": prospect_data.get('websiteUrl', ''),
            "hs_lead_status": "NEW",
            "lifecyclestage": "lead"
        }
        
        # Datos para enviar a HubSpot
        payload = {
            "properties": contact_properties
        }
        
        # Realizar la petición a HubSpot
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            contact_data = response.json()
            contact_id = contact_data.get('id')
            logger.info(f"✅ Contacto creado exitosamente en HubSpot. ID: {contact_id}")
            return {"success": True, "contact_id": contact_id}
        
        elif response.status_code == 409:
            # El contacto ya existe, intentar actualizarlo
            logger.info(f"Contacto ya existe, intentando actualizar: {prospect_data['emailCorporativo']}")
            return update_existing_hubspot_contact(prospect_data)
        
        else:
            error_msg = f"Error de HubSpot API: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    except Exception as e:
        error_msg = f"Error creando contacto en HubSpot: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

def update_existing_hubspot_contact(prospect_data):
    """Actualiza un contacto existente en HubSpot"""
    
    try:
        # Primero buscar el contacto por email
        search_url = f"https://api.hubapi.com/crm/v3/objects/contacts/search"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        search_payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": prospect_data['emailCorporativo']
                }]
            }],
            "properties": ["id", "email", "firstname", "lastname"]
        }
        
        search_response = requests.post(search_url, headers=headers, json=search_payload)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            results = search_data.get('results', [])
            
            if results:
                contact_id = results[0]['id']
                
                # Actualizar el contacto
                update_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
                
                contact_properties = {
                    "firstname": prospect_data['nombres'],
                    "lastname": prospect_data['apellidos'],
                    "company": prospect_data['compania'],
                    "jobtitle": prospect_data['rol'],
                    "website": prospect_data.get('websiteUrl', ''),
                    "hs_lead_status": "NEW",
                    "lifecyclestage": "lead"
                }
                
                update_payload = {
                    "properties": contact_properties
                }
                
                update_response = requests.patch(update_url, headers=headers, json=update_payload)
                
                if update_response.status_code == 200:
                    logger.info(f"✅ Contacto actualizado exitosamente en HubSpot. ID: {contact_id}")
                    return {"success": True, "contact_id": contact_id}
                else:
                    error_msg = f"Error actualizando contacto: {update_response.status_code} - {update_response.text}"
                    logger.error(error_msg)
                    return {"success": False, "error": error_msg}
            else:
                error_msg = "Contacto no encontrado para actualizar"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
        else:
            error_msg = f"Error buscando contacto: {search_response.status_code} - {search_response.text}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    except Exception as e:
        error_msg = f"Error actualizando contacto en HubSpot: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}
