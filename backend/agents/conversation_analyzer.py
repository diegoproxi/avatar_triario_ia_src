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
    "No se en que invierte el tiempo mis vendedores",
    "No tengo CRM o siento que no lo aprovecho lo suficiente", 
    "El seguimiento a los prospectos y negocios es minimo",
    "El equipo de ventas gasta mucho tiempo en actividades operativas",
    "Mi nivel de recompra es muy bajo",
    "Los negocios que generamos son muy pocos"
]

class ConversationAnalysis(BaseModel):
    """Modelo para el análisis de la conversación"""
    
    summary: str = Field(description="Resumen ejecutivo de la conversación en máximo 200 palabras")
    
    pain_point: str = Field(description="Dolor principal identificado del cliente. Debe ser uno de los valores predefinidos")
    
    pain_confidence: float = Field(description="Nivel de confianza en la identificación del dolor (0.0 a 1.0)")
    
    key_insights: List[str] = Field(description="Lista de insights clave extraídos de la conversación")
    
    next_steps: str = Field(description="Próximos pasos recomendados basados en la conversación")
    
    qualification_score: int = Field(description="Puntuación de calificación del prospecto (1-10)")

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

INSTRUCCIONES:
1. Analiza toda la transcripción proporcionada
2. Identifica el dolor principal del cliente
3. Crea un resumen ejecutivo
4. Extrae insights clave
5. Sugiere próximos pasos

DOLORES DE VENTA VÁLIDOS:
{sales_pain_options}

FORMATO DE SALIDA:
{format_instructions}

TRANSCRIPCIÓN DE LA CONVERSACIÓN:
{transcript}

CONTEXTO ADICIONAL:
- Empresa: {company}
- Rol del prospecto: {role}
- Email: {email}

Analiza la conversación y proporciona el análisis en el formato JSON solicitado.
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
        
        try:
            # Si no hay API key, retornar análisis simulado
            if not self.llm:
                return self._simulate_analysis(transcript, prospect_data)
            
            # Convertir transcript a texto
            transcript_text = self._format_transcript(transcript)
            
            # Preparar el prompt
            prompt = self.prompt_template.format(
                sales_pain_options="\n".join([f"- {pain}" for pain in SALES_PAIN_OPTIONS]),
                format_instructions=self.parser.get_format_instructions(),
                transcript=transcript_text,
                company=prospect_data.get('compania', 'N/A'),
                role=prospect_data.get('rol', 'N/A'),
                email=prospect_data.get('emailCorporativo', 'N/A')
            )
            
            logger.info("🤖 Iniciando análisis de conversación con LangChain")
            
            # Ejecutar el análisis
            response = self.llm.invoke(prompt)
            
            # Parsear la respuesta
            analysis = self.parser.parse(response.content)
            
            logger.info(f"✅ Análisis completado. Dolor identificado: {analysis.pain_point}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis de conversación: {str(e)}")
            return self._simulate_analysis(transcript, prospect_data)
    
    def _format_transcript(self, transcript: List[Dict]) -> str:
        """Convierte la transcripción a formato de texto legible"""
        
        formatted_messages = []
        
        for message in transcript:
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            
            if role == 'user':
                formatted_messages.append(f"PROSPECTO: {content}")
            elif role == 'assistant':
                formatted_messages.append(f"AGENTE: {content}")
            elif role == 'system' and 'tool_calls' in message:
                # Manejar tool calls
                tool_calls = message.get('tool_calls', [])
                for tool_call in tool_calls:
                    function_name = tool_call.get('function', {}).get('name', 'unknown')
                    formatted_messages.append(f"AGENTE: [Ejecutó herramienta: {function_name}]")
        
        return "\n".join(formatted_messages)
    
    def _simulate_analysis(self, transcript: List[Dict], prospect_data: Dict) -> ConversationAnalysis:
        """Simula un análisis cuando no hay API key de OpenAI"""
        
        logger.info("🔄 Simulando análisis de conversación")
        
        # Análisis básico basado en palabras clave
        transcript_text = self._format_transcript(transcript).lower()
        
        # Identificar dolor basado en palabras clave
        pain_keywords = {
            "No se en que invierte el tiempo mis vendedores": ["tiempo", "vendedores", "actividades", "productividad"],
            "No tengo CRM o siento que no lo aprovecho lo suficiente": ["crm", "sistema", "herramientas", "tecnología"],
            "El seguimiento a los prospectos y negocios es minimo": ["seguimiento", "prospectos", "negocios", "pipeline"],
            "El equipo de ventas gasta mucho tiempo en actividades operativas": ["operativo", "tareas", "administrativo", "procesos"],
            "Mi nivel de recompra es muy bajo": ["recompra", "retention", "fidelización", "clientes"],
            "Los negocios que generamos son muy pocos": ["negocios", "ventas", "generación", "demanda"]
        }
        
        identified_pain = "No tengo CRM o siento que no lo aprovecho lo suficiente"  # Default
        max_score = 0
        
        for pain, keywords in pain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in transcript_text)
            if score > max_score:
                max_score = score
                identified_pain = pain
        
        return ConversationAnalysis(
            summary=f"Conversación con {prospect_data.get('nombres', '')} {prospect_data.get('apellidos', '')} de {prospect_data.get('compania', '')}. El prospecto manifestó interés en mejorar sus procesos de ventas y marketing. Se identificaron desafíos en la gestión de clientes y procesos comerciales.",
            pain_point=identified_pain,
            pain_confidence=0.7 if max_score > 0 else 0.3,
            key_insights=[
                "Prospecto interesado en optimización de procesos",
                "Empresa en etapa de crecimiento",
                "Necesidad de mejor gestión de clientes"
            ],
            next_steps="Agendar reunión de calificación con especialista comercial para evaluar necesidades específicas y presentar propuesta personalizada.",
            qualification_score=7
        )
    
    def get_pain_mapping(self, pain_point: str) -> str:
        """
        Mapea el dolor identificado al valor exacto de HubSpot
        
        Args:
            pain_point: Dolor identificado por el análisis
            
        Returns:
            str: Valor exacto para el campo de HubSpot
        """
        
        # Mapeo exacto de dolores
        pain_mapping = {
            "No se en que invierte el tiempo mis vendedores": "No se en que invierte el tiempo mis vendedores",
            "No tengo CRM o siento que no lo aprovecho lo suficiente": "No tengo CRM o siento que no lo aprovecho lo suficiente",
            "El seguimiento a los prospectos y negocios es minimo": "El seguimiento a los prospectos y negocios es minimo",
            "El equipo de ventas gasta mucho tiempo en actividades operativas": "El equipo de ventas gasta mucho tiempo en actividades operativas",
            "Mi nivel de recompra es muy bajo": "Mi nivel de recompra es muy bajo",
            "Los negocios que generamos son muy pocos": "Los negocios que generamos son muy pocos"
        }
        
        return pain_mapping.get(pain_point, "No tengo CRM o siento que no lo aprovecho lo suficiente")

# Instancia global del analizador
conversation_analyzer = ConversationAnalyzer()
