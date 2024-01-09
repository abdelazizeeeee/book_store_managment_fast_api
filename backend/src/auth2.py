from .config.database import User, database
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from .models.user import *


SECRET_KEY = "211c181bc3ce2efaf4a22945ace128fdc1e3c0cd6271655ca186cad34033eaa4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# db = {
#     "oussema": {
#         "username": "oussema",
#         "full_name": "oussema ben hassena",
#         "email": "oussema@gmail.com",
#         "hashed_password": "$2b$12$wAI4L2U0kluXqK909dUBwOT.Kpj3z3Xk67nT66zXrerleP75Qp5X6",
#         "disabled": False,
#     }
# }


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
db = User


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    query = User.select().where(User.c.username == username)
    username = database.fetch_one(query)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
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
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]


# -----------------------------------------------
# create user


@app.post("/api/user", status_code=status.HTTP_201_CREATED)
async def create_user(user: Users):
    query = User.insert().values(user.dict())

    last_record_id = await database.execute(query)

    return {"message": "user created successfully", "user_id": last_record_id}
