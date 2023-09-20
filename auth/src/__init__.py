import os
import motor.motor_asyncio
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from passlib.context import CryptContext

from .documents import User
from .config import Settings, get_settings, settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_app() -> FastAPI:
    app = FastAPI()

    from .routes import router
    app.include_router(router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup_event():
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        await init_beanie(client['users'], document_models=[User])

    @app.get("/health")
    async def health(sett: Settings = Depends(get_settings)):
        return {
            "ping": "pong!",
            "testing": sett.testing
        }
    return app
