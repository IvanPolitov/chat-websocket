from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from utils.services import UserServices, get_user_services
from schemas.user import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')


async def get_current_user(
        token: str = Depends(oauth2_schema),
        service: UserServices = Depends(get_user_services)
) -> User:
    user = await service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not detected')
    return user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
