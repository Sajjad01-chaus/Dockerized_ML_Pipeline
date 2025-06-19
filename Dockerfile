FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir \
    fastapi uvicorn[standard] sqlalchemy psycopg2-binary \
    pandas numpy python-dotenv groq

RUN pip install --no-cache-dir \
    sentence-transformers torch chromadb

RUN mkdir -p /app/data /app/logs

COPY src/ ./src/
COPY data/ ./data/

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONPATH=/app

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
