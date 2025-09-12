#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de Resend
"""

import os
from dotenv import load_dotenv
import resend

# Cargar variables de entorno
load_dotenv()

def test_resend_config():
    """Prueba la configuración de Resend"""
    
    # Verificar variables de entorno
    api_key = os.getenv('RESEND_API_KEY')
    from_email = os.getenv('FROM_EMAIL')
    
    print("=== Verificación de configuración Resend ===")
    print(f"RESEND_API_KEY: {'✓ Configurada' if api_key else '✗ No configurada'}")
    print(f"FROM_EMAIL: {'✓ Configurada' if from_email else '✗ No configurada'}")
    
    if not api_key:
        print("\n❌ Error: RESEND_API_KEY no está configurada")
        print("Por favor, configura tu API key de Resend en el archivo .env")
        return False
    
    if not from_email:
        print("\n❌ Error: FROM_EMAIL no está configurada")
        print("Por favor, configura tu email de envío en el archivo .env")
        return False
    
    # Probar conexión con Resend
    try:
        resend.api_key = api_key
        print("\n✓ API key de Resend configurada exitosamente")
        
        # Crear un email de prueba
        test_email = input("\nIngresa un email para prueba (o presiona Enter para omitir): ").strip()
        
        if test_email:
            print(f"\n📤 Enviando email de prueba a {test_email}...")
            
            response = resend.Emails.send({
                "from": from_email,
                "to": [test_email],
                "subject": "🔍 Prueba de configuración Resend",
                "html": """
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #ff433f; text-align: center;">¡Prueba de Resend!</h2>
                        
                        <p>Si recibes este email, Resend está funcionando correctamente.</p>
                        
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3>Detalles de la prueba:</h3>
                            <ul>
                                <li><strong>Servicio:</strong> Resend</li>
                                <li><strong>Remitente:</strong> {}</li>
                                <li><strong>Timestamp:</strong> {}</li>
                            </ul>
                        </div>
                        
                        <p style="font-size: 12px; color: #666; text-align: center;">
                            Este email fue enviado automáticamente por Triario AI
                        </p>
                    </div>
                </body>
                </html>
                """.format(from_email, os.popen('date').read().strip()),
                "text": f"Prueba de Resend - Si recibes este email, todo está funcionando.\n\nRemitente: {from_email}\nTimestamp: {os.popen('date').read().strip()}"
            })
            
            print(f"✓ Email enviado exitosamente!")
            print(f"📋 Response: {response}")
            
            if response and 'id' in response:
                print(f"🆔 Email ID: {response['id']}")
                print("📧 Revisa tu bandeja de entrada (y spam)")
            else:
                print("⚠️ Respuesta inesperada de Resend")
                
        else:
            print("✓ Configuración de Resend correcta (sin envío de prueba)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error conectando con Resend: {str(e)}")
        return False

def show_resend_info():
    """Muestra información sobre Resend"""
    print("\n" + "="*50)
    print("📚 INFORMACIÓN SOBRE RESEND")
    print("="*50)
    print("✅ Plan gratuito: 3,000 emails por mes")
    print("✅ API súper simple y moderna")
    print("✅ Excelente deliverability")
    print("✅ Perfecto para desarrolladores")
    print("\n🔗 Enlaces útiles:")
    print("• Dashboard: https://resend.com/dashboard")
    print("• Documentación: https://resend.com/docs")
    print("• API Keys: https://resend.com/api-keys")

if __name__ == "__main__":
    show_resend_info()
    test_resend_config()
