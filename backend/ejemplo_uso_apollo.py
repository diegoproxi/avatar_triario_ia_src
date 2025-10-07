#!/usr/bin/env python3
"""
Ejemplo de uso del enriquecimiento de datos de Apollo
Este script muestra cómo usar la funcionalidad de enriquecimiento paso a paso
"""

import os
import sys
import json
import logging
from datetime import datetime

# Agregar el directorio backend al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.apollo import enrich_company_data

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ejemplo_basico():
    """Ejemplo básico de enriquecimiento de datos"""
    
    print("="*60)
    print("EJEMPLO BÁSICO - ENRIQUECIMIENTO DE DATOS CON APOLLO")
    print("="*60)
    
    # Dominio a enriquecer
    dominio = "apollo.io"
    
    print(f"🔍 Enriqueciendo datos para: {dominio}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Realizar enriquecimiento
    resultado = enrich_company_data(dominio)
    
    if resultado.get('success'):
        print("✅ ¡Enriquecimiento exitoso!")
        
        datos = resultado.get('data', {})
        
        # Mostrar información básica
        info_basica = datos.get('informacion_basica', {})
        print(f"\n🏢 EMPRESA: {info_basica.get('nombre', 'N/A')}")
        print(f"🏭 INDUSTRIA: {info_basica.get('industria', 'N/A')}")
        print(f"👥 EMPLEADOS: {info_basica.get('tamaño', 'N/A')}")
        print(f"🌐 SITIO WEB: {info_basica.get('sitio_web', 'N/A')}")
        
        # Mostrar información financiera
        info_financiera = datos.get('financiera', {})
        if info_financiera.get('ingresos_anuales'):
            print(f"💰 INGRESOS: {info_financiera['ingresos_anuales']}")
        
        # Mostrar empleados clave
        empleados = datos.get('empleados_clave', [])
        if empleados:
            print(f"\n👥 EMPLEADOS CLAVE ({len(empleados)}):")
            for i, emp in enumerate(empleados[:3], 1):
                print(f"  {i}. {emp.get('nombre', 'N/A')} - {emp.get('cargo', 'N/A')}")
        
        # Mostrar resumen ejecutivo
        if datos.get('resumen_ejecutivo'):
            print(f"\n📝 RESUMEN EJECUTIVO:")
            print(f"   {datos['resumen_ejecutivo']}")
        
    else:
        print("❌ Error en el enriquecimiento:")
        print(f"   {resultado.get('error', 'Error desconocido')}")

def ejemplo_detallado():
    """Ejemplo detallado mostrando todos los datos disponibles"""
    
    print("\n" + "="*60)
    print("EJEMPLO DETALLADO - TODOS LOS DATOS DISPONIBLES")
    print("="*60)
    
    dominio = "google.com"
    
    print(f"🔍 Enriquecimiento detallado para: {dominio}")
    
    resultado = enrich_company_data(dominio)
    
    if resultado.get('success'):
        datos = resultado.get('data', {})
        datos_raw = resultado.get('raw_data', {})
        
        print("✅ Datos obtenidos exitosamente")
        
        # Mostrar estructura completa
        print(f"\n📊 ESTRUCTURA DE DATOS PROCESADOS:")
        print(json.dumps(datos, indent=2, ensure_ascii=False))
        
        print(f"\n📋 DATOS RAW DE APOLLO (primeros 1000 caracteres):")
        raw_str = json.dumps(datos_raw, indent=2, ensure_ascii=False)
        print(raw_str[:1000] + "..." if len(raw_str) > 1000 else raw_str)
        
    else:
        print("❌ Error obteniendo datos detallados")

def ejemplo_multiple_dominios():
    """Ejemplo con múltiples dominios"""
    
    print("\n" + "="*60)
    print("EJEMPLO MÚLTIPLE - VARIOS DOMINIOS")
    print("="*60)
    
    dominios = [
        ("microsoft.com", "Microsoft"),
        ("apple.com", "Apple"),
        ("openai.com", "OpenAI")
    ]
    
    resultados = []
    
    for dominio, nombre in dominios:
        print(f"\n🔍 Procesando: {nombre} ({dominio})")
        
        resultado = enrich_company_data(dominio)
        resultados.append((nombre, dominio, resultado))
        
        if resultado.get('success'):
            datos = resultado.get('data', {})
            info_basica = datos.get('informacion_basica', {})
            print(f"  ✅ {info_basica.get('nombre', nombre)} - {info_basica.get('industria', 'N/A')}")
        else:
            print(f"  ❌ Error: {resultado.get('error', 'Desconocido')}")
    
    # Resumen
    print(f"\n📊 RESUMEN:")
    exitosos = sum(1 for _, _, r in resultados if r.get('success'))
    print(f"  ✅ Exitosos: {exitosos}/{len(resultados)}")
    print(f"  ❌ Fallidos: {len(resultados) - exitosos}/{len(resultados)}")

def main():
    """Función principal"""
    
    print("🚀 EJEMPLOS DE USO - ENRIQUECIMIENTO DE DATOS APOLLO")
    print("Este script muestra diferentes formas de usar el enriquecimiento de datos")
    print("")
    
    try:
        # Ejecutar ejemplos
        ejemplo_basico()
        ejemplo_detallado()
        ejemplo_multiple_dominios()
        
        print("\n" + "="*60)
        print("🎉 EJEMPLOS COMPLETADOS")
        print("="*60)
        print("")
        print("💡 Para más información:")
        print("  - Revisa APOLLO_LOGS_GUIDE.md")
        print("  - Ejecuta: python test_apollo_detailed_logs.py")
        print("  - Usa el endpoint: POST /api/test-apollo")
        
    except KeyboardInterrupt:
        print("\n⏹️  Ejemplos interrumpidos por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {str(e)}")
        logger.error(f"Error en main: {str(e)}")

if __name__ == "__main__":
    main()
