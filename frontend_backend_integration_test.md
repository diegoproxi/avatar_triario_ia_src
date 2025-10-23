# Prueba de Integración Frontend-Backend para schedule_meeting

## Flujo Corregido

### ✅ **Flujo Actual (Correcto):**

1. **Tavus envía tool_call** al frontend via `app-message`
2. **Frontend detecta** el tool_call `schedule_meeting`
3. **Frontend extrae** email y obtiene idioma actual del usuario
4. **Frontend hace llamada HTTP** al backend `/webhook`
5. **Backend procesa** el tool_call y envía el email
6. **Backend responde** con el resultado al frontend
7. **Frontend registra** el resultado en consola

## Código Implementado

### Frontend (`use-cvi-call.tsx`)

```typescript
const handleScheduleMeeting = useCallback(async (toolArguments: any) => {
  try {
    const email = toolArguments?.email;
    if (!email) {
      console.error('Error: No se proporcionó el email del usuario');
      return;
    }

    // Obtener la URL del backend
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5003';
    
    console.log('📧 Enviando solicitud de programación de reunión:');
    console.log('🌐 Backend URL:', backendUrl);
    console.log('📧 Email:', email);
    console.log('🗣️ Idioma:', language);

    // Crear el payload para el webhook
    const webhookPayload = {
      event_type: 'conversation.tool_call',
      properties: {
        function: {
          name: 'schedule_meeting',
          arguments: {
            email: email,
            language: language
          }
        }
      }
    };

    // Enviar al backend
    const response = await fetch(`${backendUrl}/webhook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(webhookPayload)
    });

    const result = await response.json();
    
    if (response.ok) {
      console.log('✅ Email de programación de reunión enviado exitosamente:', result);
    } else {
      console.error('❌ Error enviando email de programación de reunión:', result);
    }
  } catch (error) {
    console.error('💥 Error procesando solicitud de programación de reunión:', error);
  }
}, [language]);
```

### Manejo del Tool Call

```typescript
case 'schedule_meeting':
  console.log('Tool call schedule_meeting detectado - enviando al backend');
  handleScheduleMeeting(event?.data?.properties?.function?.arguments);
  break;
```

## Payloads de Ejemplo

### 1. Tool Call desde Tavus (Español)
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

### 2. Llamada Frontend → Backend (Español)
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

### 3. Tool Call desde Tavus (Inglés)
```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "function": {
      "name": "schedule_meeting",
      "arguments": {
        "email": "user@example.com"
      }
    }
  }
}
```

### 4. Llamada Frontend → Backend (Inglés)
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

## Pruebas Recomendadas

### 1. Prueba con Usuario en Español
1. **Cambiar idioma** a español en el selector
2. **Iniciar conversación** con Tavus
3. **Solicitar**: "Quiero programar una reunión, mi email es test@ejemplo.com"
4. **Verificar logs**:
   - "Tool call schedule_meeting detectado - enviando al backend"
   - "📧 Email: test@ejemplo.com"
   - "🗣️ Idioma: es"
   - "✅ Email de programación de reunión enviado exitosamente"

### 2. Prueba con Usuario en Inglés
1. **Cambiar idioma** a inglés en el selector
2. **Iniciar conversación** con Tavus
3. **Solicitar**: "I want to schedule a meeting, my email is test@example.com"
4. **Verificar logs**:
   - "Tool call schedule_meeting detectado - enviando al backend"
   - "📧 Email: test@example.com"
   - "🗣️ Idioma: en"
   - "✅ Email de programación de reunión enviado exitosamente"

### 3. Prueba de Error (Sin Email)
1. **Solicitar**: "Quiero programar una reunión" (sin proporcionar email)
2. **Verificar logs**:
   - "Error: No se proporcionó el email del usuario"

### 4. Prueba de Error de Red
1. **Desconectar** el backend
2. **Solicitar** programación de reunión
3. **Verificar logs**:
   - "💥 Error procesando solicitud de programación de reunión"

## Variables de Entorno Requeridas

### Frontend (.env)
```env
VITE_BACKEND_URL=http://localhost:5003
```

### Backend (.env)
```env
RESEND_API_KEY=tu-api-key-de-resend
FROM_EMAIL=tu-email@dominio.com
```

## Logs Esperados

### Consola del Navegador
```
app-message {event_type: "conversation.tool_call", properties: {...}}
Tool call detectado: schedule_meeting
Tool call schedule_meeting detectado - enviando al backend
📧 Enviando solicitud de programación de reunión:
🌐 Backend URL: http://localhost:5003
📧 Email: test@ejemplo.com
🗣️ Idioma: es
✅ Email de programación de reunión enviado exitosamente: {status: "success", result: "..."}
```

### Backend Logs
```
INFO:app:Programando reunión para test@ejemplo.com en idioma: es, usando enlace: https://meetings.hubspot.com/joshdomagala/inbound-leads-latam
INFO:app:✅ Email enviado exitosamente a test@ejemplo.com. ID: ...
```

## Diferencias Clave

### ❌ **Implementación Anterior (Incorrecta):**
- Tool call se ejecutaba automáticamente en backend
- Frontend solo registraba en consola
- No había comunicación directa frontend-backend

### ✅ **Implementación Actual (Correcta):**
- Tool call se detecta en frontend
- Frontend obtiene idioma del usuario actual
- Frontend hace llamada HTTP al backend
- Backend procesa y envía email
- Frontend recibe confirmación del resultado

---

**Fecha de Corrección**: 16 de Octubre de 2025
**Estado**: ✅ Corregido e Implementado
