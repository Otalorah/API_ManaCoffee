from classes.server_smtp import ServerSMTP

server = ServerSMTP()

def send_email_code(email: str, code: str) -> None:
    """
    Envía un email con el código de verificación
    """  
    server.send_email_code(email=email, code=code)

def send_email_welcome(email: str, name: str) -> None:
    server.send_email_welcome(email=email, name=name)