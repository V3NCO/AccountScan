from datetime import timedelta
from typing import Annotated
from accscan.config import settings
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
import jwt
from accscan.auth import authenticate_user, create_access_token, get_user
import accscan.email
import accscan.auth
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username) #type: ignore
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.post("/users/create")
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await accscan.auth.create_user(form_data)

@app.post("/email/account/add")
async def add_user_email(
    current_user: Annotated[User, Depends(get_current_active_user)],
    hostname: str,
    username: str,
    password: str,
    secure: bool
):
    return await accscan.email.add_user_email(current_user, hostname, username, password, secure)

@app.get("/email/account/list")
async def fastapi_account_list(
  current_user: Annotated[User, Depends(get_current_active_user)]
):
    return await accscan.email.list_user_email(current_user)

@app.get("/email/pull")
async def fastapi_email_pull(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    await accscan.email.pull_emails(current_user)
    return {'ok': True}

@app.get("/email/progress/pull")
async def fastapi_email_progpull(
    current_user: Annotated[User, Depends(get_current_active_user)],
    account: str
):
    return await accscan.email.check_progress(current_user, account)
