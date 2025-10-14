"""
Agente de análisis de conversaciones usando LangChain
Extrae resumen y dolor del cliente de las transcripciones
"""

import os
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

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
        """Inicializa el analizador con el modelo de OpenAI"""
        
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY no configurada, el análisis será simulado")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.1,
                api_key=OPENAI_API_KEY
            )
        
        # Configurar el parser de salida
        self.parser = PydanticOutputParser(pydantic_object=ConversationAnalysis)
        
        # Crear el prompt template
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Crea el template de prompt para el análisis"""
        
        prompt_text = """
Eres un experto analista de conversaciones de ventas. Tu tarea es analizar una transcripción de una conversación entre un SDR (Sales Development Representative) y un prospecto, y extraer información clave.

Información del prospecto:
- Nombre: {nombre}
- Empresa: {empresa}
- Rol: {rol}
- Email: {email}

Transcripción de la conversación:
{transcript}

Instrucciones:
1. Analiza la conversación y extrae el punto de dolor principal del prospecto
2. Evalúa la calificación del prospecto (1-10) basándote en:
   - Fit del producto/servicio
   - Autoridad para tomar decisiones
   - Urgencia de la necesidad
   - Presupuesto disponible
3. Identifica insights clave de la conversación
4. Sugiere próximos pasos específicos

{format_instructions}
"""

        return ChatPromptTemplate.from_template(prompt_text)
    
    def analyze_conversation(self, transcript: List[Dict], prospect_data: Dict) -> ConversationAnalysis:
        """
        Analiza una transcripción de conversación
        
        Args:
            transcript: Lista de mensajes de la conversación
            prospect_data: Datos del prospecto
            
        Returns:
            ConversationAnalysis: Análisis estructurado de la conversación
        """
        
        if not self.llm:
            logger.warning("LLM no disponible, retornando análisis simulado")
            return self._get_simulated_analysis(prospect_data)
        
        try:
            # Convertir transcript a texto
            transcript_text = self._format_transcript(transcript)
            
            # Crear el prompt
            prompt = self.prompt_template.format(
                nombre=prospect_data.get('nombre', 'No especificado'),
                empresa=prospect_data.get('empresa', 'No especificada'),
                rol=prospect_data.get('rol', 'No especificado'),
                email=prospect_data.get('email', 'No especificado'),
                transcript=transcript_text,
                format_instructions=self.parser.get_format_instructions()
            )
            
            # Ejecutar el análisis
            response = self.llm.invoke(prompt)
            
            # Parsear la respuesta
            analysis = self.parser.parse(response.content)
            
            logger.info(f"Análisis completado para {prospect_data.get('nombre', 'prospecto')}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis de conversación: {str(e)}")
            return self._get_simulated_analysis(prospect_data)
    
    def _format_transcript(self, transcript: List[Dict]) -> str:
        """Formatea la transcripción para el análisis"""
        
        formatted_lines = []
        for msg in transcript:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            if role == 'user':
                formatted_lines.append(f"SDR: {content}")
            elif role == 'assistant':
                formatted_lines.append(f"Prospecto: {content}")
            else:
                formatted_lines.append(f"{role.title()}: {content}")
        
        return "\n".join(formatted_lines)
    
    def _get_simulated_analysis(self, prospect_data: Dict) -> ConversationAnalysis:
        """Retorna un análisis simulado cuando no hay LLM disponible"""
        
        return ConversationAnalysis(
            summary=f"Conversación con {prospect_data.get('nombre', 'prospecto')} de {prospect_data.get('empresa', 'empresa')}. Análisis simulado.",
            pain_point="No tengo CRM o siento que no lo aprovecho lo suficiente",
            pain_confidence=0.7,
            qualification_score=6,
            key_insights=[
                "Prospecto interesado en mejorar procesos",
                "Mencionó problemas con seguimiento de clientes"
            ],
            next_steps=[
                "Enviar información sobre el CRM",
                "Programar demo personalizada",
                "Seguimiento en una semana"
            ]
        )
    
    def get_pain_mapping(self, pain_point: str) -> str:
        """
        Mapea el punto de dolor identificado a las opciones de HubSpot
        
        Args:
            pain_point: Punto de dolor identificado por la IA
            
        Returns:
            str: Punto de dolor mapeado a las opciones de HubSpot
        """
        
        # Mapeo inteligente basado en palabras clave
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
        
        # Buscar coincidencias
        pain_lower = pain_point.lower()
        for key, value in pain_mapping.items():
            if key in pain_lower:
                return value
        
        # Si no encuentra coincidencia exacta, buscar palabras clave
        if any(word in pain_lower for word in ["crm", "sistema", "software"]):
            return "No tengo CRM o siento que no lo aprovecho lo suficiente"
        elif any(word in pain_lower for word in ["pipeline", "embudo", "proceso"]):
            return "Siento que no tengo visibilidad de mi pipeline de ventas"
        elif any(word in pain_lower for word in ["seguimiento", "contacto", "llamada"]):
            return "Me cuesta trabajo hacer seguimiento a mis prospectos"
        elif any(word in pain_lower for word in ["proceso", "metodología", "pasos"]):
            return "No tengo un proceso de ventas definido"
        elif any(word in pain_lower for word in ["calificar", "evaluar", "priorizar"]):
            return "No sé cómo calificar a mis prospectos"
        elif any(word in pain_lower for word in ["cerrar", "cierre", "negociación"]):
            return "Me cuesta trabajo cerrar ventas"
        elif any(word in pain_lower for word in ["métricas", "kpi", "indicadores"]):
            return "No tengo métricas claras de mi equipo de ventas"
        elif any(word in pain_lower for word in ["prospecting", "prospección", "leads"]):
            return "No sé cómo hacer prospecting efectivo"
        elif any(word in pain_lower for word in ["objeciones", "resistencia", "rechazo"]):
            return "Me cuesta trabajo manejar objeciones"
        elif any(word in pain_lower for word in ["post-venta", "soporte", "retention"]):
            return "No tengo un sistema de seguimiento post-venta"
        
        # Si no encuentra ninguna coincidencia, usar "otro"
        return "otro"

# Instancia global del analizador
conversation_analyzer = ConversationAnalyzer()