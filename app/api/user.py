from fastapi import APIRouter, Depends, Request, Response
from schemas.schemas import UserRequest
from db.models import User
from db.base import get_db
from sqlalchemy.orm import Session


user_router = APIRouter()

@user_router.post('/create')
def create_user(
    request: Request,
    user: UserRequest,
    db: Session = Depends(get_db)
):

    new_user = User(name=user.name, ip=request.client.host)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
