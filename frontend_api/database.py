from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

mongodb_url = os.getenv("MONGODB_URL")

client = MongoClient(mongodb_url)
db = client.library  # Your MongoDB database
