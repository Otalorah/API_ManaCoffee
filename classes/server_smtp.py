from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
import pytz
from datetime import datetime

load_dotenv()
SENDGRID_API_KEY = getenv('SENDGRID_API_KEY')
FROM_EMAIL = getenv('FROM_EMAIL', 'brokerviewes@gmail.com')

class ServerSMTP:
    def __init__(self, templates_path: str = None):
        """
        Inicializa el servidor SMTP con la ruta a las plantillas HTML
        
        Args:
            templates_path: Ruta a la carpeta que contiene las plantillas HTML
        """
        if templates_path is None:
            # Ruta por defecto: retrocede una carpeta y entra a templates/email
            self.templates_path = Path(__file__).parent.parent / 'templates' / 'email'
        else:
            self.templates_path = Path(templates_path)
    
    def send_email_code(self, email: str, code: str):
        """
        Envía un email usando SendGrid API con HTML
        """
        try:
            # Construir el contenido HTML
            html_content = self._load_template('verification_code.html', code=code)
            
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
    
    def send_email_welcome(self, email: str, name: str):
        """
        Envía un email de bienvenida usando SendGrid API con HTML
        """
        try:
            # Construir el contenido HTML de bienvenida
            html_content = self._load_template('welcome.html', name=name)
            
            message = Mail(
                from_email=Email(FROM_EMAIL),
                to_emails=To(email),
                subject='¡Bienvenido a ManaCoffe!',
                html_content=Content("text/html", html_content)
            )
            
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            
            return response
            
        except Exception as e:
            print(f"❌ Error enviando email de bienvenida: {str(e)}")
            raise e
    
    def _load_template(self, template_name: str, **kwargs) -> str:
        """
        Carga una plantilla HTML desde un archivo y reemplaza las variables
        
        Args:
            template_name: Nombre del archivo de plantilla
            **kwargs: Variables a reemplazar en la plantilla
            
        Returns:
            Contenido HTML con variables reemplazadas
        """
        template_path = self.templates_path / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Plantilla no encontrada: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Reemplazar variables en la plantilla
        for key, value in kwargs.items():
            placeholder = f'{{{{{key}}}}}'
            html_content = html_content.replace(placeholder, str(value))
        
        return html_content

    def send_email_reservation(self, email: str, name: str, date, 
                               number_of_people: int, phone: str):
        """
        Envía un email de confirmación de reserva usando SendGrid API con HTML
        
        Args:
            email: Email del cliente
            name: Nombre del cliente
            date: Fecha de la reserva (puede ser string ISO o objeto datetime)
            number_of_people: Número de personas
            phone: Teléfono del cliente
        """

        phone = phone[:3] + " " + phone[3:]

        try:
            # Timezone de Colombia
            colombia_tz = pytz.timezone('America/Bogota')
            
            # Formatear la fecha de manera legible
            try:
                # Si date es un string, convertirlo a datetime
                if isinstance(date, str):
                    # Limpiar el string de fecha
                    if date.endswith('Z'):
                        date_str = date.replace('Z', '+00:00')
                    elif 'T' in date and '+' not in date and '-' not in date.split('T')[1]:
                        date_str = date + '+00:00'
                    else:
                        date_str = date
                    
                    # Parsear como UTC
                    date_obj = datetime.fromisoformat(date_str)
                    
                    # Si la fecha es naive (sin timezone), asumirla como UTC
                    if date_obj.tzinfo is None:
                        date_obj = pytz.utc.localize(date_obj)
                    
                    # Convertir a hora de Colombia
                    date_obj = date_obj.astimezone(colombia_tz)
                else:
                    # Si ya es un objeto datetime, usarlo directamente
                    date_obj = date
                    if date_obj.tzinfo is None:
                        date_obj = pytz.utc.localize(date_obj)
                    date_obj = date_obj.astimezone(colombia_tz)
                
                # Configurar nombres de meses en español
                meses = {
                    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
                    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
                }
                
                formatted_date = f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"
                formatted_time = date_obj.strftime('%I:%M %p')
                
            except Exception as e:
                print(f"Error al formatear fecha: {e}")
                formatted_date = str(date)
                formatted_time = 'Hora a confirmar'
            
            # Cargar plantilla con los datos
            html_content = self._load_template(
                'reservation.html',
                name=name,
                date=formatted_date,
                time=formatted_time,
                numberOfPeople=number_of_people,
                phone=phone
            )
            
            message = Mail(
                from_email=Email(FROM_EMAIL),
                to_emails=To(email),
                subject='Confirmación de Reserva - ManaCoffe',
                html_content=Content("text/html", html_content)
            )
            
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            
            print(f"✅ Email de confirmación enviado a {email}")
            return response
            
        except Exception as e:
            print(f"❌ Error enviando email de reserva: {str(e)}")
            raise e