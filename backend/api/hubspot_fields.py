"""
Módulo para actualizar campos personalizados en HubSpot
Específicamente para el campo dolores_de_venta
"""

import os
import requests
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

logger = logging.getLogger(__name__)

# Configuración de HubSpot API
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
HUBSPOT_BASE_URL = 'https://api.hubapi.com'

def update_contact_pain_field(contact_id: str, pain_value: str) -> Dict:
    """
    Actualiza el campo dolores_de_venta en un contacto de HubSpot
    
    Args:
        contact_id (str): ID del contacto en HubSpot
        pain_value (str): Valor del dolor a actualizar
        
    Returns:
        Dict: Resultado de la operación
    """
    
    if not HUBSPOT_API_KEY:
        logger.warning("API Key de HubSpot no configurada, simulando actualización de campo")
        logger.info(f"Campo simulado actualizado para contacto {contact_id}: {pain_value}")
        return {"success": True, "message": "Campo actualizado simulado"}
    
    try:
        # URL para actualizar el contacto
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Datos para actualizar
        payload = {
            "properties": {
                "dolores_de_venta": pain_value
            }
        }
        
        logger.info(f"📝 Actualizando campo dolores_de_venta para contacto {contact_id}: {pain_value}")
        
        # Realizar la petición
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            logger.info(f"✅ Campo dolores_de_venta actualizado exitosamente para contacto {contact_id}")
            return {
                "success": True,
                "message": "Campo dolores_de_venta actualizado exitosamente",
                "contact_id": contact_id,
                "pain_value": pain_value
            }
        else:
            error_msg = f"Error actualizando campo: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    except Exception as e:
        error_msg = f"Error actualizando campo dolores_de_venta: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

def get_contact_pain_field(contact_id: str) -> Optional[str]:
    """
    Obtiene el valor actual del campo dolores_de_venta de un contacto
    
    Args:
        contact_id (str): ID del contacto en HubSpot
        
    Returns:
        str o None: Valor actual del campo o None si hay error
    """
    
    if not HUBSPOT_API_KEY:
        logger.warning("API Key de HubSpot no configurada")
        return None
    
    try:
        url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
        
        headers = {
            "Authorization": f"Bearer {HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }
        
        params = {
            "properties": ["dolores_de_venta"]
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            contact_data = response.json()
            pain_value = contact_data.get('properties', {}).get('dolores_de_venta')
            logger.info(f"✅ Campo dolores_de_venta obtenido para contacto {contact_id}: {pain_value}")
            return pain_value
        else:
            logger.error(f"Error obteniendo campo dolores_de_venta: {response.status_code}")
            return None
    
    except Exception as e:
        logger.error(f"Error obteniendo campo dolores_de_venta: {str(e)}")
        return None

def validate_pain_value(pain_value: str) -> bool:
    """
    Valida que el valor del dolor sea uno de los permitidos
    
    Args:
        pain_value (str): Valor a validar
        
    Returns:
        bool: True si es válido, False si no
    """
    
    valid_values = [
        "No se en que invierte el tiempo mis vendedores",
        "No tengo CRM o siento que no lo aprovecho lo suficiente",
        "El seguimiento a los prospectos y negocios es minimo",
        "El equipo de ventas gasta mucho tiempo en actividades operativas",
        "Mi nivel de recompra es muy bajo",
        "Los negocios que generamos son muy pocos"
    ]
    
    return pain_value in valid_values
