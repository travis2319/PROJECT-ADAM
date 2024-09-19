from fastapi import APIRouter, HTTPException
from utils.chromadb_client import chroma_client

clear_router = APIRouter()


@clear_router.delete("/clear-vectordb/")
async def clear_vectordb():
    try:
        # Delete the entire collection from ChromaDB
        chroma_client.delete_collection(name="csv_data")
        return {"detail": "All data cleared from the collection"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")
