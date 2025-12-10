from typing import List
from models.reservations import ReservationData
from classes.google_sheet_reservation import GoogleSheetReservation

sheet = GoogleSheetReservation()

# - - - - - - - - - - - - - - - - - - - - - Funciones Google Sheets - - - - - - - - - - - - - - - - - - - - -

def add_reservation(reservation: ReservationData) -> None:
    values = reservation.to_sheet_values()  
    sheet.write_reservation(values)

def convert_to_dictionary(table: list[list]) -> list[dict]:

    reservations = list()
    columns_name = [
       "name", "email", "phone", "numberOfPeople", "reservationType",
       "timestamp", "date", "reason"]

    for row in table:
        item_dict = dict(zip(columns_name, row))
        item_dict['numberOfPeople'] = int(item_dict['numberOfPeople'])
        reservations.append(item_dict)

    return reservations

def get_reservations_sheet() -> List[ReservationData]:
    reservations = sheet.get_reservations()
    return convert_to_dictionary(reservations)

def update_reservations_sheet(reservations: List[ReservationData]) -> int:
    num_reservations = len(reservations)
    sheet_data = [
        reservation.to_sheet_values()  
        for reservation in reservations
    ]
    sheet.update_reservations(values=sheet_data, num_items=num_reservations)
   
    return num_reservations