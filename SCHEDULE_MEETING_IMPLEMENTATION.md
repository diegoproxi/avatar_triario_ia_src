# Implementación del Tool Call `schedule_meeting`

## Resumen

Se ha implementado exitosamente el tool_call `schedule_meeting` que permite enviar correos electrónicos con enlaces de reunión de HubSpot, seleccionando automáticamente el enlace correcto según el idioma del usuario.

## Funcionalidades Implementadas

### 1. Parámetros del Tool Call

- **`email`** (string, requerido): Email del usuario al que enviar el enlace
- **`language`** (string, opcional): Idioma para seleccionar el enlace correcto
  - `'es'` o `'spanish'` → Español
  - `'en'` o `'english'` → Inglés
  - Cualquier otro valor → Fallback a español

### 2. Enlaces por Idioma

| Idioma | Enlace de HubSpot |
|--------|-------------------|
| Español | `https://meetings.hubspot.com/joshdomagala/inbound-leads-latam` |
| Inglés | `https://meetings.hubspot.com/joshdomagala/inbound-leads-jose-josh-` |

### 3. Contenido de Email

#### Email en Español
- **Asunto**: "Programar Reunión - Triario"
- **Saludo**: "¡Hola!"
- **Mensaje**: "Gracias por tu interés en programar una reunión con nosotros."
- **Botón**: "Programar Reunión"
- **Enlace de respaldo**: Enlace completo para copiar y pegar

#### Email en Inglés
- **Asunto**: "Schedule Meeting - Triario"
- **Saludo**: "Hello!"
- **Mensaje**: "Thank you for your interest in scheduling a meeting with us."
- **Botón**: "Schedule Meeting"
- **Enlace de respaldo**: Enlace completo para copiar y pegar

## Archivos Modificados

### 1. Backend Principal
- **Archivo**: `backend/app.py`
- **Función**: `schedule_meeting(arguments)`
- **Líneas**: 171-302

### 2. API Alternativa
- **Archivo**: `backend/api/index.py`
- **Función**: `schedule_meeting(arguments)`
- **Líneas**: 60-191

### 3. Documentación
- **Archivo**: `TOOL_CALLS_ARCHITECTURE.md`
- **Secciones actualizadas**: Tool Calls Implementadas, Flujo de Datos

## Ejemplos de Uso

### Payload del Webhook - Español
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

### Payload del Webhook - Inglés
```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "function": {
      "name": "schedule_meeting",
      "arguments": {
        "email": "user@example.com",
        "language": "en"
      }
    }
  }
}
```

### Payload del Webhook - Sin Idioma (Fallback)
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

## Respuesta del Tool Call

### Éxito
```json
{
  "status": "success",
  "result": "Email de programación de reunión enviado exitosamente a usuario@ejemplo.com en idioma es"
}
```

### Error
```json
{
  "status": "error",
  "message": "Error: No se proporcionó el email del usuario"
}
```

## Pruebas Realizadas

✅ **6 casos de prueba exitosos**:

1. **Email en español (por defecto)** - Sin parámetro `language`
2. **Email en español (explícito)** - Con `language: "es"`
3. **Email en inglés** - Con `language: "en"`
4. **Email en inglés (nombre completo)** - Con `language: "english"`
5. **Email con idioma inválido** - Fallback a español
6. **Email sin parámetro de idioma** - Fallback a español

### Verificaciones
- ✅ Selección correcta de enlaces según idioma
- ✅ Contenido de email en idioma correcto
- ✅ Fallback a español funciona correctamente
- ✅ Formato de payload del webhook correcto
- ✅ Manejo de errores apropiado

## Configuración Requerida

### Variables de Entorno
```env
RESEND_API_KEY=tu-api-key-de-resend
FROM_EMAIL=tu-email@dominio.com
```

### Notas sobre Resend
- En modo de prueba, solo permite enviar a tu propio email
- Para producción, se requiere verificar un dominio
- Hay límites de rate (2 requests por segundo)

## Integración con Frontend

El tool_call se puede llamar desde Tavus cuando el usuario solicita programar una reunión. El idioma se puede obtener del contexto de la conversación o del `LanguageContext` del frontend.

## Logs y Monitoreo

El sistema registra:
- Idioma seleccionado
- Enlace utilizado
- Email de destino
- Resultado del envío
- Errores si los hay

## Próximos Pasos

1. **Integración con Frontend**: Conectar el tool_call con el selector de idioma
2. **Configuración de Producción**: Verificar dominio en Resend
3. **Testing Real**: Probar con emails reales una vez configurado el dominio
4. **Monitoreo**: Implementar métricas de uso del tool_call

---

**Fecha de Implementación**: 16 de Octubre de 2025
**Estado**: ✅ Completado y Probado
**Versión**: 1.0
