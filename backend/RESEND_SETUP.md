# Configuración de Resend

## 🚀 Pasos para configurar Resend

### 1. Crear cuenta en Resend
1. Ve a [resend.com](https://resend.com)
2. Haz clic en "Get Started"
3. Crea una cuenta gratuita
4. Verifica tu email

### 2. Obtener API Key
1. En el dashboard de Resend, ve a **API Keys**
2. Haz clic en **Create API Key**
3. Dale un nombre (ej: "tavus-app")
4. Selecciona el dominio (o crea uno nuevo)
5. Copia la API key generada

### 3. Configurar variables de entorno
1. Copia `env.example` a `.env`:
   ```bash
   cp env.example .env
   ```

2. Edita el archivo `.env` y configura:
   ```env
   RESEND_API_KEY=re_xxxxxxxxxxxxx
   FROM_EMAIL=tu-email@tudominio.com
   ```

### 4. Verificar dominio (Recomendado)
Para mejor deliverability, verifica tu dominio:
1. Ve a **Domains** en el dashboard
2. Haz clic en **Add Domain**
3. Agrega tu dominio (ej: `tudominio.com`)
4. Agrega los registros DNS que te proporcione Resend
5. Espera la verificación (puede tomar unos minutos)

### 5. Probar la configuración
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar script de prueba
python test_resend.py
```

## ✅ Ventajas de Resend

- **3,000 emails gratuitos por mes** (muy generoso)
- **API súper simple** - Solo necesitas una API key
- **Excelente deliverability** - Los emails llegan a la bandeja de entrada
- **Moderno y rápido** - Diseñado para desarrolladores
- **Documentación excelente** - Muy fácil de usar

## 📊 Límites del plan gratuito

- ✅ 3,000 emails por mes
- ✅ 100 emails por día
- ✅ Soporte por email
- ✅ API completa

## 🔧 Solución de problemas

### Error: "Invalid API key"
- Verifica que la API key esté correctamente copiada
- Asegúrate de que no tenga espacios extra

### Error: "Domain not verified"
- Verifica tu dominio en Resend
- O usa un email verificado individualmente

### Error: "Rate limit exceeded"
- Has alcanzado el límite de 100 emails por día
- Espera hasta el siguiente día o actualiza tu plan

### Email no llega
1. **Revisa la carpeta de SPAM**
2. **Verifica que el dominio esté autenticado**
3. **Revisa los logs en el dashboard de Resend**
4. **Usa un dominio personalizado para mejor deliverability**

## 🆚 Resend vs SendGrid

| Característica | Resend | SendGrid |
|----------------|--------|----------|
| Emails gratuitos/mes | 3,000 | 100 |
| API Key | ✅ Simple | ✅ Simple |
| Deliverability | ✅ Excelente | ✅ Excelente |
| Documentación | ✅ Moderna | ✅ Completa |
| Precio | ✅ Muy económico | ⚠️ Más caro |
| Facilidad de uso | ✅ Súper fácil | ✅ Fácil |

## 🚀 Próximos pasos

1. **Configura tu cuenta** en [resend.com](https://resend.com)
2. **Obtén tu API key** en el dashboard
3. **Configura las variables** en tu archivo `.env`
4. **Prueba la configuración** con `python test_resend.py`
5. **¡Disfruta enviando emails!** 🎉

## 📞 Soporte

- **Documentación:** [resend.com/docs](https://resend.com/docs)
- **Dashboard:** [resend.com/dashboard](https://resend.com/dashboard)
- **Soporte:** Disponible en el dashboard

---

**¡Resend es perfecto para tu aplicación!** 🚀
