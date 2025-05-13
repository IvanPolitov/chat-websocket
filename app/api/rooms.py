from fastapi import APIRouter, Depends, status, HTTPException
from utils.services import get_room_services, RoomServices
from utils.auth import get_current_user
from schemas.user import User
from schemas.room import RoomCreate


rooms_router = APIRouter(prefix='/rooms', tags=['rooms'])


@rooms_router.get('/')
async def get_all_rooms(
    service: RoomServices = Depends(get_room_services),
    current_user: User = Depends(get_current_user)
):

    rooms = await service.get_all_current_user_rooms(current_user.id)

    return rooms


@rooms_router.post('/create')
async def create_room(
    room: RoomCreate,
    current_user: User = Depends(get_current_user),
    service: RoomServices = Depends(get_room_services),
):
    room_check = await service.unique_room(room.name)
    if not room_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room already exist"
        )

    db_room = await service.create_room(room, current_user.id)
    return {'message': f'{db_room.name} is successfully registered!'}
