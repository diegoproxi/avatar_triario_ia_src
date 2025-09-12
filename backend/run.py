#!/usr/bin/env python3
"""
Script para ejecutar el servidor Flask del webhook handler
"""

import os
from dotenv import load_dotenv
from app import app

# Cargar variables de entorno desde .env
load_dotenv()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"Iniciando servidor webhook en puerto {port}")
    print(f"Modo debug: {debug}")
    print(f"Webhook endpoint: http://localhost:{port}/webhook")
    print(f"Health check: http://localhost:{port}/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
