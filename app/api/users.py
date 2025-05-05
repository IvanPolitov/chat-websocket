from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from schemas.auth import TokenResponse
from utils.utils import create_jwt
from utils.auth import get_admin_user, get_current_user
from utils.services import get_user_services
from utils.services import UserServices
from schemas.user import User, UserCreate


user_router = APIRouter(prefix='/login', tags=['login'])


@user_router.post('/', response_model=TokenResponse)
async def login_user(
    credentials: OAuth2PasswordRequestForm = Depends(),
    service: UserServices = Depends(get_user_services)
):
    db_user = await service.authenticate_user(credentials.username, credentials.password)

    if db_user:
        access_token = create_jwt({'sub': db_user.username, 'role': db_user.role})
        token = TokenResponse(access_token=access_token)
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={"WWW-Authenticate": "Bearer"}
    )


@user_router.post('/register')
async def register_user(
    user: UserCreate,
    service: UserServices = Depends(get_user_services)
):
    user_check = await service.unique_user(user.username)
    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    db_user = await service.register_user(user)
    return {'message': f'{db_user.username} is successfully registered!'}


@user_router.get("/logout")
async def logout():

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@user_router.get("/protected")
async def protected(
    user: User = Depends(get_current_user)
):
    return {'message': f'Hi, {user.role} {user.username}'}


@user_router.get("/admin_protected")
async def admin_protected(
    user: User = Depends(get_admin_user)
):
    return {'message': f'Hi, {user.role} {user.username}'}
