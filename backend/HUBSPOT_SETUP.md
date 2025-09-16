# Configuración de HubSpot CRM

## Variables de Entorno Requeridas

Agrega las siguientes variables de entorno a tu archivo `.env`:

```bash
# Configuración de HubSpot CRM
HUBSPOT_API_KEY=your_hubspot_api_key_here
HUBSPOT_PORTAL_ID=your_hubspot_portal_id_here
```

## Cómo obtener las credenciales de HubSpot

### 1. API Key de HubSpot
1. Ve a tu cuenta de HubSpot
2. Navega a Settings > Integrations > Private Apps
3. Crea una nueva Private App
4. En la pestaña "Scopes", asegúrate de tener los siguientes permisos:
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
   - `crm.schemas.contacts.read`
5. Copia el API Key generado

### 2. Portal ID de HubSpot
1. En tu cuenta de HubSpot, ve a Settings > Account Setup > Account Defaults
2. Copia el "Hub ID" (este es tu Portal ID)

## Campos de Contacto Mapeados

El formulario de prospecto mapea los siguientes campos a HubSpot:

| Campo del Formulario | Campo de HubSpot | Descripción |
|---------------------|------------------|-------------|
| nombres | firstname | Nombre del contacto |
| apellidos | lastname | Apellido del contacto |
| compania | company | Nombre de la empresa |
| emailCorporativo | email | Email corporativo |
| rol | jobtitle | Título del trabajo |
| websiteUrl | website | Sitio web de la empresa |

## Estados del Lead

Los contactos creados se configuran con:
- `hs_lead_status`: "NEW"
- `lifecyclestage`: "lead"

## Funcionalidades

- **Crear contacto**: Si el email no existe, se crea un nuevo contacto
- **Actualizar contacto**: Si el email ya existe, se actualiza la información del contacto existente
- **Validación**: Se validan todos los campos requeridos antes de enviar a HubSpot
- **Logging**: Se registran todas las operaciones para debugging

## Testing

Para probar la integración sin credenciales reales, simplemente no configures las variables de entorno. El sistema simulará la creación de contactos y registrará la información en los logs.
