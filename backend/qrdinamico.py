from flask import Flask, request, render_template_string

app = Flask(__name__)

# Base de datos simulada
contactos = {
    "123": {
        "nombre": "John Doe",
        "empresa": "Mi Empresa",
        "titulo": "Desarrollador",
        "telefono": "+1234567890",
        "email": "johndoe@email.com",
        "web": "https://miempresa.com",
        "direccion": "Calle Falsa 123, Ciudad, País"
    }
}

@app.route("/contacto")
def obtener_contacto():
    id_contacto = request.args.get("id")
    
    if id_contacto in contactos:
        contacto = contactos[id_contacto]
        
        # Formato vCard en una sola línea para el esquema data:text/vcard
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{contacto["nombre"]}
ORG:{contacto["empresa"]}
TITLE:{contacto["titulo"]}
TEL:{contacto["telefono"]}
EMAIL:{contacto["email"]}
URL:{contacto["web"]}
ADR:;;{contacto["direccion"]}
END:VCARD""".replace("\n", "%0A")  # Codificar saltos de línea para la URL

        vcard_url = f"data:text/vcard;charset=utf-8,{vcard}"  # Generar el esquema data URL

        # Página HTML con botón de importación directa
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Contacto</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
                .card {{ border: 1px solid #ddd; padding: 20px; border-radius: 10px; display: inline-block; }}
                h2 {{ margin-top: 0; }}
                button {{ padding: 10px 15px; font-size: 16px; cursor: pointer; background-color: #28a745; color: white; border: none; border-radius: 5px; }}
                button:hover {{ background-color: #218838; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>{contacto["nombre"]}</h2>
                <p><strong>Empresa:</strong> {contacto["empresa"]}</p>
                <p><strong>Título:</strong> {contacto["titulo"]}</p>
                <p><strong>Teléfono:</strong> {contacto["telefono"]}</p>
                <p><strong>Email:</strong> <a href="mailto:{contacto["email"]}">{contacto["email"]}</a></p>
                <p><strong>Web:</strong> <a href="{contacto["web"]}" target="_blank">{contacto["web"]}</a></p>
                <p><strong>Dirección:</strong> {contacto["direccion"]}</p>
                <a href="{vcard_url}" download="contacto.vcf">
                    <button>Importar Contacto</button>
                </a>
            </div>
        </body>
        </html>
        """
        return render_template_string(html)

    return "Contacto no encontrado", 404


if __name__ == "__main__":
    app.run(host="192.168.253.133", port=5000, debug=True)
