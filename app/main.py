from fastapi import FastAPI
from .models import UserCreate
from .products import router as products_router
from .auth import router as auth_router
from .headers import router as headers_router

app = FastAPI()
@app.post("/create_user")
def create_user(user: UserCreate):
    return user
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(headers_router)
@app.get("/")
def read_root():
    return {"message": "sdfsdfdf"}