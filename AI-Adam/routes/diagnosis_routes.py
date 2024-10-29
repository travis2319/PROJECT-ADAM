from fastapi import APIRouter, HTTPException
from transformers import pipeline
from utils.chromadb_client import collection
from utils.embedding import embedding_function

diagnosis_router = APIRouter()

# Initialize text-generation model
generator = pipeline('text2text-generation', model='google/flan-t5-base', tokenizer='google/flan-t5-base')

@diagnosis_router.post("/diagnosis/")
async def diagnosis(query: str):
    try:
        # Generate the embedding for the query and convert to a list
        embedding_query = embedding_function([query])[0].tolist()

        # Retrieve relevant documents from ChromaDB using the embedding of the query
        results = collection.query(query_embeddings=[embedding_query], n_results=5, include=["documents", "metadatas"])

        if not results.get('documents'):
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        # Extract and format the relevant data from the results (documents and metadata)
        relevant_info = ""
        for doc, metadata in zip(results['documents'], results['metadatas']):
            if isinstance(doc, str) and metadata:
                # Combine relevant fields into a coherent string
                relevant_info += f"Code: {metadata.get('Code', 'N/A')} - {doc}\n"

        # Pass the relevant information to the text generation model with car diagnostic context
        diagnostic_prompt = (
            "You are a car diagnostic service provider. Summarize the following information, which "
            "is related to car diagnostics:\n" + relevant_info
        )

        # Generate text with the context of car diagnostics
        generated_text = generator(diagnostic_prompt, max_length=150, num_return_sequences=1, truncation=True)

        # Return the generated paragraph, ensuring it uses the relevant diagnostic information
        return {"generated_paragraph": generated_text[0]['generated_text']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")
