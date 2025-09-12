# Tavus Webhook Handler

Este backend Flask maneja los webhooks de tool calls de Tavus AI, permitiendo que el agente ejecute funciones específicas durante las conversaciones.

## Características

- **Webhook Handler**: Recibe y procesa tool calls de Tavus
- **Tool Schedule Meeting**: Envía emails con enlaces de reunión de HubSpot
- **Configuración flexible**: Variables de entorno para personalización
- **Logging**: Sistema de logs para debugging
- **Health Check**: Endpoint para verificar el estado del servidor

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno:
```bash
cp env.example .env
# Editar .env con tus credenciales
```

3. Ejecutar el servidor:
```bash
python run.py
```

## Configuración

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `FLASK_ENV` | Modo de desarrollo | `development` |
| `PORT` | Puerto del servidor | `5000` |
| `SMTP_SERVER` | Servidor SMTP | `smtp.gmail.com` |
| `SMTP_PORT` | Puerto SMTP | `587` |
| `EMAIL_USER` | Usuario de email | - |
| `EMAIL_PASSWORD` | Contraseña de email | - |
| `FROM_EMAIL` | Email remitente | `EMAIL_USER` |

### Configuración de Gmail

Para usar Gmail como servidor SMTP:

1. Habilitar autenticación de 2 factores
2. Generar una contraseña de aplicación
3. Usar la contraseña de aplicación en `EMAIL_PASSWORD`

## Uso

### Endpoints

- `POST /webhook` - Recibe tool calls de Tavus
- `GET /health` - Verifica el estado del servidor

### Tool Calls Soportadas

#### schedule_meeting

Programa una reunión enviando un email con el enlace de HubSpot.

**Parámetros:**
- `email` (string): Email del usuario

**Ejemplo de uso:**
```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "function": {
      "name": "schedule_meeting",
      "arguments": {
        "email": "usuario@ejemplo.com"
      }
    }
  }
}
```

**Respuesta:**
```json
{
  "status": "success",
  "result": "Email de programación de reunión enviado exitosamente a usuario@ejemplo.com"
}
```

## Integración con Tavus

### Configuración del Frontend

En el archivo `.env` del frontend, configurar:

```env
VITE_WEBHOOK_URL=https://tu-servidor.com/webhook
```

### Creación de Conversación

El frontend ya está configurado para incluir el `callback_url` en la creación de conversaciones:

```javascript
{
  "replica_id": "rfe12d8b9597",
  "persona_id": "pdced222244b",
  "callback_url": "https://tu-servidor.com/webhook",
  // ... otros parámetros
}
```

## Desarrollo

### Estructura del Proyecto

```
backend/
├── app.py              # Aplicación Flask principal
├── run.py              # Script de ejecución
├── requirements.txt    # Dependencias Python
├── env.example         # Variables de entorno de ejemplo
└── README.md          # Documentación
```

### Agregar Nuevas Tools

Para agregar una nueva tool call:

1. Agregar la función en `execute_tool()`:
```python
def execute_tool(tool_name, arguments):
    if tool_name == "schedule_meeting":
        return schedule_meeting(arguments)
    elif tool_name == "nueva_tool":
        return nueva_tool(arguments)
    # ...
```

2. Implementar la función de la tool:
```python
def nueva_tool(arguments):
    # Lógica de la tool
    return "Resultado de la tool"
```

### Logs

El servidor genera logs detallados para debugging:

```
INFO:webhook:Webhook recibido: {...}
INFO:webhook:Tool call recibida: schedule_meeting con argumentos: {...}
INFO:webhook:Email enviado exitosamente a usuario@ejemplo.com
```

## Despliegue

### Heroku

1. Crear `Procfile`:
```
web: python run.py
```

2. Configurar variables de entorno en Heroku
3. Desplegar

### Docker

1. Crear `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

2. Construir y ejecutar:
```bash
docker build -t tavus-webhook .
docker run -p 5000:5000 --env-file .env tavus-webhook
```

## Troubleshooting

### Error de Email

Si no se envían emails:

1. Verificar credenciales SMTP
2. Revisar logs para errores específicos
3. Verificar configuración de firewall

### Webhook no Recibe Llamadas

1. Verificar que la URL del webhook sea accesible
2. Revisar logs del servidor
3. Verificar configuración de Tavus

### Testing

Para probar el webhook localmente:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "conversation.tool_call",
    "properties": {
      "function": {
        "name": "schedule_meeting",
        "arguments": {
          "email": "test@ejemplo.com"
        }
      }
    }
  }'
```
