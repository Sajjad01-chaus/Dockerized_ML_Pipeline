import asyncio
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from src.config import config
from src.database import save_to_db, get_all_data, get_by_category, clear_data
from src.data_generator import generate_data

from src.embeddings import store_embeddings, search_embeddings

app = FastAPI()

class GenerateDataRequest(BaseModel):
    num_samples: int

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

@app.post("/generate-data")
async def generate_endpoint(req: GenerateDataRequest):
    try:
        data = await generate_data(req.num_samples)
        save_to_db(data)
        store_embeddings(data)
        return {"message": f"{len(data)} items generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data")
def get_data(category: Optional[str] = Query(None)):
    return get_by_category(category) if category else get_all_data()

@app.post("/search")
def search(req: SearchRequest):
    return search_embeddings(req.query, req.limit)

@app.delete("/data")
def delete_data():
    clear_data()
    return {"message": "All data deleted"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

