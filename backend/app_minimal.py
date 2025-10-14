from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde el frontend
CORS(app, origins=['*'])

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que la aplicación está funcionando"""
    return jsonify({
        "status": "healthy",
        "message": "Backend funcionando correctamente",
        "timestamp": "2025-10-14T15:55:00Z"
    }), 200

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Endpoint webhook básico"""
    try:
        data = request.json
        logger.info(f"Webhook recibido: {data}")
        
        return jsonify({
            "status": "success",
            "message": "Webhook procesado correctamente",
            "data": data
        }), 200
        
    except Exception as e:
        logger.error(f"Error en webhook: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Endpoint raíz"""
    return jsonify({
        "message": "Backend API funcionando",
        "endpoints": ["/health", "/webhook"]
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

# Para Vercel
def handler(request):
    return app(request)
