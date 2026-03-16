"""
Category and tag seeders
"""
from sqlalchemy.orm import Session
from app.models.blog import Category, Tag


def seed_categories(db: Session):
    """Seed categories table"""
    categories_data = [
        {"name": "Technology", "slug": "technology"},
        {"name": "Programming", "slug": "programming"},
        {"name": "Web Development", "slug": "web-development"},
        {"name": "Mobile Development", "slug": "mobile-development"},
        {"name": "DevOps", "slug": "devops"},
        {"name": "Tutorial", "slug": "tutorial"},
    ]
    
    for category_data in categories_data:
        existing_category = db.query(Category).filter(
            Category.slug == category_data["slug"]
        ).first()
        
        if not existing_category:
            category = Category(**category_data)
            db.add(category)
    
    db.commit()
    print("✅ Categories seeded successfully")


def seed_tags(db: Session):
    """Seed tags table"""
    tags_data = [
        {"name": "Python", "slug": "python"},
        {"name": "FastAPI", "slug": "fastapi"},
        {"name": "JavaScript", "slug": "javascript"},
        {"name": "React", "slug": "react"},
        {"name": "Vue.js", "slug": "vuejs"},
        {"name": "Node.js", "slug": "nodejs"},
        {"name": "Docker", "slug": "docker"},
        {"name": "Kubernetes", "slug": "kubernetes"},
        {"name": "AWS", "slug": "aws"},
        {"name": "API", "slug": "api"},
    ]
    
    for tag_data in tags_data:
        existing_tag = db.query(Tag).filter(Tag.slug == tag_data["slug"]).first()
        
        if not existing_tag:
            tag = Tag(**tag_data)
            db.add(tag)
    
    db.commit()
    print("✅ Tags seeded successfully")
