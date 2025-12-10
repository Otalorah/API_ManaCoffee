from classes.server_smtp import ServerSMTP

server = ServerSMTP()

def send_email_code(email: str, code: str) -> None:
    """
    Envía un email con el código de verificación
    """  
    server.send_email_code(email=email, code=code)

def send_email_welcome(email: str, name: str) -> None:
    server.send_email_welcome(email=email, name=name)

def send_email_reservations(reservation_data: dict) -> None:

     email = reservation_data.get('email')
     name = reservation_data.get('name', 'Cliente')
     date_str = reservation_data.get('date', '')
     number_people = reservation_data.get('numberOfPeople', 1)
     phone = reservation_data.get('phone', 'No especificado')

     server.send_email_reservation(
       email=email,
       name=name,
       date=date_str,
       number_of_people=number_people,
       phone=phone
     )
