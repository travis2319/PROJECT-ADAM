from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from utils.chromadb_client import collection
from utils.embedding import embedding_function
import uuid

csv_router = APIRouter()


@csv_router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Check if data already exists in the collection
    existing_data = collection.count()
    if existing_data > 0:
        return {"detail": "Data already exists in the collection. No need to upload again."}

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    # Read CSV data into a pandas dataframe
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")

    # Store CSV data in Chroma VectorDB
    try:
        for _, row in df.iterrows():
            row_data = row.to_dict()
            row_text = " ".join([f"{key}: {value}" for key, value in row_data.items()])
            document_id = str(uuid.uuid4())

            # Embed the text of the row into a vector and convert to a list
            vector = embedding_function([row_text])[0].tolist()

            # Add the embedded row to the collection with metadata
            collection.add(
                ids=[document_id],
                embeddings=[vector],
                metadatas=[row_data],
                documents=[row_text]
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing data in Chroma: {str(e)}")

    return {"detail": "CSV data uploaded and embedded successfully"}
