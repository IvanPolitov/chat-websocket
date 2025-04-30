from app.db.repos import UserRepository
from app.schemas.schemas import UserCreate
from app.utils.auth import hash_password, verify_password
from app.schemas.schemas import User


class UserServices:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> User:
        user_data.password = hash_password(user_data.password)
        return await self.user_repo.create(user_data)

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hashed):
            return None
        return user


async def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Не авторизован. В токене нет username")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Не авторизован.") from e

    user = get_user_from_db(username)

    if not user:
        raise HTTPException(status_code=401, detail="Не авторизован. Пользователь не найден в базе данных.")

    return user
