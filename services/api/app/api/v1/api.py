from fastapi import APIRouter
from fastapi.routing import APIRoute

from app.api.v1.endpoints import parking_lots
from app.api.v1.endpoints.auth import router as auth_router

def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"

api_router = APIRouter(generate_unique_id_function=custom_generate_unique_id)

api_router.include_router(auth_router)
api_router.include_router(parking_lots.router)
