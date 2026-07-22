# verificar_correo.py
"""
Script de diagnóstico -- NO forma parte de la app.
Muestra qué está leyendo tu app del archivo .env, sin revelar la
contraseña completa (para que puedas pegarme el resultado sin
compartir tu credencial real).

Corre esto parado en la raíz del proyecto:
    .venv/Scripts/python.exe verificar_correo.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

remitente = os.environ.get("EMAIL_REMITENTE")
password = os.environ.get("EMAIL_PASSWORD")
host = os.environ.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
puerto = os.environ.get("EMAIL_SMTP_PORT", "587")


def enmascarar(valor):
    if not valor:
        return "❌ NO SE ENCONTRÓ (está vacío o el .env no se está leyendo)"
    if len(valor) <= 4:
        return "*" * len(valor)
    return valor[:2] + "*" * (len(valor) - 4) + valor[-2:]


print("EMAIL_REMITENTE  :", remitente or "❌ NO SE ENCONTRÓ")
print("EMAIL_PASSWORD   :", enmascarar(password))
print("EMAIL_SMTP_HOST  :", host)
print("EMAIL_SMTP_PORT  :", puerto)

if password:
    print()
    print("Longitud de la contraseña:", len(password), "caracteres")
    print("¿Tiene espacios?:", "SÍ (quítalos)" if " " in password else "No")
    print("¿Tiene comillas?:", "SÍ (quítalas)" if ('"' in password or "'" in password) else "No")