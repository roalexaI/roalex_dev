from flask import Flask, render_template, request, redirect, url_for
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contacto", methods=["POST"])
def contacto():
    # Datos del formulario
    nombre = request.form.get("nombre")
    celular = request.form.get("celular")
    correo = request.form.get("correo")
    comentario = request.form.get("comentario", "")

    # --- CONFIGURACIÓN DE CORREO ---
    # Usa variables de entorno para no hardcodear la clave
    EMAIL_USER = os.getenv("roalexal@outlook.com")  # tu correo de envío (ej: roalexal@outlook.com)
    EMAIL_PASS = os.getenv("112358As.outlook")  # contraseña o app password
    EMAIL_TO = os.getenv("roalexal@outlook.com", EMAIL_USER)  # a dónde se enviará (puede ser el mismo)

    if EMAIL_USER and EMAIL_PASS:
        msg = EmailMessage()
        msg["Subject"] = f"[Roalex.dev] Nuevo contacto de {nombre}"
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO

        cuerpo = f"""
Nuevo mensaje desde la landing Roalex.dev:

Nombre: {nombre}
Celular: {celular}
Correo: {correo}

Comentario:
{comentario}
"""
        msg.set_content(cuerpo)

        # Ejemplo para Outlook (SMTP Office365)
        # Si usas Gmail u otro, cambia el host/puerto
        try:
            with smtplib.SMTP("smtp.office365.com", 587) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
        except Exception as e:
            # Si algo falla, puedes loguearlo en consola
            print("Error enviando correo:", e)

    else:
        print("EMAIL_USER o EMAIL_PASS no configurados")

    # Redirige al inicio con ?ok=1 para mostrar mensaje de éxito
    return redirect(url_for("home", ok=1))


if __name__ == "__main__":
    app.run(debug=True)
