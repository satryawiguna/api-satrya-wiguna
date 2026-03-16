"""
Run all seeders
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from seeders.user_seeder import seed_roles, seed_users, seed_user_roles
from seeders.category_tag_seeder import seed_categories, seed_tags
from seeders.skill_seeder import seed_skills


async def run_all_seeders():
    """Run all database seeders"""
    db = SessionLocal()
    
    try:
        print("\n🌱 Starting database seeding...\n")
        
        # Seed in order of dependencies
        seed_roles(db)
        seed_users(db)
        seed_user_roles(db)
        seed_categories(db)
        seed_tags(db)
        seed_skills(db)
        
        print("\n✅ All seeders completed successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {str(e)}\n")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_all_seeders())
