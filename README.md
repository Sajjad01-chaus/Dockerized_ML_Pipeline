# Dockerized_ML_Pipeline

This is a simplified, production-style AI microservice that:
- Uses a GROQ LLM to generate company-related data
- Saves the data into PostgreSQL and as a CSV backup
- Embeds and stores the data in Chroma vector DB
- Provides endpoints for generation, search, retrieval, and deletion

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/dockerized-ml-pipeline.git
cd dockerized-ml-pipeline
```
### 2. Create a .env file
```bash
GROQ_API_KEY=your_actual_groq_key
```
### 3. Build & run the services
```bash
docker compose -f dc_compose.yaml up --build
```
