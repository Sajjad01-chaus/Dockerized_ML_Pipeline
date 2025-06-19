import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama3-70b-8192"
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@postgres:5432/ml_service")
    CHROMA_HOST = os.getenv("CHROMA_HOST", "http://chroma:8000")
    CHROMA_COLLECTION_NAME = "generated_data"
    CSV_FILE_PATH = "/app/data/generated_data.csv"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_BATCH_SIZE = 200
    API_HOST = "0.0.0.0"
    API_PORT = 8080

    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY")

config = Config()
