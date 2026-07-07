AI News Pipeline

An automated data pipeline that fetches, categorizes, and summarizes AI-related news using the Google Gemini API.

Architecture

Data Ingestion: Polling of Google News RSS feeds across defined topics (Science, Environment, Technology, Business, International).

Processing: Google Gemini 2.5 Flash API generates summaries, assigns categories, and extracts metadata.

Storage: MongoDB Atlas for data persistence. Implements automated document rotation (100-article limit) to manage database size.

API: FastAPI REST endpoints for data retrieval.

Client: Vanilla JavaScript and HTML front-end with Tailwind CSS. Features client-side category filtering and off-site LinkedIn sharing.

Requirements

Python 3.10+

MongoDB cluster

Google Gemini API key

Setup and Execution

Install dependencies:
pip install -r requirements.txt

Configure environment variables in a .env file:
MONGO_URI=your_mongodb_connection_string
GEMINI_API_KEY=your_gemini_api_key

Start the API server:
uvicorn main:app --reload

Start the ingestion scheduler:
python scheduler.py

Open index.html in a web browser to view the client interface.