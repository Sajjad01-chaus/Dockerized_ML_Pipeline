from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from src.config import config

client = chromadb.HttpClient(
    host=config.CHROMA_HOST.replace("http://", "").split(":")[0],
    port=int(config.CHROMA_HOST.split(":")[-1]),
    settings=Settings()
)

collection = client.get_or_create_collection(config.CHROMA_COLLECTION_NAME)
model = SentenceTransformer(config.EMBEDDING_MODEL)

def store_embeddings(data_list):
    docs = [f"{d.get('title', '')} {d.get('description', '')} {d.get('content', '')}" for d in data_list]
    embs = model.encode(docs).tolist()
    ids = [str(d["id"]) for d in data_list]
    collection.delete(ids=ids)
    collection.add(documents=docs, embeddings=embs, ids=ids)

def search_embeddings(query, limit=5):
    query_vec = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_vec,
        n_results=limit,
        include=["documents", "ids"]
    )
    return results
 