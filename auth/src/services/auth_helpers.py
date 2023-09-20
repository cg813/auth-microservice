from typing import Optional, Union
from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi import Cookie, HTTPException, status

from src import pwd_context
from src.config import settings
from src.documents import User


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str) -> Union[User, bool]:
    user = await User.find_one(User.email == email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token:str = Cookie(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.find_one(User.email == email)
    if user is None:
        raise credentials_exception
    return user
