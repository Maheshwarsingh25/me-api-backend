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

    projects = []
    async for p in projects_collection.find(query, {"_id": 0}):
        projects.append(p)

    return projects

# ---------------- SEARCH ----------------
@app.get("/search")
def search(q: str = Query(...)):
    profile = profile_collection.find_one()

    if not profile:
        return {"skills": [], "projects": []}

    q = q.lower()

    skills = [
        skill for skill in profile.get("skills", [])
        if q in skill.lower()
    ]

    projects = [
        project for project in profile.get("projects", [])
        if q in project.get("title", "").lower()
        or q in project.get("description", "").lower()
    ]

    return {
        "skills": skills,
        "projects": projects
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

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Me-API Backend is running"}
