import time
import os
import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from pymongo import MongoClient
import urllib.parse

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["ai_news_db"]
articles_col = db["articles"]
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class StructuredArticle(BaseModel):
    title: str = Field(description="A catchy tech article title")
    summary: str = Field(description="A 2-3 sentence short summary")
    content: str = Field(description="The main article body")
    tags: list[str] = Field(description="List of 2-3 relevant technology tags")
    category: str = Field(description="Must be exactly ONE of these words: Science, Environment, International, Technology, or Business")

def fetch_rss_news(search_term):
    # This safely encodes spaces into '+' for the URL
    encoded_query = urllib.parse.quote_plus(search_term)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        response = requests.get(url, timeout=10)
        root = ET.fromstring(response.content)
        articles = []
        # Grab the top 2 articles per category to keep it fast
        for item in root.findall(".//item")[:2]:
            articles.append({
                "title": item.find("title").text,
                "link": item.find("link").text,
                "description": item.find("description").text or ""
            })
        return articles
    except Exception as e:
        print(f"Error fetching RSS for {search_term}: {e}")
        return []

def process_and_store_news():
    # These are the different topics it will search for on Google News
    topics_to_fetch = ["Science", "Environment", "International Relations", "Technology", "Business"]
    
    raw_news = []
    for topic in topics_to_fetch:
        print(f"Fetching news for topic: {topic}...")
        raw_news.extend(fetch_rss_news(topic))

    for news in raw_news:
        if articles_col.find_one({"source_url": news["link"]}):
            continue

        try:
            prompt = f"Rewrite this article and assign it a category. Title: {news['title']} - {news['description']}"
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json", "response_schema": StructuredArticle}
            )
            article_data = json.loads(response.text)
            article_data["source_url"] = news["link"]
            article_data["createdAt"] = datetime.utcnow()
            
            articles_col.insert_one(article_data)
            print(f"Stored [{article_data['category']}]: {article_data['title']}")

            # Cleanup: Keep database at a maximum of 100 articles
            if articles_col.count_documents({}) > 100:
                oldest_article = articles_col.find().sort("createdAt", 1).limit(1)
                for old in oldest_article:
                    articles_col.delete_one({"_id": old["_id"]})

        except Exception as e:
            print(f"Error during AI generation: {e}")
        
        # Pause for 2 seconds to avoid getting blocked by Google Gemini
        time.sleep(2)

if __name__ == "__main__":
    while True:
        print(f"\n--- Pipeline Run: {datetime.now().strftime('%H:%M:%S')} ---")
        process_and_store_news()
        print("Sleeping for 1 hour...")
        time.sleep(3600) # 1 hour