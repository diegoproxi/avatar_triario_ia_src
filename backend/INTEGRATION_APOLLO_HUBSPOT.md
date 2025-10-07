# Integración Completa Apollo + HubSpot

## Descripción

Esta integración combina las capacidades de Apollo API (para datos de empresas) con HubSpot CRM (para datos de contactos, engagements y negocios) para proporcionar un enriquecimiento completo de prospectos.

## Funcionalidades Implementadas

### 1. Enriquecimiento de Datos de Empresa (Apollo)
- **Información básica**: Nombre, industria, tamaño, descripción
- **Información financiera**: Ingresos anuales, financiación total
- **Ubicaciones**: Direcciones y oficinas
- **Empleados clave**: Lista de ejecutivos y sus roles
- **Tecnologías**: Stack tecnológico utilizado
- **Redes sociales**: LinkedIn, Twitter, Facebook

### 2. Enriquecimiento de Datos de Contacto (HubSpot)
- **Información personal**: Nombre, email, teléfono, cargo
- **Información de la empresa**: Datos de la empresa asociada
- **Engagements**: Historial completo de interacciones
  - Reuniones programadas y realizadas
  - Llamadas telefónicas
  - Emails enviados y recibidos
  - Tareas y notas
  - Actividades de marketing
- **Analíticas**: Visitas al sitio web, páginas vistas, eventos completados
- **Estado del lead**: Puntaje de lead, etapa del ciclo de vida

### 3. Información de Empresa en HubSpot
- **Detalles de la empresa**: Información registrada en HubSpot
- **Negocios asociados**: Deals y oportunidades de venta
- **Actividad de la empresa**: Visitas al sitio, interacciones

## Endpoints Disponibles

### 1. `/api/prospect` (POST)
**Crear prospecto con enriquecimiento integrado**

```json
{
  "nombres": "Juan Carlos",
  "apellidos": "Pérez García", 
  "compania": "TechCorp Solutions",
  "websiteUrl": "https://www.techcorp.com",
  "emailCorporativo": "juan.perez@techcorp.com",
  "rol": "Director de Tecnología"
}
```

**Respuesta:**
```json
{
  "status": "success",
  "message": "Prospecto creado exitosamente",
  "hubspot_id": "contact_id_123",
  "prospect_data": { ... },
  "apollo_company_data": { ... },
  "hubspot_contact_data": { ... }
}
```

### 2. `/api/enrich-prospect` (POST)
**Enriquecimiento completo sin crear contacto**

```json
{
  "emailCorporativo": "juan.perez@techcorp.com",
  "websiteUrl": "https://www.techcorp.com"
}
```

**Respuesta:**
```json
{
  "status": "success",
  "email": "juan.perez@techcorp.com",
  "timestamp": "2024-01-15T10:30:00Z",
  "enrichment_summary": {
    "apollo_success": true,
    "hubspot_success": true,
    "has_company_data": true,
    "has_contact_data": true,
    "has_engagements": true,
    "has_company_deals": true
  },
  "apollo_company_data": { ... },
  "hubspot_contact_data": { ... },
  "combined_executive_summary": "..."
}
```

## Estructura de Datos

### Datos de Apollo (Empresa)
```json
{
  "informacion_basica": {
    "nombre": "TechCorp Solutions",
    "industria": "Software",
    "tamaño": "51-100",
    "descripcion": "...",
    "sitio_web": "https://www.techcorp.com"
  },
  "financiera": {
    "ingresos_anuales": "$10M-$50M",
    "total_funding": "$5M",
    "tecnologias": ["Python", "React", "AWS"]
  },
  "ubicaciones": [...],
  "empleados_clave": [...],
  "resumen_ejecutivo": "..."
}
```

### Datos de HubSpot (Contacto)
```json
{
  "contact_info": {
    "informacion_basica": {
      "id": "contact_123",
      "nombre": "Juan Carlos Pérez García",
      "email": "juan.perez@techcorp.com",
      "telefono": "+1-555-0123"
    },
    "analiticas": {
      "num_visitas": 15,
      "num_paginas_vistas": 45,
      "ultima_visita": "2024-01-15T09:00:00Z"
    },
    "actividad": {
      "ultima_actividad": "2024-01-14T16:30:00Z",
      "ultimo_contacto": "2024-01-12T10:15:00Z"
    }
  },
  "engagements": [
    {
      "tipo": "MEETING",
      "titulo": "Reunión de seguimiento",
      "fecha_inicio": "2024-01-12T10:00:00Z",
      "estado": "completed"
    },
    {
      "tipo": "CALL",
      "duracion": 1800000,
      "direccion": "outbound",
      "disposition": "connected"
    }
  ],
  "company_info": {
    "company_details": { ... },
    "deals": [
      {
        "informacion_basica": {
          "nombre": "Proyecto de Migración",
          "monto": "$50000",
          "etapa": "negotiation"
        }
      }
    ]
  }
}
```

## Configuración Requerida

### Variables de Entorno
```bash
# Apollo API
APOLLO_API_KEY=your_apollo_api_key

# HubSpot CRM
HUBSPOT_API_KEY=your_hubspot_api_key
HUBSPOT_PORTAL_ID=your_hubspot_portal_id
```

### Permisos de HubSpot
La API Key de HubSpot debe tener los siguientes permisos:
- `crm.objects.contacts.read`
- `crm.objects.contacts.write`
- `crm.objects.companies.read`
- `crm.objects.deals.read`
- `engagements.read`
- `crm.schemas.contacts.read`
- `crm.schemas.companies.read`
- `crm.schemas.deals.read`

## Casos de Uso

### 1. Prospección Completa
Cuando un nuevo prospecto se registra, el sistema:
1. Busca información de la empresa en Apollo
2. Consulta datos del contacto en HubSpot (si existe)
3. Obtiene historial de engagements
4. Recopila información de negocios de la empresa
5. Crea un resumen ejecutivo combinado

### 2. Seguimiento de Leads
Para leads existentes, el sistema puede:
1. Actualizar información de la empresa con Apollo
2. Consultar nuevos engagements en HubSpot
3. Verificar cambios en negocios activos
4. Generar insights de actividad

### 3. Análisis de Oportunidades
El sistema proporciona:
1. Contexto completo del prospecto
2. Historial de interacciones
3. Información financiera de la empresa
4. Empleados clave para outreach
5. Estado de negocios activos

## Logging y Monitoreo

El sistema incluye logging detallado para:
- Consultas a Apollo API
- Consultas a HubSpot API
- Procesamiento de datos
- Errores y fallbacks
- Métricas de rendimiento

## Testing

### Script de Prueba
```bash
python test_complete_enrichment.py
```

### Casos de Prueba
1. **Enriquecimiento completo**: Datos de Apollo + HubSpot
2. **Solo Apollo**: Cuando el contacto no existe en HubSpot
3. **Solo HubSpot**: Cuando no hay datos de empresa en Apollo
4. **Fallback**: Cuando ambas APIs fallan

## Mejores Prácticas

### 1. Manejo de Errores
- Fallback graceful cuando las APIs no están disponibles
- Timeouts apropiados para evitar bloqueos
- Logging detallado para debugging

### 2. Optimización de Rendimiento
- Consultas paralelas cuando es posible
- Cache de datos frecuentemente consultados
- Límites apropiados en número de resultados

### 3. Privacidad y Seguridad
- No almacenar datos sensibles en logs
- Validación de datos de entrada
- Manejo seguro de tokens de API

## Limitaciones

1. **Rate Limits**: Respetar límites de las APIs
2. **Datos Incompletos**: No todos los contactos/empresas tendrán datos completos
3. **Sincronización**: Los datos pueden no estar actualizados en tiempo real
4. **Costos**: Las consultas a las APIs pueden generar costos

## Roadmap

### Próximas Funcionalidades
1. **Cache inteligente**: Reducir consultas repetitivas
2. **Webhooks**: Actualizaciones en tiempo real
3. **Análisis predictivo**: Scoring basado en datos combinados
4. **Integración con más fuentes**: LinkedIn, Crunchbase, etc.
5. **Dashboard de analytics**: Métricas de enriquecimiento
