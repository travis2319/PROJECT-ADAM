
import time
from fastapi import FastAPI
from routers.emissions import router as emissions_router
from routers.engine_health import router as engine_health_router
from routers.predictive_maintenance import router as predictive_maintenance_router

app = FastAPI(
    title="Car Diagnostics API",
    description="API for emissions compliance and engine health analysis.",
    version="2.0.0"
)

@app.on_event("startup")
async def startup_event():
    retries = 5
    while retries > 0:
        try:
            from utils.database import connect_to_db
            conn = connect_to_db()
            conn.close()
            print("Database connection established.")
            break
        except Exception as e:
            print(f"Database connection failed. Retrying... {e}")
            retries -= 1
            time.sleep(5)
    if retries == 0:
        raise Exception("Failed to connect to the database.")

@app.get("/")
def root():
    return {"message": "Welcome to the Car Diagnostics API"}

app.include_router(emissions_router)
app.include_router(engine_health_router)
app.include_router(predictive_maintenance_router)