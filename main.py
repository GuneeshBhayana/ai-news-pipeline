from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson import json_util
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["ai_news_db"]
articles_col = db["articles"]

@app.get("/")
def read_root():
    return {"message": "Server is running! Access data at /api/news"}

@app.get("/api/news")
def get_news(category: str = None):
    query = {}
    if category:
        query = {"category": category}
    
    # Sort by createdAt descending so newest are always first
    articles = list(articles_col.find(query).sort("createdAt", -1))
    return json.loads(json_util.dumps(articles))