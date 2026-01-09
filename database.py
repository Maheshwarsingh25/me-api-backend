import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/me_api_db")


client = AsyncIOMotorClient(MONGO_URI)
db = client["me_api_db"]

profile_collection = db["profile"]
projects_collection = db["projects"]
skills_collection = db["skills"]
