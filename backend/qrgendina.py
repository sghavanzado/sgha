# qrgendina.py
import qrcode
import hmac
import hashlib

# Configuración (DEBE COINCIDIR CON EL SERVIDOR)
SECRET_KEY = b'tu_super_secreto_complejo'
DOMINIO = "http://192.168.253.133"
CONTACT_ID = "123"

def generar_firma_hmac(id_contacto):
    return hmac.new(
        SECRET_KEY,
        id_contacto.encode(),
        hashlib.sha256
    ).hexdigest()

firma = generar_firma_hmac(CONTACT_ID)
url_segura = f"{DOMINIO}/contacto?id={CONTACT_ID}&firma={firma}"

# Configuración simplificada
qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=4
)

try:
    qr.add_data(url_segura)
    qr.make(fit=True)
    
    # Generar PNG estándar
    img = qr.make_image(fill_color="navy", back_color="white")
    img.save("qr_contacto_seguro.png")
    
    print("QR generado exitosamente como PNG")
    print(f"Ruta: qr_contacto_seguro.png")

except Exception as e:
    print(f"Error: {str(e)}")