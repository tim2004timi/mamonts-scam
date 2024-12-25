from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
import logging
import asyncio

from .auth.router import router as auth_router
from .users.router import router as users_router
from .events.router import router as events_router
from .teams.router import router as teams_router

from .database import Base
from .config import DEV, origins

from .telegram.bot import main_bot


app = FastAPI(
    title="Mamonts Scam API",
    description="API for bet company",
    version="1.0",
)

main_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_router.include_router(auth_router)
main_router.include_router(users_router)
main_router.include_router(events_router)
main_router.include_router(teams_router)

app.include_router(main_router)


@app.on_event("startup")
async def on_startup():
    app.state.bot_task = asyncio.create_task(main_bot())


@app.on_event("shutdown")
async def on_shutdown():
    app.state.bot_task.cancel()
    try:
        await app.state.bot_task
    except asyncio.CancelledError:
        print("Telegram-бот остановлен.")
