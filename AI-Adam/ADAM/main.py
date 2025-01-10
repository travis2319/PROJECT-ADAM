# main.py
from fastapi import FastAPI
from utils.database import Database
from routers import emissions, engine_health, maintenance, chatbot, health
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize the database pool
    Database.initialize()
    yield
    # Shutdown: close all database connections
    Database.close_all()

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(emissions.router)
app.include_router(health.router)
# app.include_router(engine_health.router)
# app.include_router(maintenance.router)
# app.include_router(chatbot.router)

