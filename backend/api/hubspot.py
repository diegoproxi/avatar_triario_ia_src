import json
import os
import requests
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

logger = logging.getLogger(__name__)

# Configuración de HubSpot API
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
HUBSPOT_PORTAL_ID = os.getenv('HUBSPOT_PORTAL_ID')
HUBSPOT_BASE_URL = 'https://api.hubapi.com'

def get_contact_info(email):
    """
    Obtiene información detallada de un contacto en HubSpot por email
    
    Args:
        email (str): Email del contacto
    
    Returns:
        dict: Información del contacto o error
    """
    
    if not email:
        return {
            "success": False,
            "error": "Email es requerido"
        }
    
    if not HUBSPOT_API_KEY:
        logger.warning("API Key de HubSpot no configurada")
        return {
            "success": False,
            "error": "API Key de HubSpot no configurada"
        }
    
    try:
        # Buscar contacto por email
        contact_data = search_contact_by_email(email)
        
        if not contact_data.get('success'):
            return contact_data
        
        contact_id = contact_data.get('contact_id')
        
        # Obtener información detallada del contacto
        detailed_info = get_contact_details(contact_id)
        
        if detailed_info.get('success'):
            # Obtener engagements del contacto
            engagements = get_contact_engagements(contact_id)
            
            # Obtener información de la empresa asociada
            company_info = get_contact_company_info(contact_id)
            
            # Combinar toda la información
            combined_info = {
                "contact_info": detailed_info.get('data'),
                "engagements": engagements.get('data', []),
                "company_info": company_info.get('data', {}),
                "contact_id": contact_id
            }
            
            logger.info(f"✅ Información completa del contacto obtenida: {email}")
            return {
                "success": True,
                "data": combined_info
            }
        else:
            return detailed_info
    
    except Exception as e:
        error_msg = f"Error obteniendo información del contacto: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def search_contact_by_email(email):
    """
    Busca un contacto en HubSpot por email
    
    Args:
        email (str): Email del contacto
    
    Returns:
        dict: Resultado de la búsqueda
    """
    
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/search"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email
                }]
            }],
            "properties": [
                "id", "email", "firstname", "lastname", "company", "jobtitle",
                "phone", "website", "createdate", "lastmodifieddate", 
                "hs_lead_status", "lifecyclestage", "hs_analytics_source",
                "hs_analytics_source_data_1", "hs_analytics_source_data_2"
            ]
        }
        
        logger.info(f"🔍 Buscando contacto por email: {email}")
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                contact_id = results[0]['id']
                logger.info(f"✅ Contacto encontrado: {contact_id}")
                return {
                    "success": True,
                    "contact_id": contact_id,
                    "contact_data": results[0]
                }
            else:
                logger.warning(f"No se encontró contacto con email: {email}")
                return {
                    "success": False,
                    "error": "Contacto no encontrado",
                    "code": "NOT_FOUND"
                }
        else:
            error_msg = f"Error buscando contacto: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    except Exception as e:
        error_msg = f"Error en búsqueda de contacto: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def get_contact_details(contact_id):
    """
    Obtiene información detallada de un contacto por ID
    
    Args:
        contact_id (str): ID del contacto en HubSpot
    
    Returns:
        dict: Información detallada del contacto
    """
    
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Propiedades adicionales para obtener más información
        params = {
            "properties": [
                "id", "email", "firstname", "lastname", "company", "jobtitle",
                "phone", "mobilephone", "website", "address", "city", "state", 
                "country", "zip", "industry", "num_employees", "annualrevenue",
                "createdate", "lastmodifieddate", "hs_lead_status", "lifecyclestage",
                "hs_analytics_source", "hs_analytics_source_data_1", "hs_analytics_source_data_2",
                "hs_analytics_last_visit_timestamp", "hs_analytics_num_visits",
                "hs_analytics_num_page_views", "hs_analytics_num_event_completions",
                "hs_email_optout", "hs_email_open", "hs_email_click",
                "hs_latest_source", "hs_latest_source_data_1", "hs_latest_source_data_2",
                "hubspot_owner_id", "hs_lead_score", "hs_predictivecontactscore",
                "description", "notes_last_contacted", "notes_last_activity_date",
                "notes_next_activity_date", "num_contacted_notes", "num_notes",
                "recent_deal_amount", "recent_deal_close_date", "recent_conversion_event_name",
                "recent_conversion_date", "recent_source", "recent_source_data_1"
            ]
        }
        
        logger.info(f"📋 Obteniendo detalles del contacto: {contact_id}")
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            contact_data = response.json()
            
            # Procesar y estructurar los datos
            processed_data = process_contact_data(contact_data)
            
            logger.info(f"✅ Detalles del contacto obtenidos: {contact_id}")
            return {
                "success": True,
                "data": processed_data
            }
        else:
            error_msg = f"Error obteniendo detalles del contacto: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    except Exception as e:
        error_msg = f"Error obteniendo detalles del contacto: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def get_contact_engagements(contact_id):
    """
    Obtiene los engagements de un contacto (reuniones, llamadas, emails, etc.)
    
    Args:
        contact_id (str): ID del contacto en HubSpot
    
    Returns:
        dict: Lista de engagements del contacto
    """
    
    try:
        # Obtener engagements del contacto
        url = f"{HUBSPOT_BASE_URL}/engagements/v1/engagements/associated/contact/{contact_id}/paged"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "limit": 50,  # Límite de engagements a obtener
            "offset": 0
        }
        
        logger.info(f"📞 Obteniendo engagements del contacto: {contact_id}")
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            engagements = data.get('results', [])
            
            # Procesar engagements
            processed_engagements = process_engagements(engagements)
            
            logger.info(f"✅ {len(processed_engagements)} engagements obtenidos para contacto: {contact_id}")
            return {
                "success": True,
                "data": processed_engagements
            }
        else:
            error_msg = f"Error obteniendo engagements: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "data": []
            }
    
    except Exception as e:
        error_msg = f"Error obteniendo engagements: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "data": []
        }

def get_contact_company_info(contact_id):
    """
    Obtiene información de la empresa asociada al contacto
    
    Args:
        contact_id (str): ID del contacto en HubSpot
    
    Returns:
        dict: Información de la empresa
    """
    
    try:
        # Obtener asociaciones del contacto con empresas
        url = f"{HUBSPOT_BASE_URL}/crm/v4/objects/contacts/{contact_id}/associations/companies"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"🏢 Obteniendo información de empresa para contacto: {contact_id}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            company_associations = data.get('results', [])
            
            if company_associations:
                # La API v4 usa 'toObjectId' en lugar de 'id'
                company_id = company_associations[0].get('toObjectId') or company_associations[0].get('id')
                
                # Obtener detalles de la empresa
                company_details = get_company_details(company_id)
                
                if company_details.get('success'):
                    # Obtener negocios asociados a la empresa
                    deals = get_company_deals(company_id)
                    
                    company_info = {
                        "company_details": company_details.get('data'),
                        "deals": deals.get('data', [])
                    }
                    
                    logger.info(f"✅ Información de empresa obtenida: {company_id}")
                    return {
                        "success": True,
                        "data": company_info
                    }
                else:
                    return company_details
            else:
                logger.info(f"No se encontró empresa asociada al contacto: {contact_id}")
                return {
                    "success": True,
                    "data": {}
                }
        else:
            error_msg = f"Error obteniendo asociaciones de empresa: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    except Exception as e:
        error_msg = f"Error obteniendo información de empresa: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def get_company_details(company_id):
    """
    Obtiene detalles de una empresa por ID
    
    Args:
        company_id (str): ID de la empresa en HubSpot
    
    Returns:
        dict: Detalles de la empresa
    """
    
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/companies/{company_id}"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "properties": [
                "id", "name", "domain", "industry", "type", "description",
                "phone", "address", "city", "state", "country", "zip",
                "num_employees", "annualrevenue", "createdate", "lastmodifieddate",
                "hubspot_owner_id", "hs_lead_status", "lifecyclestage",
                "website", "linkedin_company_page", "twitterhandle", "facebook_company_page",
                "hs_analytics_source", "hs_analytics_source_data_1", "hs_analytics_source_data_2",
                "hs_analytics_num_visits", "hs_analytics_num_page_views",
                "hs_analytics_last_visit_timestamp", "hs_analytics_first_visit_timestamp",
                "recent_deal_amount", "recent_deal_close_date", "total_revenue"
            ]
        }
        
        logger.info(f"🏢 Obteniendo detalles de empresa: {company_id}")
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            company_data = response.json()
            
            # Procesar datos de la empresa
            processed_data = process_company_data(company_data)
            
            logger.info(f"✅ Detalles de empresa obtenidos: {company_id}")
            return {
                "success": True,
                "data": processed_data
            }
        else:
            error_msg = f"Error obteniendo detalles de empresa: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    except Exception as e:
        error_msg = f"Error obteniendo detalles de empresa: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def get_company_deals(company_id):
    """
    Obtiene los negocios (deals) asociados a una empresa
    
    Args:
        company_id (str): ID de la empresa en HubSpot
    
    Returns:
        dict: Lista de negocios de la empresa
    """
    
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v4/objects/companies/{company_id}/associations/deals"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"💰 Obteniendo negocios de empresa: {company_id}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            deal_associations = data.get('results', [])
            
            deals = []
            for association in deal_associations:
                # La API v4 usa 'toObjectId' en lugar de 'id'
                deal_id = association.get('toObjectId') or association.get('id')
                
                # Obtener detalles del deal
                deal_details = get_deal_details(deal_id)
                if deal_details.get('success'):
                    deals.append(deal_details.get('data'))
            
            logger.info(f"✅ {len(deals)} negocios obtenidos para empresa: {company_id}")
            return {
                "success": True,
                "data": deals
            }
        else:
            error_msg = f"Error obteniendo negocios: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "data": []
            }
    
    except Exception as e:
        error_msg = f"Error obteniendo negocios: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "data": []
        }

def get_deal_details(deal_id):
    """
    Obtiene detalles de un negocio por ID
    
    Args:
        deal_id (str): ID del negocio en HubSpot
    
    Returns:
        dict: Detalles del negocio
    """
    
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals/{deal_id}"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "properties": [
                "id", "dealname", "dealstage", "amount", "closedate", "createdate",
                "lastmodifieddate", "hs_lead_status", "pipeline", "hs_deal_stage_probability",
                "description", "hubspot_owner_id", "hs_analytics_source",
                "hs_analytics_source_data_1", "hs_analytics_source_data_2"
            ]
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            deal_data = response.json()
            
            # Procesar datos del deal
            processed_data = process_deal_data(deal_data)
            
            return {
                "success": True,
                "data": processed_data
            }
        else:
            return {
                "success": False,
                "error": f"Error obteniendo deal: {response.status_code}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error obteniendo deal: {str(e)}"
        }

def process_contact_data(contact_data):
    """
    Procesa y estructura los datos del contacto
    
    Args:
        contact_data (dict): Datos crudos del contacto
    
    Returns:
        dict: Datos procesados del contacto
    """
    
    properties = contact_data.get('properties', {})
    
    return {
        "informacion_basica": {
            "id": contact_data.get('id'),
            "nombre": f"{properties.get('firstname', '')} {properties.get('lastname', '')}".strip(),
            "email": properties.get('email', ''),
            "empresa": properties.get('company', ''),
            "cargo": properties.get('jobtitle', ''),
            "telefono": properties.get('phone', ''),
            "telefono_movil": properties.get('mobilephone', ''),
            "sitio_web": properties.get('website', ''),
            "industria": properties.get('industry', ''),
            "descripcion": properties.get('description', '')
        },
        "direccion": {
            "direccion": properties.get('address', ''),
            "ciudad": properties.get('city', ''),
            "estado": properties.get('state', ''),
            "pais": properties.get('country', ''),
            "codigo_postal": properties.get('zip', '')
        },
        "informacion_empresa": {
            "num_empleados": properties.get('num_employees', ''),
            "ingresos_anuales": properties.get('annualrevenue', '')
        },
        "actividad": {
            "fecha_creacion": properties.get('createdate', ''),
            "ultima_modificacion": properties.get('lastmodifieddate', ''),
            "ultima_actividad": properties.get('notes_last_activity_date', ''),
            "proxima_actividad": properties.get('notes_next_activity_date', ''),
            "ultimo_contacto": properties.get('notes_last_contacted', '')
        },
        "analiticas": {
            "fuente": properties.get('hs_analytics_source', ''),
            "fuente_datos": properties.get('hs_analytics_source_data_1', ''),
            "ultima_visita": properties.get('hs_analytics_last_visit_timestamp', ''),
            "num_visitas": properties.get('hs_analytics_num_visits', ''),
            "num_paginas_vistas": properties.get('hs_analytics_num_page_views', ''),
            "num_eventos_completados": properties.get('hs_analytics_num_event_completions', '')
        },
        "email_marketing": {
            "opt_out": properties.get('hs_email_optout', ''),
            "emails_abiertos": properties.get('hs_email_open', ''),
            "emails_clicados": properties.get('hs_email_click', '')
        },
        "estado": {
            "estado_lead": properties.get('hs_lead_status', ''),
            "etapa_ciclo_vida": properties.get('lifecyclestage', ''),
            "puntaje_lead": properties.get('hs_lead_score', ''),
            "puntaje_predictivo": properties.get('hs_predictivecontactscore', ''),
            "propietario": properties.get('hubspot_owner_id', '')
        },
        "notas": {
            "num_notas": properties.get('num_notes', ''),
            "num_notas_contactadas": properties.get('num_contacted_notes', '')
        }
    }

def process_engagements(engagements):
    """
    Procesa y estructura los engagements del contacto
    
    Args:
        engagements (list): Lista de engagements crudos
    
    Returns:
        list: Lista de engagements procesados
    """
    
    processed_engagements = []
    
    for engagement in engagements:
        engagement_type = engagement.get('engagement', {}).get('type', '')
        metadata = engagement.get('metadata', {})
        
        processed_engagement = {
            "id": engagement.get('engagement', {}).get('id'),
            "tipo": engagement_type,
            "timestamp": engagement.get('engagement', {}).get('timestamp'),
            "activo": engagement.get('engagement', {}).get('active', False)
        }
        
        # Procesar según el tipo de engagement
        if engagement_type == 'MEETING':
            processed_engagement.update({
                "titulo": metadata.get('title', ''),
                "descripcion": metadata.get('description', ''),
                "fecha_inicio": metadata.get('startTime', ''),
                "fecha_fin": metadata.get('endTime', ''),
                "ubicacion": metadata.get('location', ''),
                "organizador": metadata.get('organizer', ''),
                "asistentes": metadata.get('attendees', []),
                "estado": metadata.get('state', '')
            })
        
        elif engagement_type == 'CALL':
            processed_engagement.update({
                "duracion": metadata.get('durationMilliseconds', 0),
                "estado": metadata.get('state', ''),
                "direccion": metadata.get('direction', ''),
                "disposition": metadata.get('disposition', ''),
                "grabacion_url": metadata.get('recordingUrl', ''),
                "transcripcion": metadata.get('transcript', '')
            })
        
        elif engagement_type == 'EMAIL':
            processed_engagement.update({
                "asunto": metadata.get('subject', ''),
                "de": metadata.get('from', ''),
                "para": metadata.get('to', []),
                "cc": metadata.get('cc', []),
                "bcc": metadata.get('bcc', []),
                "estado": metadata.get('state', ''),
                "direccion": metadata.get('direction', ''),
                "html": metadata.get('html', ''),
                "texto": metadata.get('text', '')
            })
        
        elif engagement_type == 'TASK':
            processed_engagement.update({
                "titulo": metadata.get('title', ''),
                "descripcion": metadata.get('description', ''),
                "estado": metadata.get('state', ''),
                "prioridad": metadata.get('priority', ''),
                "fecha_vencimiento": metadata.get('dueDate', ''),
                "tipo": metadata.get('type', '')
            })
        
        elif engagement_type == 'NOTE':
            processed_engagement.update({
                "contenido": metadata.get('body', ''),
                "fuente": metadata.get('source', ''),
                "tipo": metadata.get('sourceType', '')
            })
        
        processed_engagements.append(processed_engagement)
    
    return processed_engagements

def process_company_data(company_data):
    """
    Procesa y estructura los datos de la empresa
    
    Args:
        company_data (dict): Datos crudos de la empresa
    
    Returns:
        dict: Datos procesados de la empresa
    """
    
    properties = company_data.get('properties', {})
    
    return {
        "informacion_basica": {
            "id": company_data.get('id'),
            "nombre": properties.get('name', ''),
            "dominio": properties.get('domain', ''),
            "industria": properties.get('industry', ''),
            "tipo": properties.get('type', ''),
            "descripcion": properties.get('description', ''),
            "sitio_web": properties.get('website', ''),
            "telefono": properties.get('phone', '')
        },
        "direccion": {
            "direccion": properties.get('address', ''),
            "ciudad": properties.get('city', ''),
            "estado": properties.get('state', ''),
            "pais": properties.get('country', ''),
            "codigo_postal": properties.get('zip', '')
        },
        "informacion_financiera": {
            "num_empleados": properties.get('num_employees', ''),
            "ingresos_anuales": properties.get('annualrevenue', ''),
            "ingresos_totales": properties.get('total_revenue', ''),
            "monto_negocio_reciente": properties.get('recent_deal_amount', ''),
            "fecha_cierre_negocio_reciente": properties.get('recent_deal_close_date', '')
        },
        "redes_sociales": {
            "linkedin": properties.get('linkedin_company_page', ''),
            "twitter": properties.get('twitterhandle', ''),
            "facebook": properties.get('facebook_company_page', '')
        },
        "actividad": {
            "fecha_creacion": properties.get('createdate', ''),
            "ultima_modificacion": properties.get('lastmodifieddate', ''),
            "ultima_visita": properties.get('hs_analytics_last_visit_timestamp', ''),
            "primera_visita": properties.get('hs_analytics_first_visit_timestamp', ''),
            "num_visitas": properties.get('hs_analytics_num_visits', ''),
            "num_paginas_vistas": properties.get('hs_analytics_num_page_views', '')
        },
        "estado": {
            "estado_lead": properties.get('hs_lead_status', ''),
            "etapa_ciclo_vida": properties.get('lifecyclestage', ''),
            "propietario": properties.get('hubspot_owner_id', ''),
            "fuente": properties.get('hs_analytics_source', ''),
            "fuente_datos": properties.get('hs_analytics_source_data_1', '')
        }
    }

def process_deal_data(deal_data):
    """
    Procesa y estructura los datos del negocio
    
    Args:
        deal_data (dict): Datos crudos del negocio
    
    Returns:
        dict: Datos procesados del negocio
    """
    
    properties = deal_data.get('properties', {})
    
    return {
        "informacion_basica": {
            "id": deal_data.get('id'),
            "nombre": properties.get('dealname', ''),
            "etapa": properties.get('dealstage', ''),
            "monto": properties.get('amount', ''),
            "fecha_cierre": properties.get('closedate', ''),
            "descripcion": properties.get('description', ''),
            "pipeline": properties.get('pipeline', ''),
            "probabilidad": properties.get('hs_deal_stage_probability', '')
        },
        "actividad": {
            "fecha_creacion": properties.get('createdate', ''),
            "ultima_modificacion": properties.get('lastmodifieddate', ''),
            "fuente": properties.get('hs_analytics_source', ''),
            "fuente_datos": properties.get('hs_analytics_source_data_1', '')
        },
        "estado": {
            "estado_lead": properties.get('hs_lead_status', ''),
            "propietario": properties.get('hubspot_owner_id', '')
        }
    }

def create_conversation_engagement(contact_id, conversation_data):
    """
    Crea una llamada en HubSpot usando la API de calls v3 con información de la conversación
    
    Args:
        contact_id (str): ID del contacto en HubSpot
        conversation_data (dict): Datos de la conversación
    
    Returns:
        dict: Resultado de la creación de la llamada
    """
    
    if not HUBSPOT_API_KEY:
        logger.warning("API Key de HubSpot no configurada, simulando creación de llamada")
        logger.info(f"Llamada simulada para contacto: {contact_id}")
        return {
            "success": True, 
            "call_id": "simulated_call_id",
            "message": "Llamada simulada creada exitosamente"
        }
    
    try:
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Crear llamada usando la API de calls v3
        logger.info(f"📞 Creando llamada para contacto: {contact_id}")
        logger.info(f"📝 Resumen a incluir: {conversation_data.get('summary', '')[:100]}...")
        
        # Preparar datos de la llamada según la documentación de HubSpot
        # Solo usar propiedades que existen por defecto en HubSpot
        summary=create_detailed_note_content(conversation_data)
        call_data = {
            "properties": {
                "hs_timestamp": int(datetime.now().timestamp() * 1000),  # Timestamp en milisegundos
                "hs_call_title": conversation_data.get('title', 'Conversación con IA - Triario'),
                "hs_call_body":summary,
                "hs_call_duration": conversation_data.get('duration', 0),
                "hs_call_status": "COMPLETED",
                "hs_call_direction": "INBOUND",
                "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7",  # Connected
                "hs_call_recording_url": conversation_data.get('recording_url', ''),
                "hs_call_source": "INTEGRATIONS_PLATFORM"
            },
            "associations": [
                {
                    "to": {
                        "id": contact_id
                    },
                    "types": [
                        {
                            "associationCategory": "HUBSPOT_DEFINED",
                            "associationTypeId": 194  # call_to_contact
                        }
                    ]
                }
            ]
        }
        
        # Incluir información adicional en el cuerpo de la llamada (hs_call_body)
        # ya que las propiedades personalizadas no existen
        additional_info = []
        
        if conversation_data.get('transcript'):
            additional_info.append(f"TRANSCRIPCIÓN:\n{conversation_data.get('transcript', '')}")
        
        if conversation_data.get('pain_points'):
            pain_points_str = ', '.join(conversation_data.get('pain_points', []))
            additional_info.append(f"DOLOR IDENTIFICADO: {pain_points_str}")
        
        if conversation_data.get('key_insights'):
            insights_str = '\n'.join([f"- {insight}" for insight in conversation_data.get('key_insights', [])])
            additional_info.append(f"INSIGHTS CLAVE:\n{insights_str}")
        
        if conversation_data.get('next_steps'):
            additional_info.append(f"PRÓXIMOS PASOS: {conversation_data.get('next_steps', '')}")
        
        if conversation_data.get('engagement_score'):
            additional_info.append(f"PUNTUACIÓN DE CALIFICACIÓN: {conversation_data.get('engagement_score', 0)}/10")
        
        if conversation_data.get('company'):
            additional_info.append(f"EMPRESA: {conversation_data.get('company', '')}")
        
        if conversation_data.get('job_title'):
            additional_info.append(f"CARGO: {conversation_data.get('job_title', '')}")
        
        if conversation_data.get('conversation_id'):
            additional_info.append(f"ID CONVERSACIÓN: {conversation_data.get('conversation_id', '')}")
        
        # Combinar toda la información en el cuerpo de la llamada
        # if additional_info:
        #     full_body = call_data["properties"]["hs_call_body"]
        #     if full_body:
        #         full_body += "\n\n" + "="*50 + "\n\n"
        #     else:
        #         full_body = ""
            
        #     full_body += "\n\n".join(additional_info)
        #     call_data["properties"]["hs_call_body"] = full_body
        
        call_url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/calls"
        call_response = requests.post(call_url, headers=headers, json=call_data)
        
        if call_response.status_code in [200, 201]:
            call_data_response = call_response.json()
            call_id = call_data_response.get('id')
            logger.info(f"✅ Llamada creada exitosamente. ID: {call_id}")
            logger.info(f"📋 Datos enviados: {json.dumps(call_data, indent=2, ensure_ascii=False)}")
            
            return {
                "success": True,
                "call_id": call_id,
                "message": "Llamada creada exitosamente",
                "contact_id": contact_id
            }
        else:
            logger.error(f"❌ Error creando llamada: {call_response.status_code} - {call_response.text}")
            return {
                "success": False, 
                "error": f"Error creando llamada: {call_response.status_code} - {call_response.text}"
            }
    
    except Exception as e:
        error_msg = f"Error creando llamada: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def create_detailed_note_content(conversation_data):
    """
    Crea el contenido detallado para la nota de HubSpot
    
    Args:
        conversation_data (dict): Datos de la conversación
    
    Returns:
        str: Contenido formateado de la nota
    """
    
    note_content = f"""
🎯 RESUMEN DE CONVERSACIÓN 
===========================

📅 Fecha: {datetime.now().strftime('%d de %B de %Y')}
🤖 Agente: {conversation_data.get('ai_agent', 'Tavus')}
📞 Tipo: {conversation_data.get('conversation_type', 'simulated_demo')}
⭐ Puntuación: {conversation_data.get('engagement_score', 0)}/10

👤 INFORMACIÓN DEL CONTACTO
============================
• Empresa: {conversation_data.get('company', 'N/A')}
• Cargo: {conversation_data.get('job_title', 'N/A')}

🎯 PUNTOS CLAVE IDENTIFICADOS
==============================
"""
    
    pain_points = conversation_data.get('pain_points', [])
    for i, pain_point in enumerate(pain_points, 1):
        note_content += f"• {pain_point}\n"
    
    if not pain_points:
        note_content += "• No se identificaron puntos de dolor específicos\n"
    
    note_content += f"""
👥 TOMADORES DE DECISIÓN
========================
"""
    
    decision_makers = conversation_data.get('decision_makers', [])
    for decision_maker in decision_makers:
        note_content += f"• {decision_maker}\n"
    
    if not decision_makers:
        note_content += "• No se identificaron tomadores de decisión específicos\n"
    
    note_content += f"""
📊 MÉTRICAS DE LA CONVERSACIÓN
===============================
• Nivel de interés: {conversation_data.get('interest_level', 'N/A')}
• Presupuesto mencionado: {'Sí' if conversation_data.get('budget_mentioned', False) else 'No'}
• Timeline mencionado: {conversation_data.get('timeline_mentioned', 'N/A')}
• Competidores mencionados: {len(conversation_data.get('competitors_mentioned', []))}
• Puntos de dolor identificados: {len(pain_points)}

🔍 INSIGHTS CLAVE
==================
{conversation_data.get('key_insights', 'No se capturaron insights específicos')}

🔄 PRÓXIMOS PASOS
==================
{conversation_data.get('next_steps', 'No se definieron próximos pasos específicos')}

📝 NOTAS ADICIONALES
=====================
{conversation_data.get('notes', 'No hay notas adicionales')}


📋 RESUMEN
===========
{conversation_data.get('summary', '')}


---

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    return note_content

def create_follow_up_task_content(conversation_data):
    """
    Crea el contenido para la tarea de seguimiento
    
    Args:
        conversation_data (dict): Datos de la conversación
    
    Returns:
        str: Contenido formateado de la tarea
    """
    
    task_content = f"""
TAREA DE SEGUIMIENTO - CONVERSACIÓN SIMULADA
============================================

📅 Fecha de seguimiento: {conversation_data.get('follow_up_date', 'N/A')}
👤 Contacto: {conversation_data.get('contact_name', 'N/A')}
🏢 Empresa: {conversation_data.get('company', 'N/A')}
📞 Conversación: {conversation_data.get('title', 'Conversación Simulada')}

🎯 OBJETIVO
============
{conversation_data.get('next_steps', 'Seguimiento de conversación simulada')}

📊 INFORMACIÓN RELEVANTE
=========================
• Puntuación de engagement: {conversation_data.get('engagement_score', 0)}/10
• Nivel de interés: {conversation_data.get('interest_level', 'N/A')}
• Demo exitosa: {'Sí' if conversation_data.get('demo_successful', False) else 'No'}

🔍 PUNTOS A DISCUTIR
====================
"""
    
    pain_points = conversation_data.get('pain_points', [])
    for i, pain_point in enumerate(pain_points, 1):
        task_content += f"{i}. {pain_point}\n"
    
    if not pain_points:
        task_content += "• Revisar necesidades específicas del cliente\n"
    
    task_content += f"""
📝 NOTAS
=========
{conversation_data.get('notes', 'No hay notas adicionales')}

---
Tarea generada automáticamente por el sistema de conversaciones simuladas
    """
    
    return task_content

def enrich_prospect_with_hubspot_data(prospect_data):
    """
    Enriquece los datos del prospecto con información de HubSpot
    
    Args:
        prospect_data (dict): Datos del prospecto
    
    Returns:
        dict: Datos enriquecidos con información de HubSpot
    """
    
    email = prospect_data.get('emailCorporativo')
    
    if not email:
        return {
            "success": False,
            "error": "Email del prospecto es requerido"
        }
    
    logger.info(f"🔄 Enriqueciendo prospecto con datos de HubSpot: {email}")
    
    # Obtener información del contacto
    hubspot_info = get_contact_info(email)
    
    if hubspot_info.get('success'):
        logger.info(f"✅ Datos de HubSpot obtenidos para: {email}")
        
        # Combinar datos del prospecto con información de HubSpot
        enriched_data = {
            "prospect_data": prospect_data,
            "hubspot_data": hubspot_info.get('data'),
            "enrichment_source": "HubSpot API",
            "enrichment_timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "data": enriched_data
        }
    else:
        logger.warning(f"⚠️ No se pudieron obtener datos de HubSpot: {hubspot_info.get('error')}")
        return {
            "success": False,
            "error": hubspot_info.get('error'),
            "data": {
                "prospect_data": prospect_data,
                "hubspot_data": None,
                "enrichment_source": "HubSpot API",
                "enrichment_timestamp": datetime.now().isoformat()
            }
        }
