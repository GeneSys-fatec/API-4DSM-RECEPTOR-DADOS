import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    PORT = int(os.getenv("PORT", 5000))
    DB_NAME = "sensor_data"
    COLLECTION_NAME = "leituras"

def get_db_collection():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.DB_NAME]
    return db[Config.COLLECTION_NAME]