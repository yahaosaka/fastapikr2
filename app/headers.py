from fastapi import APIRouter, Request, HTTPException, Header, Depends, Response
from .models import CommonHeaders
import time

router = APIRouter()


@router.get("/headers")
def get_headers(request: Request):
    user_agent = request.headers.get("User-Agent")
    accept_language = request.headers.get("Accept-Language")

    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Missing headers")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }


def get_headers_dep(
    user_agent: str = Header(...),
    accept_language: str = Header(...)
):
    return CommonHeaders(
        user_agent=user_agent,
        accept_language=accept_language
    )


@router.get("/info")
def info(response: Response, headers: CommonHeaders = Depends(get_headers_dep)):
    response.headers["X-Server-Time"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": headers.dict()
    }