# utils/notificaciones.py


import json
import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

RUTA_PREFERENCIAS = "data/notificaciones.json"

PREFERENCIAS_POR_DEFECTO = {
    "activo": False,
    "correo_destino": "",
    "ultimo_nivel_notificado": "ok",
}

# Orden de severidad para saber si el estado "empeoró" respecto al último aviso
ORDEN_SEVERIDAD = {"ok": 0, "atencion": 1, "critico": 2}


def cargar_preferencias():

    if not os.path.exists(RUTA_PREFERENCIAS):
        return PREFERENCIAS_POR_DEFECTO.copy()

    try:
        with open(RUTA_PREFERENCIAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return {**PREFERENCIAS_POR_DEFECTO, **datos}
    except (json.JSONDecodeError, OSError):
        return PREFERENCIAS_POR_DEFECTO.copy()


def guardar_preferencias(preferencias):

    Path("data").mkdir(exist_ok=True)

    with open(RUTA_PREFERENCIAS, "w", encoding="utf-8") as f:
        json.dump(preferencias, f, ensure_ascii=False, indent=2)


def enviar_correo(destinatario, asunto, cuerpo):
    """
    Envía un correo usando credenciales configuradas como variables de
    entorno (ver .env.example):

        EMAIL_REMITENTE  -> el correo que envía (ej: alertas.tuapp@gmail.com)
        EMAIL_PASSWORD   -> contraseña de aplicación (NO tu contraseña normal)
        EMAIL_SMTP_HOST  -> smtp.gmail.com (por defecto)
        EMAIL_SMTP_PORT  -> 587 (por defecto)
    """

    remitente = os.environ.get("EMAIL_REMITENTE")
    password = os.environ.get("EMAIL_PASSWORD")
    host = os.environ.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
    puerto = int(os.environ.get("EMAIL_SMTP_PORT", "587"))

    if not remitente or not password:
        return False, "Faltan EMAIL_REMITENTE y EMAIL_PASSWORD como variables de entorno."

    mensaje = MIMEText(cuerpo)
    mensaje["Subject"] = asunto
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    try:
        with smtplib.SMTP(host, puerto, timeout=10) as servidor:
            servidor.starttls()
            servidor.login(remitente, password)
            servidor.sendmail(remitente, [destinatario], mensaje.as_string())
        return True, "Correo enviado."
    except Exception as e:
        return False, f"No se pudo enviar el correo: {e}"


def revisar_y_notificar(estado):
    

    preferencias = cargar_preferencias()

    nivel_actual = estado["nivel"]
    nivel_anterior = preferencias.get("ultimo_nivel_notificado", "ok")

    empeoro = ORDEN_SEVERIDAD.get(nivel_actual, 0) > ORDEN_SEVERIDAD.get(nivel_anterior, 0)

    resultado = None

    if preferencias["activo"] and preferencias["correo_destino"] and empeoro:

        asunto = f"{estado['icono']} Alerta Agroindustria: {estado['titulo']}"

        cuerpo = (
            f"{estado['titulo']}\n\n"
            f"{estado['mensaje']}\n\n"
            f"Acción recomendada: {estado['accion']}\n\n"
            "— Sistema de monitoreo Agroindustria"
        )

        resultado = enviar_correo(preferencias["correo_destino"], asunto, cuerpo)

    # Siempre actualizamos el último nivel visto (haya o no enviado correo)
    # para poder detectar correctamente el próximo cambio de estado.
    if nivel_actual != nivel_anterior:
        preferencias["ultimo_nivel_notificado"] = nivel_actual
        guardar_preferencias(preferencias)

    return resultado