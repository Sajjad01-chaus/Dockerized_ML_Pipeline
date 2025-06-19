import json
import asyncio
from groq import Groq
from src.config import config

client = Groq(api_key=config.GROQ_API_KEY)

topics = [
    "AI startups", "Fintech", "Healthcare", "Edtech", 
    "Energy", "Ecommerce", "Cybersecurity", "IoT", "Blockchain"
]

def build_prompt(topic, id):
    return f"""
Generate a JSON company profile.

Topic: {topic}
ID: {id}

{{
  "id": {id},
  "title": "Company {id}",
  "description": "Short description",
  "category": "technology",
  "tags": ["a", "b"],
  "content": "Detailed info about company {id}",
  "industry": "Industry",
  "founded_year": 2023,
  "location": "City, Country"
}}
"""

async def generate_one(id):
    topic = topics[id % len(topics)]
    prompt = build_prompt(topic, id)
    try:
        res = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        content = res.choices[0].message.content
        json_str = content[content.find("{"):content.rfind("}")+1]
        return json.loads(json_str)
    except:
        return {
            "id": id,
            "title": f"Fallback {id}",
            "description": "Error fallback",
            "category": "unknown",
            "tags": [],
            "content": "No content",
            "industry": "N/A",
            "founded_year": 2023,
            "location": "N/A"
        }

async def generate_data(n):
    n = min(n, config.MAX_BATCH_SIZE)
    tasks = [generate_one(i + 1) for i in range(n)]
    return await asyncio.gather(*tasks)
