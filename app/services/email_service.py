"""
Servicio de envío de emails transaccionales (SMTP async via aiosmtplib)

Si SMTP_HOST no está configurado, el token se loguea en consola
para facilitar pruebas en desarrollo.
"""

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from ..core.config import settings

logger = logging.getLogger(__name__)


async def enviar_email_verificacion(email_destino: str, nombre: str, token: str):
    """Envía email con link para verificar la cuenta (expira en 24 horas)"""
    verify_url = f"{settings.BACKEND_URL}/auth/verify-email?token={token}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 0;">
      <div style="background: linear-gradient(135deg, #1a1a1a 0%, #0b6dff 100%);
                  padding: 40px 20px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 32px; letter-spacing: -0.5px;">
          Abogad<span style="color: #93c5fd;">ai</span>
        </h1>
      </div>

      <div style="padding: 40px 30px; background: #ffffff;">
        <h2 style="color: #1a1a1a; margin-top: 0;">Verifica tu cuenta</h2>
        <p style="color: #4a4a4a; line-height: 1.6;">Hola {nombre},</p>
        <p style="color: #4a4a4a; line-height: 1.6;">
          Gracias por registrarte en Abogadai. Para activar tu cuenta,
          haz clic en el botón a continuación:
        </p>

        <div style="text-align: center; margin: 36px 0;">
          <a href="{verify_url}"
             style="background: #0b6dff; color: white; padding: 14px 32px;
                    text-decoration: none; border-radius: 8px; font-weight: bold;
                    font-size: 16px; display: inline-block;">
            Verificar mi email
          </a>
        </div>

        <p style="color: #6a6a6a; font-size: 14px; line-height: 1.6;">
          Este enlace expirará en <strong>24 horas</strong>.
        </p>
        <p style="color: #6a6a6a; font-size: 14px; line-height: 1.6;">
          Si no creaste esta cuenta, puedes ignorar este mensaje.
        </p>
      </div>

      <div style="padding: 20px 30px; background: #f5f5f5; border-top: 1px solid #e0e0e0;">
        <p style="color: #9a9a9a; font-size: 12px; margin: 0;">
          Si el botón no funciona, copia y pega este enlace en tu navegador:<br>
          <a href="{verify_url}" style="color: #0b6dff; word-break: break-all;">{verify_url}</a>
        </p>
      </div>
    </body>
    </html>
    """

    if not settings.SMTP_HOST:
        logger.warning(
            f"[EMAIL_SERVICE] SMTP no configurado. "
            f"Token de verificación para {email_destino}: {token}"
        )
        logger.warning(f"[EMAIL_SERVICE] URL de verificación: {verify_url}")
        return

    message = MIMEMultipart("alternative")
    message["From"] = f"Abogadai <{settings.SMTP_FROM}>"
    message["To"] = email_destino
    message["Subject"] = "Verifica tu cuenta - Abogadai"
    message.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        use_ssl = settings.SMTP_PORT == 465
        use_starttls = settings.SMTP_PORT == 587

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=use_ssl,
            start_tls=use_starttls,
        )
        logger.info(f"[EMAIL_SERVICE] Email de verificación enviado a {email_destino}")
    except Exception as e:
        logger.error(f"[EMAIL_SERVICE] Error enviando email a {email_destino}: {e}")
        raise


async def enviar_email_reset_contrasena(email_destino: str, nombre: str, token: str):
    """Envía email con link para restablecer contraseña (expira en 1 hora)"""
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 0;">
      <div style="background: linear-gradient(135deg, #1a1a1a 0%, #0b6dff 100%);
                  padding: 40px 20px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 32px; letter-spacing: -0.5px;">
          Abogad<span style="color: #93c5fd;">ai</span>
        </h1>
      </div>

      <div style="padding: 40px 30px; background: #ffffff;">
        <h2 style="color: #1a1a1a; margin-top: 0;">Restablece tu contraseña</h2>
        <p style="color: #4a4a4a; line-height: 1.6;">Hola {nombre},</p>
        <p style="color: #4a4a4a; line-height: 1.6;">
          Recibimos una solicitud para restablecer la contraseña de tu cuenta en Abogadai.
          Haz clic en el botón a continuación para crear una nueva contraseña:
        </p>

        <div style="text-align: center; margin: 36px 0;">
          <a href="{reset_url}"
             style="background: #0b6dff; color: white; padding: 14px 32px;
                    text-decoration: none; border-radius: 8px; font-weight: bold;
                    font-size: 16px; display: inline-block;">
            Restablecer contraseña
          </a>
        </div>

        <p style="color: #6a6a6a; font-size: 14px; line-height: 1.6;">
          Este enlace expirará en <strong>1 hora</strong>.
        </p>
        <p style="color: #6a6a6a; font-size: 14px; line-height: 1.6;">
          Si no solicitaste restablecer tu contraseña, puedes ignorar este mensaje.
          Tu contraseña actual no cambiará.
        </p>
      </div>

      <div style="padding: 20px 30px; background: #f5f5f5; border-top: 1px solid #e0e0e0;">
        <p style="color: #9a9a9a; font-size: 12px; margin: 0;">
          Si el botón no funciona, copia y pega este enlace en tu navegador:<br>
          <a href="{reset_url}" style="color: #0b6dff; word-break: break-all;">{reset_url}</a>
        </p>
      </div>
    </body>
    </html>
    """

    # Si SMTP no está configurado, loguear el token (útil en desarrollo)
    if not settings.SMTP_HOST:
        logger.warning(
            f"[EMAIL_SERVICE] SMTP no configurado. "
            f"Token de reset para {email_destino}: {token}"
        )
        logger.warning(f"[EMAIL_SERVICE] URL de reset: {reset_url}")
        return

    message = MIMEMultipart("alternative")
    message["From"] = f"Abogadai <{settings.SMTP_FROM}>"
    message["To"] = email_destino
    message["Subject"] = "Restablece tu contraseña - Abogadai"
    message.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        # Puerto 587 → STARTTLS (start_tls=True, use_tls=False)
        # Puerto 465 → SSL directo (use_tls=True, start_tls=False)
        use_ssl = settings.SMTP_PORT == 465
        use_starttls = settings.SMTP_PORT == 587

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=use_ssl,
            start_tls=use_starttls,
        )
        logger.info(f"[EMAIL_SERVICE] Email de reset enviado a {email_destino}")
    except Exception as e:
        logger.error(f"[EMAIL_SERVICE] Error enviando email a {email_destino}: {e}")
        raise
