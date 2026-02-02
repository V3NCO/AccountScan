import asyncio
import jwt
from accscan.tables import Users
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from accscan.config import settings
from pydantic import BaseModel

from accscan.utils import get_uuid

password_hash = PasswordHash.recommended()

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    public_key: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


async def get_user(username: str):
    is_in_db = await Users.exists().where(Users.username == username)
    if is_in_db:
        user_dict = await Users.select().where(Users.username == username)
        return UserInDB(**user_dict[0])


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    verified = await asyncio.to_thread(verify_password, password, user.hashed_password)
    if not verified:
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_user(form_data):
    if Users.exists().where(Users.username == form_data.username):
        return {"ok": False, "error": "This username is taken!"}
    else:
        try:
            pwd = password_hash.hash(form_data.password)
            uuid = await get_uuid(Users, Users.id)
            await Users.insert(Users(
                id=uuid,
                username=form_data.username,
                hashed_password=pwd
            ))
            return {"ok": True}
        except Exception as error:
            return {"ok": False, "error": error}
