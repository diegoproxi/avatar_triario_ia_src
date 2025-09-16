# Guía de Despliegue del Backend

## 🚀 Opciones de Despliegue

### 1. Railway (Recomendado)

**Pasos:**
1. Ve a [railway.app](https://railway.app)
2. Conecta tu cuenta de GitHub
3. Selecciona tu repositorio
4. Railway detectará automáticamente que es una app Python
5. Configura las variables de entorno en el dashboard

**Variables de entorno necesarias:**
```bash
HUBSPOT_API_KEY=tu_api_key_aqui
HUBSPOT_PORTAL_ID=tu_portal_id_aqui
RESEND_API_KEY=tu_resend_api_key_aqui
FROM_EMAIL=noreply@tudominio.com
FLASK_ENV=production
PORT=5000
```

**Ventajas:**
- ✅ Despliegue automático desde GitHub
- ✅ HTTPS incluido
- ✅ Plan gratuito disponible
- ✅ Fácil configuración de variables de entorno

---

### 2. Render

**Pasos:**
1. Ve a [render.com](https://render.com)
2. Conecta tu cuenta de GitHub
3. Crea un nuevo "Web Service"
4. Selecciona tu repositorio
5. Configura:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Python Version**: 3.9+

**Variables de entorno:**
```bash
HUBSPOT_API_KEY=tu_api_key_aqui
HUBSPOT_PORTAL_ID=tu_portal_id_aqui
RESEND_API_KEY=tu_resend_api_key_aqui
FROM_EMAIL=noreply@tudominio.com
FLASK_ENV=production
PORT=5000
```

**Ventajas:**
- ✅ Plan gratuito generoso
- ✅ Despliegue automático
- ✅ HTTPS incluido
- ✅ Logs en tiempo real

---

### 3. Heroku

**Pasos:**
1. Instala Heroku CLI
2. Crea una nueva app: `heroku create tu-app-name`
3. Configura variables de entorno:
   ```bash
   heroku config:set HUBSPOT_API_KEY=tu_api_key_aqui
   heroku config:set HUBSPOT_PORTAL_ID=tu_portal_id_aqui
   heroku config:set RESEND_API_KEY=tu_resend_api_key_aqui
   heroku config:set FROM_EMAIL=noreply@tudominio.com
   heroku config:set FLASK_ENV=production
   ```
4. Despliega: `git push heroku main`

**Ventajas:**
- ✅ Muy estable y confiable
- ✅ Excelente documentación
- ✅ Add-ons disponibles

---

### 4. Vercel

**Pasos:**
1. Ve a [vercel.com](https://vercel.com)
2. Conecta tu cuenta de GitHub
3. Importa tu repositorio
4. Vercel detectará automáticamente la configuración Python
5. Configura las variables de entorno

**Variables de entorno:**
```bash
HUBSPOT_API_KEY=tu_api_key_aqui
HUBSPOT_PORTAL_ID=tu_portal_id_aqui
RESEND_API_KEY=tu_resend_api_key_aqui
FROM_EMAIL=noreply@tudominio.com
FLASK_ENV=production
```

**Ventajas:**
- ✅ Plan gratuito disponible
- ✅ Despliegue automático
- ✅ Excelente para frontend + backend
- ✅ Edge functions

---

## 🔧 Configuración Post-Despliegue

### 1. Actualizar URL del Frontend

Una vez desplegado, actualiza la URL en el frontend:

```typescript
// En my-tavus-app/src/components/cvi/components/conversation/index.tsx
const response = await fetch('https://tu-backend-url.com/api/prospect', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
});
```

### 2. Configurar CORS (si es necesario)

Si tienes problemas de CORS, agrega esto al backend:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite todas las origins
```

### 3. Configurar Dominio Personalizado

La mayoría de servicios permiten configurar un dominio personalizado:
- Railway: Settings > Domains
- Render: Settings > Custom Domains
- Heroku: Settings > Domains
- Vercel: Settings > Domains

## 🧪 Testing Post-Despliegue

```bash
# Probar el endpoint de salud
curl https://tu-backend-url.com/health

# Probar creación de prospecto
curl -X POST https://tu-backend-url.com/api/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "Test",
    "apellidos": "User",
    "compania": "Test Company",
    "emailCorporativo": "test@example.com",
    "rol": "Manager"
  }'
```

## 📊 Monitoreo

### Logs
- **Railway**: Dashboard > Deployments > View Logs
- **Render**: Dashboard > Logs
- **Heroku**: `heroku logs --tail`
- **Vercel**: Dashboard > Functions > View Logs

### Métricas
- **Railway**: Dashboard > Metrics
- **Render**: Dashboard > Metrics
- **Heroku**: Dashboard > Metrics
- **Vercel**: Dashboard > Analytics

## 💰 Comparación de Costos

| Servicio | Plan Gratuito | Plan Pago | Características |
|----------|---------------|-----------|-----------------|
| **Railway** | $0/mes | $5/mes | Fácil, automático |
| **Render** | $0/mes | $7/mes | Generoso, estable |
| **Heroku** | - | $7/mes | Clásico, confiable |
| **Vercel** | $0/mes | $20/mes | Edge, rápido |

## 🎯 Recomendación Final

Para tu proyecto, recomiendo **Railway** porque:
1. Es muy fácil de configurar
2. Tiene un plan gratuito decente
3. Despliegue automático desde GitHub
4. Excelente para proyectos Python/Flask
5. Buena documentación y soporte

¿Te gustaría que te ayude a configurar el despliegue en alguno de estos servicios?
