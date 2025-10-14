"""
Agente de análisis de conversaciones (versión limpia sin LangChain)
Extrae resumen y dolor del cliente de las transcripciones
"""

import os
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Posibles dolores de venta según HubSpot
SALES_PAIN_OPTIONS = [
    "No tengo CRM o siento que no lo aprovecho lo suficiente",
    "Siento que no tengo visibilidad de mi pipeline de ventas",
    "Me cuesta trabajo hacer seguimiento a mis prospectos",
    "No tengo un proceso de ventas definido",
    "No sé cómo calificar a mis prospectos",
    "Me cuesta trabajo cerrar ventas",
    "No tengo métricas claras de mi equipo de ventas",
    "No sé cómo hacer prospecting efectivo",
    "Me cuesta trabajo manejar objeciones",
    "No tengo un sistema de seguimiento post-venta",
    "otro"
]

class ConversationAnalysis(BaseModel):
    """Modelo para el análisis de conversaciones"""
    summary: str = Field(description="Resumen de la conversación")
    pain_point: str = Field(description="Punto de dolor identificado del cliente")
    pain_confidence: float = Field(description="Confianza en la identificación del dolor (0-1)")
    qualification_score: int = Field(description="Puntuación de calificación del prospecto (1-10)")
    key_insights: List[str] = Field(description="Insights clave de la conversación")
    next_steps: List[str] = Field(description="Próximos pasos recomendados")

class ConversationAnalyzer:
    """Agente para analizar conversaciones y extraer información relevante"""
    
    def __init__(self):
        """Inicializa el analizador"""
        
        logger.info("ConversationAnalyzer inicializado (modo sin LangChain)")
        self.llm = None
        self.parser = None
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self):
        """Crea el template de prompt para el análisis"""
        
        prompt_text = """
Eres un experto analista de conversaciones de ventas. Tu tarea es analizar una transcripción de una conversación entre un SDR (Sales Development Representative) y un prospecto, y extraer información clave.

Información del prospecto:
- Nombre: {nombre}
- Empresa: {empresa}
- Rol: {rol}
- Email: {email}

Analiza la conversación y proporciona el análisis en el formato JSON solicitado.
"""

        return prompt_text
    
    def analyze_conversation(self, transcript: List[Dict], prospect_data: Dict) -> ConversationAnalysis:
        """
        Analiza una transcripción de conversación
        """
        
        logger.info("Analizando conversación (modo simulado)")
        
        # Análisis simulado sin LangChain
        analysis = ConversationAnalysis(
            summary="Transcripción procesada sin análisis de IA avanzado",
            pain_point="otro",
            pain_confidence=0.5,
            qualification_score=5,
            key_insights=["Conversación procesada sin análisis de IA"],
            next_steps=["Contactar al prospecto para seguimiento"]
        )
        
        return analysis
    
    def get_pain_mapping(self, pain_point: str) -> str:
        """
        Mapea el punto de dolor identificado a las opciones de HubSpot
        """
        
        # Mapeo simple sin IA
        pain_mapping = {
            "crm": "No tengo CRM o siento que no lo aprovecho lo suficiente",
            "pipeline": "Siento que no tengo visibilidad de mi pipeline de ventas",
            "seguimiento": "Me cuesta trabajo hacer seguimiento a mis prospectos",
            "proceso": "No tengo un proceso de ventas definido",
            "calificar": "No sé cómo calificar a mis prospectos",
            "cerrar": "Me cuesta trabajo cerrar ventas",
            "métricas": "No tengo métricas claras de mi equipo de ventas",
            "prospecting": "No sé cómo hacer prospecting efectivo",
            "objeciones": "Me cuesta trabajo manejar objeciones",
            "post-venta": "No tengo un sistema de seguimiento post-venta"
        }
        
        # Buscar coincidencias simples
        pain_lower = pain_point.lower()
        for key, value in pain_mapping.items():
            if key in pain_lower:
                return value
        
        # Si no encuentra coincidencia, usar "otro"
        return "otro"

# Instancia global del analizador
conversation_analyzer = ConversationAnalyzer()
