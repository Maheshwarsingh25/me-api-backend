import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["me_api"]

profile_collection = db["profile"]
projects_collection = db["projects"]
skills_collection = db["skills"]
