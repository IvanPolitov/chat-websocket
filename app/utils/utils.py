from fastapi import status, HTTPException
from datetime import datetime, timedelta
import os
from typing import Dict
from base64 import urlsafe_b64encode, urlsafe_b64decode
import jwt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey


ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = 'SECRET_KEY'
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием алгоритма PBKDF2HMAC.

    Parameters
    ----------
    password : str
        Пароль, который нужно хешировать.

    Returns
    -------
    str
        Хеш пароля в виде строки base64, включающей соль и хеш.

    Notes
    -----
    Функция генерирует случайную соль длиной 16 байт и использует алгоритм PBKDF2HMAC с SHA256,
    длиной ключа 32 байта и 10000 итераций. Хеш пароля и соль объединяются и кодируются в строку base64.

    Examples
    --------
    >>> hashed_password = hash_password("my_secure_password")
    >>> print(hashed_password)
    '...'
    """
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )

    password_bytes = password.encode('utf-8')
    key = kdf.derive(password_bytes)  # Вычисляется хеш пароля

    hashed_password = urlsafe_b64encode(salt + key).decode('utf-8')
    return hashed_password


def verify_password(stored_password_hash: str, input_password: str) -> bool:
    """
    Проверяет, соответствует ли предоставленный пароль хешу.

    Parameters
    ----------
    stored_password_hash : str
        Хеш сохраненного пароля в виде строки base64, включающей соль и хеш.
    input_password : str
        Пароль, который нужно проверить.

    Returns
    -------
    bool
        True, если предоставленный пароль соответствует хешу, иначе False.

    Notes
    -----
    Функция расшифровывает строку base64, извлекает соль и хеш пароля, затем создаёт экземпляр PBKDF2HMAC с теми же параметрами,
    что и при хешировании, и проверяет, соответствует ли предоставленный пароль хешу.

    Examples
    --------
    >>> hashed_password = hash_password("my_secure_password")
    >>> is_correct = verify_password(hashed_password, "my_secure_password")
    >>> print(is_correct)
    True

    >>> is_incorrect = verify_password(hashed_password, "wrong_password")
    >>> print(is_incorrect)
    False
    """
    try:
        salt_and_key = urlsafe_b64decode(stored_password_hash.encode('utf-8'))
    except Exception:
        return False

    salt = salt_and_key[:16]
    key = salt_and_key[16:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )

    input_password_bytes = input_password.encode('utf-8')

    try:
        kdf.verify(input_password_bytes, key)
        return True
    except InvalidKey:
        return False


def create_jwt(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_jwt(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized. JWTerror') from e
    return payload


if __name__ == '__main__':
    pass
