"""
Sistema de almacenamiento para mapear conversation_id con hubspot_id
"""
import json
import os
import logging
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class ConversationStorage:
    """
    Clase para manejar el almacenamiento de mapeos entre conversation_id y hubspot_id
    """
    
    def __init__(self, storage_file: str = "conversation_mappings.json"):
        """
        Inicializa el almacenamiento
        
        Args:
            storage_file (str): Archivo donde se almacenan los mapeos
        """
        self.storage_file = storage_file
        self.storage_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.full_path = os.path.join(self.storage_dir, storage_file)
        
        # Crear directorio si no existe
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Cargar datos existentes
        self._load_data()
    
    def _load_data(self):
        """Carga los datos del archivo de almacenamiento"""
        try:
            if os.path.exists(self.full_path):
                with open(self.full_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info(f"Datos cargados desde {self.full_path}")
            else:
                self.data = {}
                logger.info("Inicializando almacenamiento vacío")
        except Exception as e:
            logger.error(f"Error cargando datos: {str(e)}")
            self.data = {}
    
    def _save_data(self):
        """Guarda los datos al archivo de almacenamiento"""
        try:
            with open(self.full_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.info(f"Datos guardados en {self.full_path}")
        except Exception as e:
            logger.error(f"Error guardando datos: {str(e)}")
    
    def store_mapping(self, conversation_id: str, hubspot_id: str, prospect_data: Dict) -> bool:
        """
        Almacena el mapeo entre conversation_id y hubspot_id
        
        Args:
            conversation_id (str): ID de la conversación
            hubspot_id (str): ID del contacto en HubSpot
            prospect_data (Dict): Datos del prospecto
            
        Returns:
            bool: True si se almacenó exitosamente
        """
        try:
            mapping_data = {
                "conversation_id": conversation_id,
                "hubspot_id": hubspot_id,
                "prospect_data": prospect_data,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            self.data[conversation_id] = mapping_data
            self._save_data()
            
            logger.info(f"✅ Mapeo almacenado: conversation_id={conversation_id}, hubspot_id={hubspot_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error almacenando mapeo: {str(e)}")
            return False
    
    def get_mapping(self, conversation_id: str) -> Optional[Dict]:
        """
        Obtiene el mapeo para un conversation_id
        
        Args:
            conversation_id (str): ID de la conversación
            
        Returns:
            Dict o None: Datos del mapeo si existe
        """
        try:
            mapping = self.data.get(conversation_id)
            if mapping:
                logger.info(f"✅ Mapeo encontrado para conversation_id: {conversation_id}")
                return mapping
            else:
                logger.warning(f"⚠️ No se encontró mapeo para conversation_id: {conversation_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error obteniendo mapeo: {str(e)}")
            return None
    
    def get_hubspot_id(self, conversation_id: str) -> Optional[str]:
        """
        Obtiene el hubspot_id para un conversation_id
        
        Args:
            conversation_id (str): ID de la conversación
            
        Returns:
            str o None: HubSpot ID si existe
        """
        mapping = self.get_mapping(conversation_id)
        return mapping.get('hubspot_id') if mapping else None
    
    def update_mapping(self, conversation_id: str, **updates) -> bool:
        """
        Actualiza un mapeo existente
        
        Args:
            conversation_id (str): ID de la conversación
            **updates: Campos a actualizar
            
        Returns:
            bool: True si se actualizó exitosamente
        """
        try:
            if conversation_id in self.data:
                self.data[conversation_id].update(updates)
                self.data[conversation_id]['updated_at'] = datetime.now().isoformat()
                self._save_data()
                
                logger.info(f"✅ Mapeo actualizado para conversation_id: {conversation_id}")
                return True
            else:
                logger.warning(f"⚠️ No se encontró mapeo para actualizar: {conversation_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error actualizando mapeo: {str(e)}")
            return False
    
    def list_mappings(self, limit: int = 100) -> Dict:
        """
        Lista todos los mapeos (con límite para evitar cargar demasiados datos)
        
        Args:
            limit (int): Límite de mapeos a retornar
            
        Returns:
            Dict: Diccionario con los mapeos
        """
        try:
            # Convertir a lista y ordenar por fecha de creación
            mappings_list = list(self.data.items())
            mappings_list.sort(key=lambda x: x[1].get('created_at', ''), reverse=True)
            
            # Aplicar límite
            limited_mappings = dict(mappings_list[:limit])
            
            logger.info(f"✅ {len(limited_mappings)} mapeos listados")
            return {
                "total_count": len(self.data),
                "returned_count": len(limited_mappings),
                "mappings": limited_mappings
            }
            
        except Exception as e:
            logger.error(f"Error listando mapeos: {str(e)}")
            return {"total_count": 0, "returned_count": 0, "mappings": {}}
    
    def delete_mapping(self, conversation_id: str) -> bool:
        """
        Elimina un mapeo
        
        Args:
            conversation_id (str): ID de la conversación
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            if conversation_id in self.data:
                del self.data[conversation_id]
                self._save_data()
                
                logger.info(f"✅ Mapeo eliminado para conversation_id: {conversation_id}")
                return True
            else:
                logger.warning(f"⚠️ No se encontró mapeo para eliminar: {conversation_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error eliminando mapeo: {str(e)}")
            return False

# Instancia global del almacenamiento
conversation_storage = ConversationStorage()
