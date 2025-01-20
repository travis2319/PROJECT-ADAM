import time
import secrets
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from routers.emissions import router as emissions_router
from routers.engine_health import router as engine_health_router
from routers.predictive_maintenance import router as predictive_maintenance_router
from routers.chatbot import router as chatbot_router

app = FastAPI(
    title="Car Diagnostics API",
    description="API for emissions compliance and engine health analysis.",
    version="2.0.0"
)

security = HTTPBasic(auto_error=True)



def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify HTTP Basic Auth credentials."""
    global CURRENT_USER

    # Required credentials
    correct_username = "user"
    correct_password = "password"  # Replace with your password

    is_username_correct = secrets.compare_digest(credentials.username, correct_username)
    is_password_correct = secrets.compare_digest(credentials.password, correct_password)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    CURRENT_USER = credentials.username
    return CURRENT_USER


# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    global CURRENT_USER
    CURRENT_USER = None  # Reset user on startup

    print("Authenticating connection to database...")

    retries = 5
    while retries > 0:
        try:
            from utils.database import connect_to_db
            conn = connect_to_db()
            conn.close()
            print("✓ Database connection established.")
            break
        except Exception as e:
            print(f"✗ Database connection failed. Retrying... {e}")
            retries -= 1
            time.sleep(5)
    if retries == 0:
        raise Exception("Failed to connect to the database after multiple attempts.")


@app.get("/", tags=["Authentication"])
async def root(username: str = Depends(verify_credentials)):
    """
    Root endpoint to verify authentication status.
    """
    return {
        "message": f"Authenticated as: {username}",
        "status": "operational"
    }


# Include routers with authentication requirement
app.include_router(
    emissions_router,
    dependencies=[Depends(verify_credentials)]
)
app.include_router(
    engine_health_router,
    dependencies=[Depends(verify_credentials)]
)
app.include_router(
    predictive_maintenance_router,
    dependencies=[Depends(verify_credentials)]
)
app.include_router(
    chatbot_router,
    dependencies=[Depends(verify_credentials)]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        force_exit=True
    )