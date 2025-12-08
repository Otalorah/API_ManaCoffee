from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from os import getenv
from dotenv import load_dotenv
from pathlib import Path

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