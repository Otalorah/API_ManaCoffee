from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from os import getenv
from dotenv import load_dotenv

load_dotenv()
SENDGRID_API_KEY = getenv('SENDGRID_API_KEY')
FROM_EMAIL = getenv('FROM_EMAIL', 'brokerviewes@gmail.com')

class ServerSMTP:
    def send_email(self, email: str, code: str):
        """
        Envía un email usando SendGrid API con HTML
        """
        try:
            # Construir el contenido HTML
            html_content = self.build_html_template(code)
            
            message = Mail(
                from_email=Email(FROM_EMAIL),
                to_emails=To(email),
                subject='Código de verificación - ManaCoffe',
                html_content=Content("text/html", html_content)
            )
            
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            
            return response
            
        except Exception as e:
            print(f"❌ Error enviando email: {str(e)}")
            raise e
    
    @staticmethod
    def build_html_template(code: str) -> str:
        """
        Construye una plantilla HTML profesional para el email
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Código de Verificación</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #6F4E37 0%, #3E2723 100%); padding: 40px 20px; text-align: center;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 28px;">ManaCoffe</h1>
                                </td>
                            </tr>
                            
                            <!-- Body -->
                            <tr>
                                <td style="padding: 40px 30px;">
                                    <h2 style="color: #333333; margin-top: 0; font-size: 24px;">Código de Verificación</h2>
                                    <p style="color: #666666; font-size: 16px; line-height: 1.5;">
                                        Hemos recibido una solicitud para verificar tu cuenta. Usa el siguiente código para continuar:
                                    </p>
                                    
                                    <!-- Código -->
                                    <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                        <tr>
                                            <td align="center">
                                                <div style="background-color: #FFF8E7; border: 2px dashed #6F4E37; border-radius: 8px; padding: 20px; display: inline-block;">
                                                    <span style="font-size: 32px; font-weight: bold; color: #6F4E37; letter-spacing: 8px; font-family: 'Courier New', monospace;">
                                                        {code}
                                                    </span>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="color: #666666; font-size: 14px; line-height: 1.5;">
                                        Este código expirará en <strong>10 minutos</strong>.
                                    </p>
                                    
                                    <p style="color: #999999; font-size: 13px; line-height: 1.5; margin-top: 30px;">
                                        Si no solicitaste este código, puedes ignorar este mensaje de forma segura.
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8f9fa; padding: 20px 30px; text-align: center; border-top: 1px solid #e9ecef;">
                                    <p style="color: #999999; font-size: 12px; margin: 0;">
                                        © 2025 ManaCoffe. Todos los derechos reservados.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        return html