import qrcode

# URL del servidor con un ID único para cada contacto (previsualización)
url_contacto = "http://192.168.253.133:5000/contacto?id=123"

# Generar el código QR con la URL
qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
)
qr.add_data(url_contacto)
qr.make(fit=True)

# Guardar el QR como imagen
img = qr.make_image(fill="black", back_color="white")
img.save("qr_dinamico.png")

print("Código QR dinámico generado como 'qr_dinamico.png'")
