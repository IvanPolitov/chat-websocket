from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from schemas.auth import TokenResponse
from utils.auth import create_jwt
from db.repos import UserRepository
from utils.services import UserServices
from schemas.user import User, UserCreate
from db.base import get_db


user_router = APIRouter(prefix='/login', tags=['login'])
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')


def get_user_services(db: AsyncSession = Depends(get_db)):
    return UserServices(UserRepository(db))


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
