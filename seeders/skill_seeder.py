"""
Skill seeder
"""
from sqlalchemy.orm import Session
from app.models.other import Skill


def seed_skills(db: Session):
    """Seed skills table"""
    skills_data = [
        {"name": "Python", "category": "Backend", "level": 90, "icon": "python", "sort_order": 1},
        {"name": "FastAPI", "category": "Backend", "level": 85, "icon": "fastapi", "sort_order": 2},
        {"name": "Django", "category": "Backend", "level": 80, "icon": "django", "sort_order": 3},
        {"name": "JavaScript", "category": "Frontend", "level": 85, "icon": "javascript", "sort_order": 4},
        {"name": "TypeScript", "category": "Frontend", "level": 80, "icon": "typescript", "sort_order": 5},
        {"name": "React", "category": "Frontend", "level": 85, "icon": "react", "sort_order": 6},
        {"name": "Vue.js", "category": "Frontend", "level": 75, "icon": "vue", "sort_order": 7},
        {"name": "Docker", "category": "DevOps", "level": 80, "icon": "docker", "sort_order": 8},
        {"name": "Kubernetes", "category": "DevOps", "level": 70, "icon": "kubernetes", "sort_order": 9},
        {"name": "PostgreSQL", "category": "Database", "level": 85, "icon": "postgresql", "sort_order": 10},
        {"name": "MySQL", "category": "Database", "level": 85, "icon": "mysql", "sort_order": 11},
        {"name": "MongoDB", "category": "Database", "level": 75, "icon": "mongodb", "sort_order": 12},
    ]
    
    for skill_data in skills_data:
        existing_skill = db.query(Skill).filter(
            Skill.name == skill_data["name"],
            Skill.category == skill_data["category"]
        ).first()
        
        if not existing_skill:
            skill = Skill(**skill_data)
            db.add(skill)
    
    db.commit()
    print("✅ Skills seeded successfully")
