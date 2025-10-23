# Arquitectura del Sistema de Tool Calls

## Diagrama de Flujo

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Tavus API      │    │   Backend       │
│   (React)       │    │   (Conversation) │    │   (Flask)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │ 1. Crear conversación  │                        │
         │ con callback_url       │                        │
         ├───────────────────────►│                        │
         │                        │                        │
         │ 2. Respuesta con       │                        │
         │ conversation_url       │                        │
         │◄───────────────────────┤                        │
         │                        │                        │
         │ 3. Usuario inicia      │                        │
         │ conversación           │                        │
         │                        │                        │
         │ 4. Usuario solicita    │                        │
         │ programar reunión      │                        │
         │                        │                        │
         │ 5. Tool call           │                        │
         │ schedule_meeting       │                        │
         │◄───────────────────────┤                        │
         │                        │                        │
         │ 6. Webhook POST        │                        │
         │ /webhook               │                        │
         │                        ├───────────────────────►│
         │                        │                        │
         │ 7. Procesar tool call  │                        │
         │ y enviar email         │                        │
         │                        │                        │
         │ 8. Respuesta con       │                        │
         │ resultado              │                        │
         │                        │◄───────────────────────┤
         │                        │                        │
         │ 9. Mostrar resultado   │                        │
         │ al usuario             │                        │
         │                        │                        │
```

## Componentes del Sistema

### 1. Frontend (React + Vite)
- **Archivo**: `my-tavus-app/src/components/ModernDarkChat.tsx`
- **Función**: Crear conversaciones con `callback_url` configurado
- **Configuración**: Variable `VITE_WEBHOOK_URL` en `.env`

### 2. Backend (Flask)
- **Archivo**: `backend/app.py`
- **Función**: Manejar webhooks y ejecutar tool calls
- **Endpoints**:
  - `POST /webhook` - Recibe tool calls de Tavus
  - `GET /health` - Health check del servidor

### 3. Tool Calls Implementadas

#### schedule_meeting
- **Parámetros**: 
  - `email` (string): Email del usuario al que enviar el enlace
  - `language` (string, opcional): Idioma para seleccionar el enlace correcto ('es' para español, 'en' para inglés)
- **Función**: Envía email con enlace de reunión de HubSpot según el idioma
- **Enlaces**:
  - Español: `https://meetings.hubspot.com/joshdomagala/inbound-leads-latam`
  - Inglés: `https://meetings.hubspot.com/joshdomagala/inbound-leads-jose-josh-`
- **Email**: Incluye contenido en el idioma correspondiente, botón de acción y enlace de respaldo

## Flujo de Datos

### 1. Inicialización
```javascript
// Frontend crea conversación con callback
{
  "replica_id": "rfe12d8b9597",
  "persona_id": "pdced222244b",
  "callback_url": "https://tu-servidor.com/webhook",
  // ... otros parámetros
}
```

### 2. Tool Call desde Tavus
```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "function": {
      "name": "schedule_meeting",
      "arguments": {
        "email": "usuario@ejemplo.com",
        "language": "es"
      }
    }
  }
}
```

### 3. Procesamiento en Backend
```python
def schedule_meeting(arguments):
    email = arguments.get('email')
    language = arguments.get('language', 'es')  # Por defecto español
    
    # Seleccionar enlace según idioma
    meeting_links = {
        'en': 'https://meetings.hubspot.com/joshdomagala/inbound-leads-jose-josh-',
        'es': 'https://meetings.hubspot.com/joshdomagala/inbound-leads-latam'
    }
    meeting_link = meeting_links.get(language, meeting_links['es'])
    
    # Enviar email con enlace correcto según idioma
    send_email(email, subject, text_body, html_body)
    return f"Email enviado a {email} en idioma {language}"
```

### 4. Respuesta al Webhook
```json
{
  "status": "success",
  "result": "Email de programación de reunión enviado exitosamente a usuario@ejemplo.com"
}
```

## Configuración Requerida

### Variables de Entorno Frontend
```env
VITE_TAVUS_API_KEY=tu-api-key
VITE_REPLICA_ID=rfe12d8b9597
VITE_PERSONA_ID=pdced222244b
VITE_WEBHOOK_URL=https://tu-servidor.com/webhook
```

### Variables de Entorno Backend
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-app-password
FROM_EMAIL=tu-email@gmail.com
```

## Seguridad

- **Validación de entrada**: Verificar estructura de webhook
- **Autenticación**: Considerar autenticación de webhook
- **Rate limiting**: Implementar límites de requests
- **Logs**: Registrar todas las operaciones

## Monitoreo

- **Health check**: `GET /health`
- **Logs**: Sistema de logging integrado
- **Métricas**: Considerar métricas de uso
- **Alertas**: Notificaciones de errores

## Escalabilidad

- **Load balancer**: Para múltiples instancias
- **Queue system**: Para procesamiento asíncrono
- **Database**: Para persistencia de datos
- **Caching**: Para optimización de rendimiento
