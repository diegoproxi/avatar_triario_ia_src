from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import resend
import requests
from datetime import datetime
from dotenv import load_dotenv
from api.apollo import enrich_company_data
from api.hubspot import enrich_prospect_with_hubspot_data, get_contact_info, create_conversation_engagement
from storage.conversation_storage import conversation_storage
from agents.conversation_analyzer import conversation_analyzer
from api.hubspot_fields import update_contact_pain_field, validate_pain_value

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde el frontend
CORS(app, origins=[
    'http://localhost:5173', 
    'http://localhost:3000', 
    'http://127.0.0.1:5173', 
    'http://127.0.0.1:3000',
    'https://avatar-triario-ia.vercel.app',  # Frontend en Vercel
    'https://*.vercel.app'  # Cualquier subdominio de Vercel
])

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
def handle_webhook():
    try:
        data = request.json
        logger.info(f"Webhook recibido: {data}")
        
        # Verificar si es una transcripción de conversación
        if 'transcript' in data['properties']:
            return handle_conversation_transcript(data)
        
     
    
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def handle_conversation_transcript(data):
    """
    Maneja el procesamiento de transcripciones de conversaciones
    
    Args:
        data: Datos del webhook con transcript y replica_id
        
    Returns:
        JSON response con el resultado del procesamiento
    """
    try:
        replica_id = data['properties'].get('replica_id')
        transcript = data['properties'].get('transcript', [])
        conversation_id = data.get('conversation_id')
        
        logger.info(f"🎙️ Procesando transcripción de conversación. Replica ID: {replica_id}")
        
        # Buscar el mapeo conversation_id -> hubspot_id
    
        
        mapping = conversation_storage.get_mapping(conversation_id)
        
        if not mapping:
            logger.warning(f"⚠️ No se encontró mapeo para conversation_id: {conversation_id}")
            return jsonify({
                "status": "warning",
                "message": f"No se encontró información del prospecto para la conversación {conversation_id}"
            })
        
        hubspot_id = mapping.get('hubspot_id')
        prospect_data = mapping.get('prospect_data', {})
        
        logger.info(f"📋 Procesando conversación para contacto HubSpot: {hubspot_id}")
        
        # Analizar la transcripción con LangChain
        logger.info("🤖 Iniciando análisis de transcripción con IA")
        analysis = conversation_analyzer.analyze_conversation(transcript, prospect_data)
        
        # Validar y mapear el dolor identificado
        pain_value = conversation_analyzer.get_pain_mapping(analysis.pain_point)
        
        if not validate_pain_value(pain_value):
            logger.warning(f"⚠️ Valor de dolor inválido: {pain_value}")
            pain_value = "No tengo CRM o siento que no lo aprovecho lo suficiente"  # Default
        
        # Actualizar el campo dolores_de_venta en HubSpot
        logger.info(f"📝 Actualizando campo dolores_de_venta: {pain_value}")
        pain_update_result = update_contact_pain_field(hubspot_id, pain_value)
        
        # Crear engagement de conversación en HubSpot
        conversation_data = {
            "title": f"Conversación con {prospect_data.get('nombres', '')} {prospect_data.get('apellidos', '')}",
            "duration": len(transcript) * 30,  # Estimación de duración
            "conversation_type": "video_call",
            "ai_agent": "Wayne (SDR Triario)",
            "engagement_score": analysis.qualification_score,
            "company": prospect_data.get('compania', ''),
            "job_title": prospect_data.get('rol', ''),
            "pain_points": [analysis.pain_point],
            "key_insights": analysis.key_insights,
            "next_steps": analysis.next_steps,
            "summary": analysis.summary,
            "transcript": "\n".join([f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" for msg in transcript]),
            "conversation_id": conversation_id,
            "follow_up_required": analysis.qualification_score >= 7
        }
        
        logger.info("📞 Creando engagement de conversación en HubSpot")
        engagement_result = create_conversation_engagement(hubspot_id, conversation_data)
        
        # Preparar respuesta
        response_data = {
            "status": "success",
            "message": "Conversación procesada exitosamente",
            "conversation_id": conversation_id,
            "hubspot_id": hubspot_id,
            "analysis": {
                "summary": analysis.summary,
                "pain_point": pain_value,
                "pain_confidence": analysis.pain_confidence,
                "qualification_score": analysis.qualification_score,
                "key_insights": analysis.key_insights,
                "next_steps": analysis.next_steps
            },
            "updates": {
                "pain_field_updated": pain_update_result.get('success', False),
                "call_created": engagement_result.get('success', False),
                "call_id": engagement_result.get('call_id')
            }
        }
        
        logger.info(f"✅ Conversación procesada exitosamente para {hubspot_id}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error procesando transcripción: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error procesando transcripción: {str(e)}"
        }), 500

def execute_tool(tool_name, arguments):
    """Ejecuta la herramienta correspondiente basada en el nombre"""
    
    if tool_name == "schedule_meeting":
        return schedule_meeting(arguments)
    
    else:
        return f"Tool '{tool_name}' no implementada"

def schedule_meeting(arguments):
    """Programa una reunión enviando un email con el link de HubSpot según el idioma"""
    
    try:
        email = arguments.get('email')
        language = arguments.get('language', 'es')  # Por defecto español
        
        if not email:
            return "Error: No se proporcionó el email del usuario"
        
        # Seleccionar el enlace según el idioma
        meeting_links = {
            'en': 'https://meetings.hubspot.com/joshdomagala/inbound-leads-jose-josh-',
            'es': 'https://meetings.hubspot.com/joshdomagala/inbound-leads-latam',
            'english': 'https://meetings.hubspot.com/joshdomagala/inbound-leads-jose-josh-',
            'spanish': 'https://meetings.hubspot.com/joshdomagala/inbound-leads-latam'
        }
        
        # Obtener el enlace correcto
        meeting_link = meeting_links.get(language, meeting_links['es'])  # Fallback a español
        
        logger.info(f"Programando reunión para {email} en idioma: {language}, usando enlace: {meeting_link}")
        
        # Crear el mensaje de email según el idioma
        if language in ['en', 'english']:
            # Email en inglés
            subject = "Schedule Meeting - Triario"
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #ff433f; text-align: center;">Hello!</h2>
                    
                    <p>Thank you for your interest in scheduling a meeting with us.</p>
                    
                    <p>You can schedule your meeting by clicking on the following link:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{meeting_link}" 
                           style="background-color: #ff433f; color: white; padding: 15px 30px; 
                                  text-decoration: none; border-radius: 5px; font-weight: bold;
                                  display: inline-block;">
                            Schedule Meeting
                        </a>
                    </div>
                    
                    <p>Or copy and paste this link in your browser:</p>
                    <p style="word-break: break-all; background-color: #f5f5f5; padding: 10px; 
                              border-radius: 3px; font-family: monospace;">
                        {meeting_link}
                    </p>
                    
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    
                    <p style="font-size: 12px; color: #666; text-align: center;">
                        This email was sent automatically by Triario AI
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Hello!
            
            Thank you for your interest in scheduling a meeting with us.
            
            You can schedule your meeting by visiting the following link:
            {meeting_link}
            
            This email was sent automatically by Triario AI
            """
            
        else:
            # Email en español (por defecto)
            subject = "Programar Reunión - Triario"
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #ff433f; text-align: center;">¡Hola!</h2>
                    
                    <p>Gracias por tu interés en programar una reunión con nosotros.</p>
                    
                    <p>Puedes agendar tu reunión haciendo clic en el siguiente enlace:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{meeting_link}" 
                           style="background-color: #ff433f; color: white; padding: 15px 30px; 
                                  text-decoration: none; border-radius: 5px; font-weight: bold;
                                  display: inline-block;">
                            Programar Reunión
                        </a>
                    </div>
                    
                    <p>O copia y pega este enlace en tu navegador:</p>
                    <p style="word-break: break-all; background-color: #f5f5f5; padding: 10px; 
                              border-radius: 3px; font-family: monospace;">
                        {meeting_link}
                    </p>
                    
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    
                    <p style="font-size: 12px; color: #666; text-align: center;">
                        Este email fue enviado automáticamente por Triario AI
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            ¡Hola!
            
            Gracias por tu interés en programar una reunión con nosotros.
            
            Puedes agendar tu reunión visitando el siguiente enlace:
            {meeting_link}
            
            Este email fue enviado automáticamente por Triario AI
            """
        
        # Enviar el email
        send_email(email, subject, text_body, html_body)
        
        return f"Email de programación de reunión enviado exitosamente a {email} en idioma {language}"
    
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
    """Crea un nuevo prospecto en HubSpot CRM y enriquece datos con Apollo"""
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['nombres', 'apellidos', 'compania', 'emailCorporativo', 'rol']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Obtener conversation_id si está presente
        conversation_id = data.get('conversation_id')
        if conversation_id:
            logger.info(f"📝 Procesando prospecto con conversation_id: {conversation_id}")
        else:
            logger.info("⚠️ No se proporcionó conversation_id")
        
        # Enriquecer datos de la empresa con Apollo
        apollo_enriched_data = None
        if data.get('websiteUrl'):
            logger.info(f"Enriqueciendo datos de empresa para dominio: {data['websiteUrl']}")
            apollo_result = enrich_company_data(data['websiteUrl'])
            
            if apollo_result.get('success'):
                apollo_enriched_data = apollo_result.get('data')
                logger.info(f"✅ Datos de Apollo obtenidos para {data['compania']}")
            else:
                logger.warning(f"⚠️ No se pudieron enriquecer datos de Apollo: {apollo_result.get('error')}")
        
        # Enriquecer datos del prospecto con información de HubSpot
        hubspot_enriched_data = None
        logger.info(f"Enriqueciendo prospecto con datos de HubSpot: {data['emailCorporativo']}")
        hubspot_result = enrich_prospect_with_hubspot_data(data)
        
        if hubspot_result.get('success'):
            hubspot_enriched_data = hubspot_result.get('data')
            logger.info(f"✅ Datos de HubSpot obtenidos para {data['emailCorporativo']}")
        else:
            logger.warning(f"⚠️ No se pudieron enriquecer datos de HubSpot: {hubspot_result.get('error')}")
        
        # Crear contacto en HubSpot
        hubspot_contact_result = create_hubspot_contact(data, apollo_enriched_data)
        
        if hubspot_contact_result.get('success'):
            hubspot_id = hubspot_contact_result.get('contact_id')
            logger.info(f"Prospecto creado exitosamente en HubSpot: {data['emailCorporativo']}")
            
            # Almacenar el mapeo entre conversation_id y hubspot_id si está disponible
            if conversation_id and hubspot_id:
                storage_success = conversation_storage.store_mapping(
                    conversation_id=conversation_id,
                    hubspot_id=hubspot_id,
                    prospect_data=data
                )
                if storage_success:
                    logger.info(f"✅ Mapeo almacenado: conversation_id={conversation_id} -> hubspot_id={hubspot_id}")
                else:
                    logger.warning(f"⚠️ Error almacenando mapeo para conversation_id: {conversation_id}")
            
            response_data = {
                "status": "success",
                "message": "Prospecto creado exitosamente",
                "hubspot_id": hubspot_id,
                "conversation_id": conversation_id,
                "prospect_data": data
            }
            
            # Incluir datos enriquecidos de Apollo si están disponibles
            if apollo_enriched_data:
                response_data["apollo_company_data"] = apollo_enriched_data
                logger.info("Datos de Apollo incluidos en la respuesta")
            
            # Incluir datos enriquecidos de HubSpot si están disponibles
            if hubspot_enriched_data:
                response_data["hubspot_contact_data"] = hubspot_enriched_data
                logger.info("Datos de HubSpot incluidos en la respuesta")
            
            return jsonify(response_data)
        else:
            logger.error(f"Error creando prospecto en HubSpot: {hubspot_contact_result.get('error')}")
            return jsonify({
                "status": "error",
                "message": "Error creando prospecto en HubSpot",
                "error": hubspot_contact_result.get('error')
            }), 500
    
    except Exception as e:
        logger.error(f"Error procesando prospecto: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def create_hubspot_contact(prospect_data, enriched_data=None):
    """Crea un contacto en HubSpot CRM con datos enriquecidos de Apollo"""
    
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
            "hs_lead_status": "Unqualified",  # Valor válido según el error
            "lifecyclestage": "lead"
        }
        
        # Agregar datos enriquecidos de Apollo si están disponibles
        if enriched_data:
            company_info = enriched_data.get('informacion_basica', {})
            contact_info = enriched_data.get('contacto', {})
            financial_info = enriched_data.get('financiera', {})
            
            # Información básica de la empresa (solo propiedades válidas para contactos)
            if company_info.get('industria'):
                # Mapear industria de Apollo a valores válidos de HubSpot
                industry_mapping = {
                    'farming': 'Consumo masivo',
                    'agriculture': 'Consumo masivo',
                    'agroindustria': 'Consumo masivo',
                    'software': 'Software y tecnologías SaaS',
                    'technology': 'Software y tecnologías SaaS',
                    'healthcare': 'Servicios de salud',
                    'finance': 'Servicios financieros',
                    'construction': 'Construcción',
                    'retail': 'Retail y ventas on-line'
                }
                mapped_industry = industry_mapping.get(company_info['industria'].lower(), 'Otro')
                contact_properties['industry'] = mapped_industry
            # Nota: description, num_employees, linkedin_company_page no existen en contactos
            
            # Información de contacto adicional
            if contact_info.get('telefono'):
                contact_properties['phone'] = contact_info['telefono']
            if contact_info.get('direccion'):
                contact_properties['address'] = contact_info['direccion']
            
            # Información financiera
            if financial_info.get('ingresos_anuales'):
                contact_properties['annualrevenue'] = financial_info['ingresos_anuales']
            
            logger.info("Datos enriquecidos de Apollo agregados al contacto de HubSpot")
        
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
            return update_existing_hubspot_contact(prospect_data, enriched_data)
        
        else:
            error_msg = f"Error de HubSpot API: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    except Exception as e:
        error_msg = f"Error creando contacto en HubSpot: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}

def update_existing_hubspot_contact(prospect_data, enriched_data=None):
    """Actualiza un contacto existente en HubSpot con datos enriquecidos"""
    
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
                    "hs_lead_status": "Unqualified",  # Valor válido según el error
                    "lifecyclestage": "lead"
                }
                
                # Agregar datos enriquecidos de Apollo si están disponibles
                if enriched_data:
                    company_info = enriched_data.get('informacion_basica', {})
                    contact_info = enriched_data.get('contacto', {})
                    financial_info = enriched_data.get('financiera', {})
                    
                    # Información básica de la empresa (solo propiedades válidas para contactos)
                    if company_info.get('industria'):
                        # Mapear industria de Apollo a valores válidos de HubSpot
                        industry_mapping = {
                            'farming': 'Consumo masivo',
                            'agriculture': 'Consumo masivo',
                            'agroindustria': 'Consumo masivo',
                            'software': 'Software y tecnologías SaaS',
                            'technology': 'Software y tecnologías SaaS',
                            'healthcare': 'Servicios de salud',
                            'finance': 'Servicios financieros',
                            'construction': 'Construcción',
                            'retail': 'Retail y ventas on-line'
                        }
                        mapped_industry = industry_mapping.get(company_info['industria'].lower(), 'Otro')
                        contact_properties['industry'] = mapped_industry
                    # Nota: description, num_employees, linkedin_company_page no existen en contactos
                    
                    # Información de contacto adicional
                    if contact_info.get('telefono'):
                        contact_properties['phone'] = contact_info['telefono']
                    if contact_info.get('direccion'):
                        contact_properties['address'] = contact_info['direccion']
                    
                    # Información financiera
                    if financial_info.get('ingresos_anuales'):
                        contact_properties['annualrevenue'] = financial_info['ingresos_anuales']
                    
                    logger.info("Datos enriquecidos de Apollo agregados al contacto actualizado de HubSpot")
                
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

@app.route('/api/enrich-context', methods=['POST'])
def enrich_and_send_context():
    """Enriquece datos de empresa y los envía como contexto a la conversación"""
    try:
        data = request.json
        
        # Validar datos requeridos
        if not data.get('websiteUrl'):
            return jsonify({"error": "URL del sitio web es requerida"}), 400
        
        # Enriquecer datos con Apollo
        logger.info(f"Enriqueciendo contexto para dominio: {data['websiteUrl']}")
        apollo_result = enrich_company_data(data['websiteUrl'])
        
        if apollo_result.get('success'):
            enriched_data = apollo_result.get('data')
            
            # Crear contexto estructurado para el agente
            context = create_agent_context(enriched_data, data)
            
            logger.info("✅ Contexto enriquecido creado exitosamente")
            return jsonify({
                "status": "success",
                "context": context,
                "enriched_data": enriched_data
            })
        else:
            logger.warning(f"⚠️ No se pudieron enriquecer datos: {apollo_result.get('error')}")
            return jsonify({
                "status": "error",
                "message": "No se pudieron enriquecer los datos de la empresa",
                "error": apollo_result.get('error')
            }), 400
    
    except Exception as e:
        logger.error(f"Error enriqueciendo contexto: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def create_agent_context(enriched_data, prospect_data):
    """
    Crea un contexto estructurado para el agente basado en los datos enriquecidos
    
    Args:
        enriched_data (dict): Datos enriquecidos de Apollo
        prospect_data (dict): Datos del prospecto
    
    Returns:
        str: Contexto formateado para el agente
    """
    
    try:
        context_parts = []
        
        # Información del prospecto
        context_parts.append("=== INFORMACIÓN DEL PROSPECTO ===")
        context_parts.append(f"Nombre: {prospect_data.get('nombres', '')} {prospect_data.get('apellidos', '')}")
        context_parts.append(f"Email: {prospect_data.get('emailCorporativo', '')}")
        context_parts.append(f"Rol: {prospect_data.get('rol', '')}")
        context_parts.append(f"Empresa: {prospect_data.get('compania', '')}")
        context_parts.append("")
        
        # Información de la empresa
        company_info = enriched_data.get('informacion_basica', {})
        if company_info:
            context_parts.append("=== INFORMACIÓN DE LA EMPRESA ===")
            
            if company_info.get('nombre'):
                context_parts.append(f"Empresa: {company_info['nombre']}")
            if company_info.get('descripcion'):
                context_parts.append(f"Descripción: {company_info['descripcion']}")
            if company_info.get('industria'):
                context_parts.append(f"Industria: {company_info['industria']}")
            if company_info.get('tamaño'):
                context_parts.append(f"Número de empleados: {company_info['tamaño']}")
            if company_info.get('fundacion'):
                context_parts.append(f"Año de fundación: {company_info['fundacion']}")
            if company_info.get('sitio_web'):
                context_parts.append(f"Sitio web: {company_info['sitio_web']}")
            
            # Redes sociales
            social_links = []
            if company_info.get('linkedin'):
                social_links.append(f"LinkedIn: {company_info['linkedin']}")
            if company_info.get('twitter'):
                social_links.append(f"Twitter: {company_info['twitter']}")
            if social_links:
                context_parts.append(f"Redes sociales: {', '.join(social_links)}")
            
            context_parts.append("")
        
        # Información financiera
        financial_info = enriched_data.get('financiera', {})
        if financial_info:
            context_parts.append("=== INFORMACIÓN FINANCIERA ===")
            
            if financial_info.get('ingresos_anuales'):
                context_parts.append(f"Ingresos anuales: {financial_info['ingresos_anuales']}")
            if financial_info.get('total_funding'):
                context_parts.append(f"Financiación total: {financial_info['total_funding']}")
            if financial_info.get('ultima_financiacion'):
                context_parts.append(f"Última financiación: {financial_info['ultima_financiacion']}")
            
            # Tecnologías
            if financial_info.get('tecnologias'):
                tech_list = financial_info['tecnologias'][:10]  # Primeras 10 tecnologías
                context_parts.append(f"Tecnologías: {', '.join(tech_list)}")
            
            context_parts.append("")
        
        # Ubicaciones
        locations = enriched_data.get('ubicaciones', [])
        if locations:
            context_parts.append("=== UBICACIONES ===")
            for location in locations:
                location_str = f"- {location.get('ciudad', '')}"
                if location.get('estado'):
                    location_str += f", {location['estado']}"
                if location.get('pais'):
                    location_str += f", {location['pais']}"
                context_parts.append(location_str)
            context_parts.append("")
        
        # Empleados clave
        employees = enriched_data.get('empleados_clave', [])
        if employees:
            context_parts.append("=== EMPLEADOS CLAVE ===")
            for employee in employees[:5]:  # Primeros 5 empleados
                if employee.get('nombre') and employee.get('cargo'):
                    context_parts.append(f"- {employee['nombre']}: {employee['cargo']}")
            context_parts.append("")
        
        # Resumen ejecutivo
        if enriched_data.get('resumen_ejecutivo'):
            context_parts.append("=== RESUMEN EJECUTIVO ===")
            context_parts.append(enriched_data['resumen_ejecutivo'])
            context_parts.append("")
        
        # Información de contacto
        contact_info = enriched_data.get('contacto', {})
        if contact_info:
            context_parts.append("=== INFORMACIÓN DE CONTACTO ===")
            if contact_info.get('telefono'):
                context_parts.append(f"Teléfono: {contact_info['telefono']}")
            if contact_info.get('email_general'):
                context_parts.append(f"Email general: {contact_info['email_general']}")
            if contact_info.get('direccion'):
                context_parts.append(f"Dirección: {contact_info['direccion']}")
            context_parts.append("")
        
        context_parts.append("=== INSTRUCCIONES PARA EL AGENTE ===")
        context_parts.append("Usa esta información para personalizar la conversación y hacer referencias específicas a:")
        context_parts.append("- La industria y el tamaño de la empresa")
        context_parts.append("- Las tecnologías que utilizan")
        context_parts.append("- Los empleados clave y sus roles")
        context_parts.append("- La información financiera relevante")
        context_parts.append("- Los detalles específicos de la empresa")
        context_parts.append("Esto te ayudará a crear una conversación más relevante y personalizada.")
        
        return "\n".join(context_parts)
    
    except Exception as e:
        logger.error(f"Error creando contexto para agente: {str(e)}")
        return f"Error creando contexto: {str(e)}"

def create_combined_executive_summary(prospect_data, apollo_data, hubspot_data):
    """
    Crea un resumen ejecutivo combinando datos de Apollo y HubSpot
    
    Args:
        prospect_data (dict): Datos del prospecto
        apollo_data (dict): Datos enriquecidos de Apollo
        hubspot_data (dict): Datos enriquecidos de HubSpot
    
    Returns:
        str: Resumen ejecutivo combinado
    """
    
    try:
        summary_parts = []
        
        # Información del prospecto
        prospect_name = f"{prospect_data.get('nombres', '')} {prospect_data.get('apellidos', '')}".strip()
        summary_parts.append(f"**{prospect_name}** es {prospect_data.get('rol', '')} en {prospect_data.get('compania', '')}")
        
        # Información de Apollo (empresa)
        if apollo_data:
            company_info = apollo_data.get('informacion_basica', {})
            if company_info:
                if company_info.get('industria'):
                    summary_parts.append(f"La empresa opera en la industria de {company_info['industria']}")
                
                if company_info.get('tamaño'):
                    summary_parts.append(f"con aproximadamente {company_info['tamaño']} empleados")
                
                financial_info = apollo_data.get('financiera', {})
                if financial_info.get('ingresos_anuales'):
                    summary_parts.append(f"e ingresos anuales estimados de {financial_info['ingresos_anuales']}")
        
        # Información de HubSpot (contacto y engagements)
        if hubspot_data and hubspot_data.get('hubspot_data'):
            hubspot_contact_data = hubspot_data['hubspot_data']
            
            # Información del contacto
            contact_info = hubspot_contact_data.get('contact_info', {})
            if contact_info:
                contact_basic = contact_info.get('informacion_basica', {})
                if contact_basic.get('telefono'):
                    summary_parts.append(f"Contacto telefónico: {contact_basic['telefono']}")
                
                # Actividad del contacto
                activity = contact_info.get('actividad', {})
                if activity.get('ultima_actividad'):
                    summary_parts.append(f"Última actividad registrada: {activity['ultima_actividad']}")
                
                # Analíticas del contacto
                analytics = contact_info.get('analiticas', {})
                if analytics.get('num_visitas'):
                    summary_parts.append(f"Ha visitado el sitio web {analytics['num_visitas']} veces")
                
                if analytics.get('num_paginas_vistas'):
                    summary_parts.append(f"con {analytics['num_paginas_vistas']} páginas vistas")
            
            # Engagements del contacto
            engagements = hubspot_contact_data.get('engagements', [])
            if engagements:
                meeting_count = len([e for e in engagements if e.get('tipo') == 'MEETING'])
                call_count = len([e for e in engagements if e.get('tipo') == 'CALL'])
                email_count = len([e for e in engagements if e.get('tipo') == 'EMAIL'])
                
                engagement_summary = []
                if meeting_count > 0:
                    engagement_summary.append(f"{meeting_count} reunión(es)")
                if call_count > 0:
                    engagement_summary.append(f"{call_count} llamada(s)")
                if email_count > 0:
                    engagement_summary.append(f"{email_count} email(s)")
                
                if engagement_summary:
                    summary_parts.append(f"Historial de engagement: {', '.join(engagement_summary)}")
            
            # Información de la empresa en HubSpot
            company_info_hubspot = hubspot_contact_data.get('company_info', {})
            if company_info_hubspot:
                company_details = company_info_hubspot.get('company_details', {})
                if company_details:
                    company_basic = company_details.get('informacion_basica', {})
                    if company_basic.get('dominio'):
                        summary_parts.append(f"Dominio de empresa: {company_basic['dominio']}")
                    
                    # Negocios de la empresa
                    deals = company_info_hubspot.get('deals', [])
                    if deals:
                        total_deals = len(deals)
                        active_deals = len([d for d in deals if d.get('informacion_basica', {}).get('etapa') != 'closedwon'])
                        summary_parts.append(f"La empresa tiene {total_deals} negocio(s) registrado(s), {active_deals} activo(s)")
        
        return ". ".join(summary_parts) + "." if summary_parts else "Información básica del prospecto disponible."
    
    except Exception as e:
        logger.error(f"Error creando resumen ejecutivo combinado: {str(e)}")
        return f"Error creando resumen: {str(e)}"

@app.route('/api/enrich-prospect', methods=['POST'])
def enrich_prospect_complete():
    """Endpoint para enriquecer completamente un prospecto con datos de Apollo y HubSpot"""
    try:
        data = request.json
        
        # Validar datos requeridos
        if not data.get('emailCorporativo'):
            return jsonify({"error": "Email corporativo es requerido"}), 400
        
        email = data['emailCorporativo']
        logger.info(f"🔄 ENRIQUECIMIENTO COMPLETO INICIADO PARA: {email}")
        
        # Enriquecer datos de la empresa con Apollo (si se proporciona websiteUrl)
        apollo_data = None
        if data.get('websiteUrl'):
            logger.info(f"🔍 Enriqueciendo datos de empresa con Apollo para: {data['websiteUrl']}")
            apollo_result = enrich_company_data(data['websiteUrl'])
            
            if apollo_result.get('success'):
                apollo_data = apollo_result.get('data')
                logger.info(f"✅ Datos de Apollo obtenidos para empresa")
            else:
                logger.warning(f"⚠️ No se pudieron obtener datos de Apollo: {apollo_result.get('error')}")
        
        # Enriquecer datos del contacto con HubSpot
        logger.info(f"🔍 Enriqueciendo datos de contacto con HubSpot para: {email}")
        hubspot_result = enrich_prospect_with_hubspot_data(data)
        
        hubspot_data = None
        if hubspot_result.get('success'):
            hubspot_data = hubspot_result.get('data')
            logger.info(f"✅ Datos de HubSpot obtenidos para contacto")
        else:
            logger.warning(f"⚠️ No se pudieron obtener datos de HubSpot: {hubspot_result.get('error')}")
        
        # Crear respuesta combinada
        response_data = {
            "status": "success",
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "prospect_data": data,
            "enrichment_summary": {
                "apollo_success": apollo_data is not None,
                "hubspot_success": hubspot_data is not None,
                "has_company_data": apollo_data is not None,
                "has_contact_data": hubspot_data is not None,
                "has_engagements": hubspot_data and bool(hubspot_data.get('hubspot_data', {}).get('engagements')),
                "has_company_deals": hubspot_data and bool(hubspot_data.get('hubspot_data', {}).get('company_info', {}).get('deals'))
            }
        }
        
        # Incluir datos de Apollo si están disponibles
        if apollo_data:
            response_data["apollo_company_data"] = apollo_data
        
        # Incluir datos de HubSpot si están disponibles
        if hubspot_data:
            response_data["hubspot_contact_data"] = hubspot_data
        
        # Crear resumen ejecutivo combinado
        combined_summary = create_combined_executive_summary(data, apollo_data, hubspot_data)
        response_data["combined_executive_summary"] = combined_summary
        
        logger.info(f"✅ ENRIQUECIMIENTO COMPLETO FINALIZADO PARA: {email}")
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"Error en enriquecimiento completo: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/test-apollo', methods=['POST'])
def test_apollo_enrichment():
    """Endpoint de prueba para mostrar logs detallados del enriquecimiento de Apollo"""
    try:
        data = request.json
        
        # Validar datos requeridos
        if not data.get('domain'):
            return jsonify({"error": "Dominio es requerido"}), 400
        
        domain = data['domain']
        logger.info(f"🧪 INICIANDO PRUEBA DE APOLLO PARA: {domain}")
        
        # Enriquecer datos con Apollo
        apollo_result = enrich_company_data(domain)
        
        if apollo_result.get('success'):
            enriched_data = apollo_result.get('data')
            raw_data = apollo_result.get('raw_data')
            
            logger.info("✅ PRUEBA EXITOSA - Datos enriquecidos obtenidos")
            
            # Crear respuesta detallada
            response_data = {
                "status": "success",
                "domain": domain,
                "timestamp": datetime.now().isoformat(),
                "enriched_data": enriched_data,
                "raw_apollo_response": raw_data,
                "summary": {
                    "company_name": enriched_data.get('informacion_basica', {}).get('nombre', 'N/A'),
                    "industry": enriched_data.get('informacion_basica', {}).get('industria', 'N/A'),
                    "employees": enriched_data.get('informacion_basica', {}).get('tamaño', 'N/A'),
                    "revenue": enriched_data.get('financiera', {}).get('ingresos_anuales', 'N/A'),
                    "locations_count": len(enriched_data.get('ubicaciones', [])),
                    "employees_count": len(enriched_data.get('empleados_clave', [])),
                    "technologies": len(enriched_data.get('financiera', {}).get('tecnologias', []))
                }
            }
            
            return jsonify(response_data)
        else:
            logger.error(f"❌ PRUEBA FALLIDA: {apollo_result.get('error')}")
            return jsonify({
                "status": "error",
                "domain": domain,
                "error": apollo_result.get('error'),
                "code": apollo_result.get('code')
            }), 400
    
    except Exception as e:
        logger.error(f"Error en prueba de Apollo: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/conversation-engagement', methods=['POST'])
def create_conversation_engagement_endpoint():
    """Endpoint para crear un engagement de conversación en HubSpot"""
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['contact_id', 'conversation_data']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        contact_id = data['contact_id']
        conversation_data = data['conversation_data']
        
        logger.info(f"📞 Creando engagement de conversación para contacto: {contact_id}")
        
        # Importar la función de creación de engagement
        from api.hubspot import create_conversation_engagement
        
        # Crear el engagement
        result = create_conversation_engagement(contact_id, conversation_data)
        
        if result.get('success'):
            logger.info(f"✅ Engagement creado exitosamente. ID: {result.get('engagement_id')}")
            return jsonify({
                "status": "success",
                "message": "Engagement de conversación creado exitosamente",
                "engagement_id": result.get('engagement_id'),
                "contact_id": contact_id,
                "timestamp": datetime.now().isoformat()
            })
        else:
            logger.error(f"❌ Error creando engagement: {result.get('error')}")
            return jsonify({
                "status": "error",
                "message": "Error creando engagement de conversación",
                "error": result.get('error')
            }), 500
    
    except Exception as e:
        logger.error(f"Error creando engagement de conversación: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/conversation/<conversation_id>', methods=['GET'])
def get_conversation_mapping(conversation_id):
    """Obtiene la información almacenada para un conversation_id"""
    try:
        logger.info(f"🔍 Consultando mapeo para conversation_id: {conversation_id}")
        
        mapping = conversation_storage.get_mapping(conversation_id)
        
        if mapping:
            logger.info(f"✅ Mapeo encontrado para conversation_id: {conversation_id}")
            return jsonify({
                "status": "success",
                "conversation_id": conversation_id,
                "mapping": mapping
            })
        else:
            logger.warning(f"⚠️ No se encontró mapeo para conversation_id: {conversation_id}")
            return jsonify({
                "status": "not_found",
                "message": f"No se encontró información para conversation_id: {conversation_id}",
                "conversation_id": conversation_id
            }), 404
    
    except Exception as e:
        logger.error(f"Error consultando mapeo: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """Lista todas las conversaciones almacenadas"""
    try:
        limit = request.args.get('limit', 100, type=int)
        logger.info(f"📋 Listando conversaciones (límite: {limit})")
        
        result = conversation_storage.list_mappings(limit=limit)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    
    except Exception as e:
        logger.error(f"Error listando conversaciones: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/conversation/<conversation_id>/hubspot', methods=['GET'])
def get_hubspot_id_by_conversation(conversation_id):
    """Obtiene solo el hubspot_id para un conversation_id"""
    try:
        logger.info(f"🔍 Consultando hubspot_id para conversation_id: {conversation_id}")
        
        hubspot_id = conversation_storage.get_hubspot_id(conversation_id)
        
        if hubspot_id:
            logger.info(f"✅ HubSpot ID encontrado: {hubspot_id}")
            return jsonify({
                "status": "success",
                "conversation_id": conversation_id,
                "hubspot_id": hubspot_id
            })
        else:
            logger.warning(f"⚠️ No se encontró hubspot_id para conversation_id: {conversation_id}")
            return jsonify({
                "status": "not_found",
                "message": f"No se encontró hubspot_id para conversation_id: {conversation_id}",
                "conversation_id": conversation_id
            }), 404
    
    except Exception as e:
        logger.error(f"Error consultando hubspot_id: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando"""
    return jsonify({"status": "healthy", "service": "tavus-webhook-handler"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando servidor en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

# Para Vercel
def handler(request):
    return app(request)
