from flask import Flask, request, jsonify
import os
import logging
import resend
import requests

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Resend
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')

# Configuración de HubSpot
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
HUBSPOT_PORTAL_ID = os.getenv('HUBSPOT_PORTAL_ID')

# Link de reunión de HubSpot
HUBSPOT_MEETING_LINK = "https://meetings.hubspot.com/diego-bustamante1?uuid=1867c207-8b62-46dd-9a59-a942352c3dd2"

@app.route('/webhook', methods=['POST'])
def handle_tool_calls():
    try:
        data = request.json
        logger.info(f"Webhook recibido: {data}")
        
        event_type = data.get('event_type')
        
        if event_type == 'conversation.tool_call':
            # Extraer información de la tool call
            tool_name = data['properties']['function']['name']
            arguments = data['properties']['function']['arguments']
            
            logger.info(f"Tool call recibida: {tool_name} con argumentos: {arguments}")
            
            # Ejecutar la función correspondiente
            result = execute_tool(tool_name, arguments)
            
            # Responder con el resultado
            return jsonify({"status": "success", "result": result})
        
        return jsonify({"status": "received"})
    
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def execute_tool(tool_name, arguments):
    """Ejecuta la herramienta correspondiente basada en el nombre"""
    
    if tool_name == "schedule_meeting":
        return schedule_meeting(arguments)
    
    else:
        return f"Tool '{tool_name}' no implementada"

def schedule_meeting(arguments):
    """Programa una reunión enviando un email con el link de HubSpot"""
    
    try:
        email = arguments.get('email')
        if not email:
            return "Error: No se proporcionó el email del usuario"
        
        # Crear el mensaje de email
        subject = "Programar Reunión - Triario"
        
        # Cuerpo del email en HTML
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #ff433f; text-align: center;">¡Hola!</h2>
                
                <p>Gracias por tu interés en programar una reunión con nosotros.</p>
                
                <p>Puedes agendar tu reunión haciendo clic en el siguiente enlace:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{HUBSPOT_MEETING_LINK}" 
                       style="background-color: #ff433f; color: white; padding: 15px 30px; 
                              text-decoration: none; border-radius: 5px; font-weight: bold;
                              display: inline-block;">
                        Programar Reunión
                    </a>
                </div>
                
                <p>O copia y pega este enlace en tu navegador:</p>
                <p style="word-break: break-all; background-color: #f5f5f5; padding: 10px; 
                          border-radius: 3px; font-family: monospace;">
                    {HUBSPOT_MEETING_LINK}
                </p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                
                <p style="font-size: 12px; color: #666; text-align: center;">
                    Este email fue enviado automáticamente por Triario AI
                </p>
            </div>
        </body>
        </html>
        """
        
        # Cuerpo del email en texto plano
        text_body = f"""
        ¡Hola!
        
        Gracias por tu interés en programar una reunión con nosotros.
        
        Puedes agendar tu reunión visitando el siguiente enlace:
        {HUBSPOT_MEETING_LINK}
        
        Este email fue enviado automáticamente por Triario AI
        """
        
        # Enviar el email
        send_email(email, subject, text_body, html_body)
        
        return f"Email de programación de reunión enviado exitosamente a {email}"
    
    except Exception as e:
        logger.error(f"Error enviando email: {str(e)}")
        return f"Error enviando email: {str(e)}"

def send_email(to_email, subject, text_body, html_body):
    """Envía un email usando Resend"""
    
    if not RESEND_API_KEY:
        logger.warning("API Key de Resend no configurada, simulando envío")
        logger.info(f"Email simulado enviado a {to_email}: {subject}")
        return
    
    if not FROM_EMAIL:
        logger.error("FROM_EMAIL no configurado")
        raise ValueError("FROM_EMAIL es requerido")
    
    try:
        # Configurar API key de Resend
        resend.api_key = RESEND_API_KEY
        
        # Enviar el email
        response = resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [to_email],
            "subject": subject,
            "html": html_body,
            "text": text_body
        })
        
        # Log detallado de la respuesta
        logger.info(f"Email enviado a {to_email}")
        logger.info(f"Response: {response}")
        
        # Verificar si el envío fue exitoso
        if response and 'id' in response:
            logger.info(f"✅ Email enviado exitosamente a {to_email}. ID: {response['id']}")
        else:
            logger.warning(f"⚠️ Respuesta inesperada de Resend: {response}")
        
    except Exception as e:
        logger.error(f"Error enviando email con Resend: {str(e)}")
        raise e

@app.route('/api/prospect', methods=['POST'])
def create_prospect():
    """Crea un nuevo prospecto en HubSpot CRM"""
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['nombres', 'apellidos', 'compania', 'emailCorporativo', 'rol']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Crear contacto en HubSpot
        hubspot_result = create_hubspot_contact(data)
        
        if hubspot_result.get('success'):
            logger.info(f"Prospecto creado exitosamente en HubSpot: {data['emailCorporativo']}")
            return jsonify({
                "status": "success",
                "message": "Prospecto creado exitosamente",
                "hubspot_id": hubspot_result.get('contact_id')
            })
        else:
            logger.error(f"Error creando prospecto en HubSpot: {hubspot_result.get('error')}")
            return jsonify({
                "status": "error",
                "message": "Error creando prospecto en HubSpot",
                "error": hubspot_result.get('error')
            }), 500
    
    except Exception as e:
        logger.error(f"Error procesando prospecto: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

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

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando"""
    return jsonify({"status": "healthy", "service": "tavus-webhook-handler"})

# Para Vercel
def handler(request):
    return app(request)

