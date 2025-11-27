from classes.server_smtp import ServerSMTP

def send_email(email: str, code: str):
    """
    Envía un email con el código de verificación
    """
    server = ServerSMTP()
    server.send_email(email=email, code=code)