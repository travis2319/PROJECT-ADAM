import time
from fastapi import FastAPI
from routers.emissions import router as emissions_router

app = FastAPI(
    title="Emissions Compliance API",
    description="API for extracting data, preprocessing, training, and predicting emissions compliance.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """
    Check the database connection on application startup.
    """
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
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Welcome to the Emissions Compliance API"}

# Include emissions router
app.include_router(emissions_router)
