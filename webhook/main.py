import hashlib
import hmac
import http

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from webhook.core.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()


def generate_hash_signature(
        secret: str,
        payload: str,
        digest_method=hashlib.sha256,
):
    return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), digest_method).hexdigest()


@app.post("/webhook/", status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request):
    if settings.WEBHOOK_SIGNATURE:
        payload = await request.body()
        secret = settings.WEBHOOK_SECRET
        signature = generate_hash_signature(secret, payload.decode())
        if request.headers.get("x_hub_signature") != f"{signature}":
            raise HTTPException(status_code=401, detail="Authentication error.")
    return {"message": "Successfully connected."}
