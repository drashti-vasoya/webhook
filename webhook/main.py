import http

from fastapi import FastAPI, Request
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


@app.post("/webhook/", status_code=http.HTTPStatus.ACCEPTED)
async def webhook(request: Request):
    return {"message": "data"}
