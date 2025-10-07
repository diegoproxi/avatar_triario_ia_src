# 📊 Guía de Logs Detallados de Apollo API

Esta guía te muestra cómo ver logs detallados del enriquecimiento de datos desde Apollo API para entender qué información específica trae para cada empresa.

## 🚀 Formas de Ver los Logs

### 1. Script de Prueba Interactivo

El script más completo para ver logs detallados:

```bash
cd backend
python test_apollo_detailed_logs.py
```

**Características:**
- ✅ Prueba múltiples dominios
- ✅ Muestra datos procesados y raw
- ✅ Análisis detallado de campos disponibles
- ✅ Logs guardados en archivo
- ✅ Interfaz interactiva

### 2. Endpoint de Prueba

Endpoint REST para probar desde cualquier cliente:

```bash
# Iniciar el servidor
cd backend
python app.py

# En otra terminal, ejecutar el script de prueba
./test_apollo_endpoint.sh
```

**O hacer peticiones manuales:**

```bash
curl -X POST http://localhost:5003/api/test-apollo \
  -H "Content-Type: application/json" \
  -d '{"domain": "google.com"}'
```

### 3. Logs en Tiempo Real

Para ver logs en tiempo real mientras usas la aplicación:

```bash
cd backend
python app.py
```

Los logs aparecerán en la consola con emojis y colores para fácil identificación.

## 📋 Información que Apollo Proporciona

### 🏢 Información Básica de la Empresa
- **Nombre**: Nombre oficial de la empresa
- **Descripción**: Descripción corta del negocio
- **Industria**: Sector en el que opera
- **Tamaño**: Número estimado de empleados
- **Fundación**: Año de fundación
- **Sitio Web**: URL principal
- **Redes Sociales**: LinkedIn, Twitter, Facebook

### 💰 Información Financiera
- **Ingresos Anuales**: Revenue anual estimado
- **Financiación Total**: Total recaudado en rondas
- **Última Financiación**: Fecha de la última ronda
- **Tecnologías**: Stack tecnológico utilizado

### 🌍 Ubicaciones
- **Ciudad, Estado, País**: Ubicaciones de oficinas
- **Direcciones**: Direcciones físicas completas

### 👥 Empleados Clave
- **Nombres**: Nombres completos
- **Cargos**: Títulos y roles
- **Emails**: Direcciones de correo
- **LinkedIn**: Perfiles profesionales
- **Departamentos**: Áreas de trabajo

## 🔍 Ejemplo de Logs Detallados

```
🔍 Consultando Apollo API para dominio: google.com
📡 URL: https://api.apollo.io/api/v1/organizations/enrich
📋 Parámetros: {'domain': 'google.com'}
📊 Status Code: 200
⏱️  Tiempo de respuesta: 1.23s
✅ Datos enriquecidos obtenidos de Apollo para google.com
🏢 Organización encontrada: Google LLC
👥 Empleados encontrados: 25
🏭 Industria: Internet
👨‍💼 Tamaño: 10000+ empleados
💰 Ingresos: $100M+
🌍 Ubicaciones: 3

🔄 Procesando datos de Apollo...
📋 Campos disponibles en organization: ['name', 'industry', 'estimated_num_employees', ...]
  • name: Google LLC
  • industry: Internet
  • estimated_num_employees: 10000+
  • annual_revenue: $100M+
  • founded_year: 1998

🌍 Procesando 3 ubicaciones...
  📍 Ubicación 1: Mountain View, California, United States
  📍 Ubicación 2: New York, New York, United States
  📍 Ubicación 3: London, England, United Kingdom

👥 Procesando 25 empleados...
  👤 Empleado 1: Sundar Pichai - CEO
  👤 Empleado 2: Ruth Porat - CFO
  👤 Empleado 3: Prabhakar Raghavan - Senior Vice President
  ...
```

## 📊 Campos Disponibles en Apollo

### Organización (organization)
- `name`: Nombre de la empresa
- `short_description`: Descripción corta
- `industry`: Industria
- `estimated_num_employees`: Número de empleados
- `annual_revenue`: Ingresos anuales
- `founded_year`: Año de fundación
- `primary_domain`: Dominio principal
- `website_url`: Sitio web
- `linkedin_url`: LinkedIn de la empresa
- `twitter_url`: Twitter de la empresa
- `facebook_url`: Facebook de la empresa
- `phone`: Teléfono
- `email`: Email general
- `raw_address`: Dirección
- `total_funding`: Financiación total
- `latest_funding_round_date`: Última financiación
- `keywords`: Tecnologías/palabras clave
- `locations`: Array de ubicaciones

### Empleados (people)
- `first_name`: Nombre
- `last_name`: Apellido
- `title`: Cargo
- `email`: Email
- `linkedin_url`: LinkedIn personal
- `department`: Departamento

## 🛠️ Solución de Problemas

### Error: "No se encontraron datos"
- Verifica que el dominio sea correcto
- Algunos dominios pueden no estar en la base de datos de Apollo
- Prueba con dominios más conocidos

### Error: "API Key no configurada"
- Configura la variable de entorno `APOLLO_API_KEY`
- Verifica que la API key sea válida

### Error: "Timeout"
- La API de Apollo puede estar lenta
- Intenta nuevamente en unos minutos

## 📝 Archivos de Log

Los logs se guardan en:
- **Consola**: Tiempo real durante la ejecución
- **Archivo**: `apollo_detailed_logs.log` (cuando usas el script de prueba)

## 🎯 Casos de Uso

1. **Desarrollo**: Entender qué datos están disponibles
2. **Debugging**: Identificar problemas en el enriquecimiento
3. **Análisis**: Ver qué información específica trae Apollo
4. **Optimización**: Mejorar el procesamiento de datos
5. **Documentación**: Crear ejemplos para el equipo

## 🔗 Endpoints Disponibles

- `POST /api/test-apollo`: Prueba de enriquecimiento
- `POST /api/prospect`: Crear prospecto con enriquecimiento
- `POST /api/enrich-context`: Enriquecer contexto para agente
- `GET /health`: Estado del servidor

## 📞 Soporte

Si tienes problemas con los logs o el enriquecimiento:
1. Revisa los logs de la consola
2. Verifica la configuración de Apollo API
3. Prueba con dominios conocidos
4. Revisa la documentación de Apollo API
