AI News Pipeline
An automated data pipeline designed to ingest, categorize, and summarize AI-related news. The system leverages Large Language Models to transform raw RSS feed data into structured, actionable intelligence.

Live Demo
https://guneeshbhayana.github.io/ai-news-pipeline/

System Architecture
Data Ingestion: An automated module that polls Google News RSS feeds across defined topics, including Science, Environment, Technology, Business, and International Relations.

Intelligence Layer: Integrates the Google Gemini 2.5 Flash API to perform automated summarization, categorical classification, and metadata extraction.

Persistence Layer: Utilizes MongoDB Atlas for data storage. The system incorporates a data rotation policy to maintain a rolling window of the 100 most recent articles.

Service Layer: A FastAPI-based REST API manages data retrieval and facilitates communication between the database and the frontend.

Client Interface: A responsive frontend built with HTML, Tailwind CSS, and Vanilla JavaScript. Features include client-side category filtering and integrated LinkedIn sharing.

Technology Stack
Backend: Python, FastAPI, Pydantic, PyMongo

Frontend: HTML5, Tailwind CSS, JavaScript

AI Integration: Google Gemini 2.5 Flash

Infrastructure: Render (API Hosting), GitHub Pages (Static Hosting)

Requirements
Python 3.10 or higher

MongoDB Atlas cluster

Google Gemini API Key

Setup and Execution
1. Installation
Clone the repository and install the required dependencies:
pip install -r requirements.txt

2. Configuration
Create a .env file in the root directory and configure the following environment variables:
MONGO_URI=your_mongodb_connection_string
GEMINI_API_KEY=your_gemini_api_key

3. Execution
To run the system locally, execute the following components:

API Server: uvicorn main:app --reload

Ingestion Scheduler: python scheduler.py

4. Production Deployment Notes
For deployment, ensure your MongoDB Atlas cluster is configured to allow network access. If connectivity issues arise, whitelist the service IP address in the MongoDB Atlas Network Access settings and restart the deployment on the hosting provider.