from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import profile_collection, projects_collection, skills_collection

app = FastAPI(title="Me-API Playground")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------- PROFILE ----------------
@app.get("/profile")
async def get_profile():
    return await profile_collection.find_one({}, {"_id": 0})

# ---------------- PROJECTS ----------------
@app.get("/projects")
async def get_projects(skill: str | None = None):
    query = {}
    if skill:
        query = {"skills": skill.lower()}

    return [p async for p in projects_collection.find(query, {"_id": 0})]

# ---------------- SEARCH ----------------
@app.get("/search")
async def search(q: str):
    q = q.lower()

    projects = [
        p async for p in projects_collection.find(
            {
                "$or": [
                    {"title": {"$regex": q, "$options": "i"}},
                    {"description": {"$regex": q, "$options": "i"}},
                    {"skills": q}
                ]
            },
            {"_id": 0}
        )
    ]

    skills = [
        s async for s in skills_collection.find(
            {"name": {"$regex": q, "$options": "i"}},
            {"_id": 0}
        )
    ]

    return {
        "projects": projects,
        "skills": skills
    }

# ---------------- TOP SKILLS ----------------
@app.get("/skills/top")
async def top_skills():
    pipeline = [
        {"$group": {"_id": "$name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]

    skills = await skills_collection.aggregate(pipeline).to_list(None)
    return [{"skill": s["_id"], "count": s["count"]} for s in skills]
