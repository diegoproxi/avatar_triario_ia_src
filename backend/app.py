from flask import Flask, request, jsonify
import os
import logging
import resend

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Resend
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')

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

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando"""
    return jsonify({"status": "healthy", "service": "tavus-webhook-handler"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando servidor en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
