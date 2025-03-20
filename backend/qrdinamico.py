# qrdinamico.py
from flask import Flask, request, render_template_string, abort
import hmac
import hashlib
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os

app = Flask(__name__)

# Configuración de seguridad
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'clave_secreta_por_defecto').encode('utf-8')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Configurar Talisman para cabeceras de seguridad
Talisman(
    app,
    content_security_policy=None,
    force_https=True,
    strict_transport_security=True,
    frame_options='DENY'
)

# Configurar logging
logging.basicConfig(
    filename='access.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Configurar rate limiting
limiter = Limiter(
    app=app,
    key_func=lambda: request.args.get('id', 'global'),
    storage_uri="memory://",
    default_limits=["200 per day", "50 per hour"]
)

# Base de datos de contactos con firmas precalculadas
contactos = {
    "123": {
        "firma": None,  # Se calculará al iniciar
        "datos": {
            "nombre": "John Doe",
            "empresa": "Tech Corp",
            "telefono": "+1234567890",
            "email": "john@techcorp.com",
            "web": "https://techcorp.com",
            "direccion": "123 Tech Street, Silicon Valley"
        }
    }
}

def generar_firma_hmac(id_contacto):
    """Genera firma HMAC-SHA256 para un ID de contacto"""
    return hmac.new(
        app.secret_key,
        id_contacto.encode(),
        hashlib.sha256
    ).hexdigest()

# Precalcular firmas al iniciar el servidor
for contacto_id in contactos:
    contactos[contacto_id]['firma'] = generar_firma_hmac(contacto_id)

def validar_hmac(f):
    """Decorador para validar HMAC en las solicitudes"""
    def wrapper(*args, **kwargs):
        id_contacto = request.args.get('id')
        firma_recibida = request.args.get('firma')
        
        # Validar parámetros básicos
        if not id_contacto or not firma_recibida:
            logging.warning(f"Parámetros faltantes desde {request.remote_addr}")
            abort(400)
            
        # Validar formato del ID
        if not id_contacto.isalnum() or len(id_contacto) > 20:
            logging.warning(f"ID inválido recibido: {id_contacto}")
            abort(400)
        
        # Validar firma HMAC
        firma_correcta = contactos.get(id_contacto, {}).get('firma')
        if not firma_correcta or not hmac.compare_digest(firma_correcta, firma_recibida):
            logging.warning(f"Intento de acceso no autorizado a {id_contacto} desde {request.remote_addr}")
            abort(403)
            
        return f(*args, **kwargs)
    return wrapper

@app.route('/contacto')
@validar_hmac
@limiter.limit("10/minute")  # Límite adicional para este endpoint
def mostrar_contacto():
    id_contacto = request.args.get('id')
    contacto = contactos.get(id_contacto)
    
    if not contacto:
        logging.error(f"Contacto no encontrado: {id_contacto}")
        abort(404)
        
    logging.info(f"Acceso autorizado a {id_contacto} desde {request.remote_addr}")
    return generar_pagina_contacto(contacto['datos'])

def generar_pagina_contacto(datos):
    """Genera la página HTML con los datos del contacto"""
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contacto - {datos['nombre']}</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', system-ui;
                max-width: 800px;
                margin: 2rem auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .card {{
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 15px rgba(0,0,0,0.1);
                padding: 2rem;
            }}
            h1 {{ color: #2c3e50; }}
            .info-section {{ margin: 1.5rem 0; }}
            .btn-download {{
                background: #3498db;
                color: white;
                padding: 12px 25px;
                border-radius: 25px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s;
            }}
            .btn-download:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(52,152,219,0.4);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>{datos['nombre']}</h1>
            <div class="info-section">
                <p><strong>Empresa:</strong> {datos['empresa']}</p>
                <p><strong>Teléfono:</strong> <a href="tel:{datos['telefono']}">{datos['telefono']}</a></p>
                <p><strong>Email:</strong> <a href="mailto:{datos['email']}">{datos['email']}</a></p>
                <p><strong>Sitio Web:</strong> <a href="{datos['web']}" target="_blank">{datos['web']}</a></p>
                <p><strong>Dirección:</strong> {datos['direccion']}</p>
            </div>
            <a href="{generar_vcard(datos)}" class="btn-download" download="contacto.vcf">
                Descargar Contacto
            </a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

def generar_vcard(datos):
    """Genera contenido vCard con validación básica"""
    vcard_content = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{datos.get('nombre', '')}",
        f"ORG:{datos.get('empresa', '')}",
        f"TEL;TYPE=WORK,VOICE:{datos.get('telefono', '')}",
        f"EMAIL;TYPE=WORK:{datos.get('email', '')}",
        f"URL:{datos.get('web', '')}",
        f"ADR;TYPE=WORK:;;{datos.get('direccion', '')}",
        "END:VCARD"
    ]
    return "data:text/vcard;charset=utf-8," + "%0A".join(vcard_content)

@app.errorhandler(400)
def bad_request(error):
    return "Solicitud incorrecta", 400

@app.errorhandler(403)
def forbidden(error):
    return "Acceso no autorizado", 403

@app.errorhandler(404)
def not_found(error):
    return "Contacto no encontrado", 404

@app.errorhandler(429)
def ratelimit_handler(error):
    return "Demasiadas solicitudes. Por favor intente más tarde.", 429

if __name__ == '__main__':
    app.run(
        host=os.environ.get('FLASK_HOST', '192.168.253.133'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    )
