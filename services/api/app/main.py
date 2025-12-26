from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import get_settings

from app.api.v1.api import api_router

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router, prefix="/api/v1")

origins = settings.cors_origins_list()

# Nota práctica: si usas "*" no combines con credentials=True (navegadores lo bloquean).
allow_credentials = settings.CORS_ALLOW_CREDENTIALS
if origins == ["*"] and allow_credentials:
    allow_credentials = False  # evita una config inválida en browsers

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"] if settings.CORS_ALLOW_METHODS.strip() == "*" else [m.strip() for m in settings.CORS_ALLOW_METHODS.split(",")],
    allow_headers=["*"] if settings.CORS_ALLOW_HEADERS.strip() == "*" else [h.strip() for h in settings.CORS_ALLOW_HEADERS.split(",")],
)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

