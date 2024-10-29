from fastapi import APIRouter, HTTPException
from utils.chromadb_client import collection

display_router = APIRouter()

@display_router.get("/display/")
async def display():
    try:
        # Fetch all data stored in the collection (documents, metadata, embeddings)
        all_data = collection.get(include=["documents", "metadatas", "embeddings"])

        if not all_data or not all_data.get('documents'):
            return {"detail": "No data in the collection"}

        # Prepare the data to be displayed in a structured format
        table_data = []
        for doc, metadata, vector in zip(all_data['documents'], all_data['metadatas'], all_data.get('embeddings', [])):
            vector = vector.tolist() if vector is not None else "No vector"
            table_data.append({
                "document": doc,
                "metadata": metadata,
                "vector": vector
            })

        # Return the structured data as response
        return {"data": table_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
