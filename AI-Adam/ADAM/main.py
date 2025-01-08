from fastapi import FastAPI
from utils.database import Database
from routers.engine_health import router as engine_health_router
from routers.emissions import router as emissions_router
from routers.maintenance import router as maintenance_router
from routers.chatbot import router as chatbot_router

# Initialize FastAPI app
app = FastAPI(
    title="Car Diagnostics and Maintenance API",
    description="An API for engine health prediction, emissions analysis, predictive maintenance, and DTC chatbot.",
    version="1.0.0"
)

# Database connection instance
DATABASE_URL = "postgresql://postgres:mysecretpassword@db:5432/mydb"
db_instance = Database(DATABASE_URL)

# Event handlers for startup and shutdown
@app.on_event("startup")
async def startup_event():
    """
    Event to handle any setup during app startup, like DB connections.
    """
    try:
        # Verify database connection
        with db_instance.engine.connect() as connection:
            connection.execute("SELECT 1")
        print("Database connection established.")
    except Exception as e:
        print(f"Database connection failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event to handle cleanup during app shutdown.
    """
    print("Shutting down application.")

# Include routers
app.include_router(engine_health_router)
app.include_router(emissions_router)
app.include_router(maintenance_router)
app.include_router(chatbot_router)

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Car Diagnostics and Maintenance API!"}
