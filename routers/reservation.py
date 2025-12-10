from fastapi import APIRouter, status

from typing import List

from models.reservations import ReservationData
from lib.functions_smtp import send_email_reservations
from lib.functions_reservation import add_reservation, get_reservations_sheet, update_reservations_sheet

router = APIRouter()


# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: ReservationData):
    
    add_reservation(reservation)
    send_email_reservations(reservation.model_dump())
    
    return {
        "message": "Reserva creada exitosamente",
        "data": reservation
    }

@router.put("/update", response_model=dict, status_code=status.HTTP_200_OK)
async def update_reservations(reservations: List[ReservationData]) -> dict:

    num_reservations = update_reservations_sheet(reservations)

    return {
        "message": "Reservations updates",
        "num_reservations": num_reservations
    }


@router.get("/", response_model=List[ReservationData], status_code=status.HTTP_200_OK)
async def get_reservations() -> List[ReservationData]:
    return get_reservations_sheet()