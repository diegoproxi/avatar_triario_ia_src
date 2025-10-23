# Prueba de Tool Calls en el Frontend

## Problema Identificado y Solucionado

### ❌ Error Original
El código en `use-cvi-call.tsx` tenía un error en la estructura del webhook:
```typescript
// INCORRECTO
event?.data?.properties?.name === 'captura_prospecto_form_tool'
```

### ✅ Corrección Implementada
```typescript
// CORRECTO
const toolName = event?.data?.properties?.function?.name;
```

## Estructura Correcta del Webhook

Según la implementación del backend, los tool_calls llegan con esta estructura:

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

## Tool Calls Soportados

### 1. `captura_prospecto_form_tool`
- **Acción**: Muestra el formulario de captura de prospecto
- **Frontend**: Actualiza el estado `showProspectForm = true`

### 2. `schedule_meeting`
- **Acción**: Se ejecuta automáticamente en el backend
- **Frontend**: Solo registra en consola (no requiere acción del usuario)

## Código Actualizado

```typescript
// Configurar el listener para app-message después de unirse a la llamada
if (daily) {
  daily.on('app-message', (event: any) => {
    console.log('app-message', event);
    
    // Verificar si es un tool_call
    if (event?.data?.event_type === 'conversation.tool_call') {
      const toolName = event?.data?.properties?.function?.name;
      console.log('Tool call detectado:', toolName);
      
      // Manejar diferentes tipos de tool_calls
      switch (toolName) {
        case 'captura_prospecto_form_tool':
          console.log('Mostrando formulario de prospecto');
          setShowProspectForm(true);
          break;
        
        case 'schedule_meeting':
          console.log('Tool call schedule_meeting detectado - se ejecutará en el backend');
          // Este tool_call se ejecuta automáticamente en el backend
          // No requiere acción del frontend
          break;
        
        default:
          console.log('Tool call no reconocido:', toolName);
          break;
      }
    }
  });
}
```

## Pruebas Recomendadas

### 1. Prueba con Tool Call de Prospecto
```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "function": {
      "name": "captura_prospecto_form_tool",
      "arguments": {}
    }
  }
}
```

**Resultado esperado**: Se debe mostrar el formulario de prospecto

### 2. Prueba con Tool Call de Schedule Meeting
```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "function": {
      "name": "schedule_meeting",
      "arguments": {
        "email": "test@ejemplo.com",
        "language": "es"
      }
    }
  }
}
```

**Resultado esperado**: 
- Log en consola: "Tool call schedule_meeting detectado - se ejecutará en el backend"
- Email enviado automáticamente por el backend

### 3. Prueba con Tool Call Desconocido
```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "function": {
      "name": "tool_desconocido",
      "arguments": {}
    }
  }
}
```

**Resultado esperado**: Log en consola: "Tool call no reconocido: tool_desconocido"

## Flujo Completo

1. **Usuario solicita programar reunión** en la conversación con Tavus
2. **Tavus envía tool_call** `schedule_meeting` al webhook del backend
3. **Backend procesa** el tool_call y envía el email
4. **Frontend recibe** el evento y registra en consola (opcional)
5. **Usuario recibe** el email con el enlace de reunión

## Monitoreo

Para verificar que los tool_calls funcionan correctamente:

1. **Abrir DevTools** en el navegador
2. **Ir a la pestaña Console**
3. **Iniciar conversación** con Tavus
4. **Solicitar programar reunión**
5. **Verificar logs**:
   - "app-message" con los datos del evento
   - "Tool call detectado: schedule_meeting"
   - "Tool call schedule_meeting detectado - se ejecutará en el backend"

---

**Fecha de Corrección**: 16 de Octubre de 2025
**Estado**: ✅ Corregido y Probado
