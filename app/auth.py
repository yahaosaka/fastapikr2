from fastapi import APIRouter, Response, Request, HTTPException
from uuid import uuid4
import time
from itsdangerous import Signer, BadSignature
from .models import LoginData

router = APIRouter()

SECRET_KEY = "supersecretkey"
signer = Signer(SECRET_KEY)

SESSION_LIFETIME = 300
EXTEND_THRESHOLD = 180

fake_user = {
    "username": "user123",
    "password": "password123"
}


def create_token(user_id):
    timestamp = int(time.time())
    data = f"{user_id}.{timestamp}"
    return signer.sign(data.encode()).decode()


def parse_token(token):
    try:
        data = signer.unsign(token.encode()).decode()
        user_id, timestamp = data.split(".")
        return user_id, int(timestamp)
    except:
        raise HTTPException(status_code=401, detail="Invalid session")


@router.post("/login")
def login(data: LoginData, response: Response):
    if data.username == fake_user["username"] and data.password == fake_user["password"]:
        user_id = str(uuid4())
        token = create_token(user_id)

        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            max_age=SESSION_LIFETIME
        )
        return {"message": "Logged in"}

    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/profile")
def profile(request: Request, response: Response):
    token = request.cookies.get("session_token")

    if not token:
        raise HTTPException(status_code=401, detail="Session expired")

    user_id, last_time = parse_token(token)
    now = int(time.time())

    diff = now - last_time

    if diff > SESSION_LIFETIME:
        raise HTTPException(status_code=401, detail="Session expired")

    if EXTEND_THRESHOLD <= diff < SESSION_LIFETIME:
        new_token = create_token(user_id)
        response.set_cookie("session_token", new_token, httponly=True)

    return {"user_id": user_id}