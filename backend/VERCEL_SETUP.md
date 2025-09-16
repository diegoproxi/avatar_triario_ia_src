# 🚀 Despliegue en Vercel - Guía Completa

## 📋 **Paso a Paso**

### **1. Preparar el Repositorio**

Asegúrate de que tu código esté en GitHub:
```bash
git add .
git commit -m "Preparar para despliegue en Vercel"
git push origin main
```

### **2. Crear Cuenta en Vercel**

1. Ve a [vercel.com](https://vercel.com)
2. Haz clic en "Sign Up"
3. Conecta tu cuenta de GitHub
4. Autoriza el acceso a tu repositorio

### **3. Importar Proyecto**

1. En el dashboard de Vercel, haz clic en "New Project"
2. Selecciona tu repositorio `tavus_ensayo`
3. Vercel detectará automáticamente que es un proyecto Python
4. Configura:
   - **Framework Preset**: Python
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: (dejar vacío)

### **4. Configurar Variables de Entorno**

En el dashboard de Vercel, ve a Settings > Environment Variables y agrega:

```bash
HUBSPOT_API_KEY=tu_api_key_aqui
HUBSPOT_PORTAL_ID=tu_portal_id_aqui
RESEND_API_KEY=tu_resend_api_key_aqui
FROM_EMAIL=noreply@tudominio.com
FLASK_ENV=production
```

### **5. Desplegar**

1. Haz clic en "Deploy"
2. Vercel construirá y desplegará tu aplicación
3. Obtendrás una URL como: `https://tu-proyecto.vercel.app`

## 🔧 **Configuración Técnica**

### **Archivos de Configuración**

- ✅ `vercel.json` - Configuración de Vercel
- ✅ `requirements.txt` - Dependencias Python
- ✅ `app.py` - Aplicación Flask principal

### **Estructura del Proyecto**

```
tavus_ensayo/
├── backend/
│   ├── app.py              # Aplicación Flask
│   ├── requirements.txt    # Dependencias
│   ├── vercel.json        # Configuración Vercel
│   └── VERCEL_SETUP.md    # Esta guía
└── my-tavus-app/          # Frontend (separado)
```

## 🌐 **URLs de la Aplicación**

Después del despliegue tendrás:

- **Backend**: `https://tu-proyecto.vercel.app`
- **Health Check**: `https://tu-proyecto.vercel.app/health`
- **API Prospectos**: `https://tu-proyecto.vercel.app/api/prospect`

## 🧪 **Testing Post-Despliegue**

### **1. Probar Health Check**
```bash
curl https://tu-proyecto.vercel.app/health
```

### **2. Probar API de Prospectos**
```bash
curl -X POST https://tu-proyecto.vercel.app/api/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "Test",
    "apellidos": "User",
    "compania": "Test Company",
    "emailCorporativo": "test@example.com",
    "rol": "Manager"
  }'
```

## 🔄 **Actualizar Frontend**

Una vez desplegado, actualiza la URL en el frontend:

```typescript
// En my-tavus-app/src/components/cvi/components/conversation/index.tsx
const response = await fetch('https://tu-proyecto.vercel.app/api/prospect', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data)
});
```

## 📊 **Monitoreo y Logs**

### **Logs en Tiempo Real**
- Ve a tu proyecto en Vercel
- Pestaña "Functions" > "View Logs"

### **Métricas**
- Dashboard > Analytics
- Monitorea requests, errores, y performance

## 🚨 **Solución de Problemas**

### **Error de Build**
- Verifica que `requirements.txt` tenga todas las dependencias
- Revisa los logs de build en Vercel

### **Error 500**
- Verifica las variables de entorno
- Revisa los logs de la función

### **CORS Issues**
- Vercel maneja CORS automáticamente
- Si hay problemas, contacta soporte

## 💰 **Costos**

- **Plan Gratuito**: 100GB bandwidth, 1000 requests/día
- **Plan Pro**: $20/mes - Para uso comercial
- **Plan Enterprise**: Contactar ventas

## 🎯 **Ventajas de Vercel**

- ✅ **Despliegue automático** desde GitHub
- ✅ **HTTPS incluido** automáticamente
- ✅ **Edge functions** para mejor performance
- ✅ **Logs en tiempo real**
- ✅ **Métricas detalladas**
- ✅ **Escalado automático**
- ✅ **CDN global**

## 🔄 **Despliegue Automático**

Una vez configurado, cada `git push` a la rama `main` desplegará automáticamente los cambios.

## 📞 **Soporte**

- **Documentación**: [vercel.com/docs](https://vercel.com/docs)
- **Comunidad**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Soporte**: Dashboard > Help

---

¡Tu backend estará listo en minutos! 🚀
