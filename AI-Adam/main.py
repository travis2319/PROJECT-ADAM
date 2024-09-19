from fastapi import FastAPI
from routes.csv_routes import csv_router
from routes.diagnosis_routes import diagnosis_router
from routes.display_routes import display_router
from routes.clear_routes import clear_router
from utils.chromadb_client import chroma_client

app = FastAPI()

# Include routers
app.include_router(csv_router, prefix="/api")
app.include_router(diagnosis_router, prefix="/api")
app.include_router(display_router, prefix="/api")
app.include_router(clear_router, prefix="/api")

# Shutdown event to persist ChromaDB data
@app.on_event("shutdown")
def shutdown():
    chroma_client.persist()

# Root route
@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
