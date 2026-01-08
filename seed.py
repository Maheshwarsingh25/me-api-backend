import asyncio
from database import profile_collection, projects_collection, skills_collection

async def seed():
    await profile_collection.delete_many({})
    await projects_collection.delete_many({})
    await skills_collection.delete_many({})

    await profile_collection.insert_one({
        "name": "Your Name",
        "email": "you@email.com",
        "education": "B.Tech Computer Science",
        "links": {
            "github": "https://github.com/yourname",
            "linkedin": "https://linkedin.com/in/yourname",
            "portfolio": "https://yourportfolio.com"
        }
    })

    skills = ["python", "fastapi", "mongodb", "html", "css", "javascript"]
    await skills_collection.insert_many(
        [{"name": s} for s in skills]
    )

    await projects_collection.insert_one({
        "title": "Portfolio Website",
        "description": "Personal portfolio using HTML, CSS, JS",
        "skills": ["html", "css", "javascript"]
    })

    print("MongoDB seeded successfully")

asyncio.run(seed())
