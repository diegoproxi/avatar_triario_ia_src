# 🧪 Guía de Pruebas - Apollo API Integration

Esta guía te ayudará a probar la integración con Apollo API usando el dominio **triario.com**.

## 📋 Scripts de Prueba Disponibles

### 1. 🔥 Prueba Rápida - Apollo API
```bash
cd backend
python test_apollo_quick.py
```
**Propósito**: Prueba rápida solo de Apollo API para verificar que funciona.

### 2. 🧪 Prueba Completa - Python
```bash
cd backend
python test_apollo_integration.py
```
**Propósito**: Prueba completa de toda la integración incluyendo backend.

### 3. 🌐 Prueba con Curl - Bash
```bash
cd backend
./test_curl_commands.sh
```
**Propósito**: Pruebas usando curl para simular peticiones HTTP reales.

### 4. 🖥️ Prueba Frontend - HTML
```bash
# Abrir en navegador
open test_frontend_integration.html
```
**Propósito**: Interfaz web para probar la integración completa.

## 🚀 Cómo Ejecutar las Pruebas

### Opción 1: Prueba Rápida (Solo Apollo)
```bash
cd backend
python test_apollo_quick.py
```

**Salida esperada:**
```
🔍 Probando Apollo API con triario.com...
✅ Apollo API funciona correctamente
📋 Empresa: Triario
🏢 Industria: Information Technology & Services
👥 Empleados: 11-50
🌐 Sitio web: https://triario.com
💻 Tecnologías: React, Node.js, JavaScript
👨‍💼 Empleados encontrados: 5
   - Juan Pérez: CEO
   - María García: CTO
   - Carlos López: CMO
```

### Opción 2: Prueba Completa (Recomendada)

**Paso 1**: Iniciar el backend
```bash
cd backend
python run.py
```

**Paso 2**: En otra terminal, ejecutar pruebas
```bash
cd backend
python test_apollo_integration.py
```

**Salida esperada:**
```
============================================================
 SCRIPT DE PRUEBAS - APOLLO API INTEGRATION
============================================================
🕐 Fecha: 2024-01-15 10:30:45
🎯 Dominio a probar: triario.com
🌐 Backend URL: http://localhost:5003

============================================================
 PRUEBA DIRECTA DE APOLLO API
============================================================
🔍 Consultando Apollo API para dominio: triario.com
✅ Respuesta exitosa de Apollo API
📋 INFORMACIÓN BÁSICA:
   Nombre: Triario
   Descripción: AI-powered customer engagement platform
   Industria: Information Technology & Services
   Empleados: 11-50
   Sitio web: https://triario.com
   Tecnologías: React, Node.js, JavaScript, Python, AWS

============================================================
 PRUEBA ENDPOINT BACKEND - ENRICH CONTEXT
============================================================
✅ Contexto enriquecido creado exitosamente

📋 CONTEXTO GENERADO:
----------------------------------------
=== INFORMACIÓN DEL PROSPECTO ===
Nombre: Juan Pérez
Email: juan@triario.com
Rol: CEO
Empresa: Triario

=== INFORMACIÓN DE LA EMPRESA ===
Empresa: Triario
Descripción: AI-powered customer engagement platform
Industria: Information Technology & Services
Número de empleados: 11-50
Año de fundación: 2020
Sitio web: https://triario.com

=== INFORMACIÓN FINANCIERA ===
Ingresos anuales: $1M-$5M
Tecnologías: React, Node.js, JavaScript, Python, AWS

=== INSTRUCCIONES PARA EL AGENTE ===
Usa esta información para personalizar la conversación...
----------------------------------------

============================================================
 RESUMEN DE PRUEBAS
============================================================
   ✅ PASS - Apollo API Directa
   ✅ PASS - Backend Health Check
   ✅ PASS - Endpoint Enrich Context
   ✅ PASS - Endpoint Prospect + Enrichment

📊 RESULTADO FINAL: 4/4 pruebas exitosas
🎉 ¡Todas las pruebas pasaron! La integración está funcionando correctamente.
```

### Opción 3: Prueba con Interfaz Web

1. Abrir `test_frontend_integration.html` en el navegador
2. Verificar que el backend esté ejecutándose
3. Hacer clic en "🚀 Probar Integración Completa"
4. Ver los resultados en tiempo real

## 🔧 Troubleshooting

### Error: "Backend no está ejecutándose"
```bash
cd backend
python run.py
```

### Error: "Connection refused"
- Verificar que el backend esté en el puerto 5003
- Cambiar la URL en los scripts si es necesario

### Error: "Apollo API no responde"
- Verificar la API key de Apollo
- Verificar conexión a internet
- Probar con otro dominio

### Error: "No se encontraron datos"
- Verificar que el dominio sea correcto
- Probar con otro dominio conocido

## 📊 Interpretación de Resultados

### ✅ Pruebas Exitosas
- **Apollo API Directa**: La API de Apollo responde correctamente
- **Backend Health Check**: El servidor backend está funcionando
- **Endpoint Enrich Context**: Se genera contexto enriquecido
- **Endpoint Prospect + Enrichment**: Se crea prospecto con datos enriquecidos

### ❌ Pruebas Fallidas
- **Apollo API**: Problema de conectividad o API key
- **Backend**: Servidor no ejecutándose o configuración incorrecta
- **Endpoints**: Error en la lógica del backend

## 🎯 Datos de Prueba

**Dominio**: `triario.com`
**Empresa**: Triario
**Industria**: Information Technology & Services
**Tamaño**: 11-50 empleados
**Tecnologías**: React, Node.js, JavaScript, Python, AWS

## 📝 Logs y Debugging

Para ver logs detallados del backend:
```bash
cd backend
python run.py
# Los logs aparecerán en la consola
```

Para ver logs de Apollo API:
- Los scripts muestran las respuestas completas
- Usar `jq` para formatear JSON: `echo 'response' | jq .`

## 🚀 Próximos Pasos

Una vez que las pruebas pasen:

1. **Integrar en producción**: Desplegar el backend con Apollo API
2. **Configurar variables de entorno**: API keys en producción
3. **Monitorear**: Verificar logs de Apollo API y backend
4. **Optimizar**: Ajustar timeouts y manejo de errores según necesidad

## 📞 Soporte

Si encuentras problemas:

1. Revisar los logs del backend
2. Verificar la configuración de Apollo API
3. Probar con dominios conocidos
4. Verificar conectividad de red

---

**¡Las pruebas están listas! 🎉 Ejecuta `python test_apollo_integration.py` para comenzar.**
