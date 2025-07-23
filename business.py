from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_urI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME")  # Default if not in .env

client = MongoClient(mongo_urI)
db = client[db_name]
collection = db["Users"]