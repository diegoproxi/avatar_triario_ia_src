import json
import os
import requests
import logging

logger = logging.getLogger(__name__)

# Configuración de Apollo API
APOLLO_API_KEY = os.getenv('APOLLO_API_KEY', 'ATpjar6DGtZOKVJWSTiGXQ')
APOLLO_BASE_URL = 'https://api.apollo.io/api/v1'

def enrich_company_data(domain):
    """
    Enriquece los datos de una empresa usando Apollo API
    
    Args:
        domain (str): Dominio de la empresa (ej: example.com)
    
    Returns:
        dict: Datos enriquecidos de la empresa o error
    """
    
    if not domain:
        return {
            "success": False,
            "error": "Dominio es requerido"
        }
    
    # Limpiar el dominio (remover protocolo si existe)
    domain = domain.replace('https://', '').replace('http://', '').replace('www.', '')
    
    try:
        # URL del endpoint de Apollo
        url = f"{APOLLO_BASE_URL}/organizations/enrich"
        
        # Headers para la API de Apollo
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'x-api-key': APOLLO_API_KEY
        }
        
        # Parámetros de la consulta
        params = {
            'domain': domain
        }
        
        logger.info(f"🔍 Consultando Apollo API para dominio: {domain}")
        logger.info(f"📡 URL: {url}")
        logger.info(f"📋 Parámetros: {params}")
        
        # Realizar la petición a Apollo
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        logger.info(f"📊 Status Code: {response.status_code}")
        logger.info(f"⏱️  Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Datos enriquecidos obtenidos de Apollo para {domain}")
            
            # Log detallado de la respuesta
            organization = data.get('organization', {})
            people = data.get('people', [])
            
            logger.info(f"🏢 Organización encontrada: {organization.get('name', 'N/A')}")
            logger.info(f"👥 Empleados encontrados: {len(people)}")
            logger.info(f"🏭 Industria: {organization.get('industry', 'N/A')}")
            logger.info(f"👨‍💼 Tamaño: {organization.get('estimated_num_employees', 'N/A')} empleados")
            logger.info(f"💰 Ingresos: {organization.get('annual_revenue', 'N/A')}")
            logger.info(f"🌍 Ubicaciones: {len(organization.get('locations', []))}")
            
            # Procesar y estructurar los datos relevantes
            enriched_data = process_apollo_data(data)
            
            return {
                "success": True,
                "data": enriched_data,
                "raw_data": data
            }
        
        elif response.status_code == 404:
            logger.warning(f"No se encontraron datos en Apollo para dominio: {domain}")
            return {
                "success": False,
                "error": "No se encontraron datos para este dominio",
                "code": "NOT_FOUND"
            }
        
        else:
            error_msg = f"Error de Apollo API: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "code": "API_ERROR"
            }
    
    except requests.exceptions.Timeout:
        logger.error(f"Timeout consultando Apollo API para {domain}")
        return {
            "success": False,
            "error": "Timeout consultando Apollo API",
            "code": "TIMEOUT"
        }
    
    except Exception as e:
        error_msg = f"Error consultando Apollo API: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "code": "UNKNOWN_ERROR"
        }

def process_apollo_data(apollo_response):
    """
    Procesa los datos de Apollo y extrae la información más relevante
    
    Args:
        apollo_response (dict): Respuesta completa de Apollo API
    
    Returns:
        dict: Datos procesados y estructurados
    """
    
    try:
        logger.info("🔄 Procesando datos de Apollo...")
        
        # Extraer la organización principal
        organization = apollo_response.get('organization', {})
        logger.info(f"📋 Campos disponibles en organization: {list(organization.keys())}")
        
        # Log de campos importantes
        important_fields = ['name', 'industry', 'estimated_num_employees', 'annual_revenue', 'founded_year']
        for field in important_fields:
            value = organization.get(field)
            if value:
                logger.info(f"  • {field}: {value}")
            else:
                logger.info(f"  • {field}: No disponible")
        
        # Información básica de la empresa
        company_info = {
            "nombre": organization.get('name', ''),
            "descripcion": organization.get('short_description', ''),
            "industria": organization.get('industry', ''),
            "tamaño": organization.get('estimated_num_employees', ''),
            "tipo": organization.get('organization_raw_webhook_url', ''),
            "fundacion": organization.get('founded_year', ''),
            "sede_principal": organization.get('primary_domain', ''),
            "sitio_web": organization.get('website_url', ''),
            "linkedin": organization.get('linkedin_url', ''),
            "twitter": organization.get('twitter_url', ''),
            "facebook": organization.get('facebook_url', '')
        }
        
        # Información de contacto
        contact_info = {
            "telefono": organization.get('phone', ''),
            "email_general": organization.get('email', ''),
            "direccion": format_address(organization.get('raw_address', ''))
        }
        
        # Información financiera (si está disponible)
        financial_info = {
            "ingresos_anuales": organization.get('annual_revenue', ''),
            "total_funding": organization.get('total_funding', ''),
            "ultima_financiacion": organization.get('latest_funding_round_date', ''),
            "tecnologias": organization.get('keywords', [])
        }
        
        # Información de ubicaciones
        locations = organization.get('locations', [])
        logger.info(f"🌍 Procesando {len(locations)} ubicaciones...")
        ubicaciones = []
        for i, location in enumerate(locations[:3], 1):  # Máximo 3 ubicaciones
            ubicacion_data = {
                "ciudad": location.get('city', ''),
                "estado": location.get('state', ''),
                "pais": location.get('country', ''),
                "direccion": location.get('address', '')
            }
            ubicaciones.append(ubicacion_data)
            logger.info(f"  📍 Ubicación {i}: {ubicacion_data['ciudad']}, {ubicacion_data['estado']}, {ubicacion_data['pais']}")
        
        # Información de empleados clave (primeros 5)
        employees = apollo_response.get('people', [])
        logger.info(f"👥 Procesando {len(employees)} empleados...")
        empleados_clave = []
        for i, employee in enumerate(employees[:5], 1):
            empleado_data = {
                "nombre": f"{employee.get('first_name', '')} {employee.get('last_name', '')}".strip(),
                "cargo": employee.get('title', ''),
                "email": employee.get('email', ''),
                "linkedin": employee.get('linkedin_url', ''),
                "departamento": employee.get('department', '')
            }
            empleados_clave.append(empleado_data)
            logger.info(f"  👤 Empleado {i}: {empleado_data['nombre']} - {empleado_data['cargo']}")
        
        # Crear resumen ejecutivo
        resumen_ejecutivo = create_executive_summary(company_info, financial_info, empleados_clave)
        
        return {
            "informacion_basica": company_info,
            "contacto": contact_info,
            "financiera": financial_info,
            "ubicaciones": ubicaciones,
            "empleados_clave": empleados_clave,
            "resumen_ejecutivo": resumen_ejecutivo,
            "fecha_consulta": apollo_response.get('created_at', ''),
            "fuente": "Apollo API"
        }
    
    except Exception as e:
        logger.error(f"Error procesando datos de Apollo: {str(e)}")
        return {
            "error": f"Error procesando datos: {str(e)}",
            "raw_data": apollo_response
        }

def format_address(raw_address):
    """
    Formatea la dirección cruda de Apollo
    
    Args:
        raw_address (str): Dirección cruda
    
    Returns:
        str: Dirección formateada
    """
    if not raw_address:
        return ""
    
    # Si es un string, devolverlo tal como está
    if isinstance(raw_address, str):
        return raw_address
    
    # Si es un diccionario, extraer los campos relevantes
    if isinstance(raw_address, dict):
        parts = []
        if raw_address.get('street'):
            parts.append(raw_address['street'])
        if raw_address.get('city'):
            parts.append(raw_address['city'])
        if raw_address.get('state'):
            parts.append(raw_address['state'])
        if raw_address.get('postal_code'):
            parts.append(raw_address['postal_code'])
        if raw_address.get('country'):
            parts.append(raw_address['country'])
        
        return ", ".join(parts)
    
    return str(raw_address)

def create_executive_summary(company_info, financial_info, employees):
    """
    Crea un resumen ejecutivo de la empresa
    
    Args:
        company_info (dict): Información básica de la empresa
        financial_info (dict): Información financiera
        employees (list): Lista de empleados clave
    
    Returns:
        str: Resumen ejecutivo formateado
    """
    
    summary_parts = []
    
    # Información básica
    if company_info.get('nombre'):
        summary_parts.append(f"**{company_info['nombre']}** es una empresa")
    
    if company_info.get('industria'):
        summary_parts.append(f"en la industria de {company_info['industria']}")
    
    if company_info.get('tamaño'):
        summary_parts.append(f"con aproximadamente {company_info['tamaño']} empleados")
    
    # Información financiera
    if financial_info.get('ingresos_anuales'):
        summary_parts.append(f"e ingresos anuales estimados de {financial_info['ingresos_anuales']}")
    
    if financial_info.get('total_funding'):
        summary_parts.append(f"y ha recaudado un total de {financial_info['total_funding']} en financiación")
    
    # Tecnologías
    if financial_info.get('tecnologias') and len(financial_info['tecnologias']) > 0:
        tech_list = financial_info['tecnologias'][:5]  # Primeras 5 tecnologías
        summary_parts.append(f"utiliza tecnologías como {', '.join(tech_list)}")
    
    # Empleados clave
    if employees and len(employees) > 0:
        key_roles = [emp['cargo'] for emp in employees[:3] if emp.get('cargo')]
        if key_roles:
            summary_parts.append(f"con roles clave como {', '.join(key_roles)}")
    
    return ". ".join(summary_parts) + "." if summary_parts else "Información de la empresa disponible a través de Apollo API."

