import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime
import requests
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from pymongo import MongoClient

# Load variables
load_dotenv()

# Setup Global Clients so there is no ambiguity
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["ai_news_db"]
articles_col = db["articles"]
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define schema
class StructuredArticle(BaseModel):
    title: str = Field(description="A catchy tech article title")
    summary: str = Field(description="A 2-3 sentence short summary")
    content: str = Field(description="The main article body")
    tags: list[str] = Field(description="List of 2-3 relevant technology tags")

def fetch_rss_news():
    url = "https://news.google.com/rss/search?q=Artificial+Intelligence&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall(".//item")[:1]:
            articles.append({
                "title": item.find("title").text,
                "link": item.find("link").text,
                "description": item.find("description").text or ""
            })
        return articles
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def process_and_store_news():
    raw_news = fetch_rss_news()
    for news in raw_news:
        prompt = f"Rewrite this article: {news['title']} - {news['description']}"
        try:
            # Using the global 'client' directly
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": StructuredArticle,
                }
            )
            article_data = json.loads(response.text)
            article_data["source_url"] = news["link"]
            article_data["createdAt"] = datetime.utcnow()
            articles_col.insert_one(article_data)
            print(f"Stored: {article_data['title']}")
 ##           if not articles_col.find_one({"source_url": news["link"]}):
 ##               articles_col.insert_one(article_data)
 ##               print(f"Stored: {article_data['title']}")
        except Exception as e:
            print(f"Error during AI generation: {e}")
        time.sleep(2)

if __name__ == "__main__":
    process_and_store_news()