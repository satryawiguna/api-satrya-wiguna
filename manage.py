#!/usr/bin/env python
"""
Management commands for the application
"""
import sys
import os
import asyncio
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))


def print_help():
    """Print available commands"""
    print("""
Available commands:
    
    migrate              Run pending migrations
    migrate:fresh        Drop all tables and run migrations
    migrate:rollback     Rollback last migration
    make:migration <name> Create a new migration
    seed                 Run database seeders
    runserver            Start development server
    help                 Show this help message
    
Usage: python manage.py <command>
    """)


def migrate():
    """Run database migrations"""
    os.system("alembic upgrade head")


def migrate_fresh():
    """Drop all tables and run migrations"""
    print("⚠️  Warning: This will drop all tables!")
    confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        os.system("alembic downgrade base")
        os.system("alembic upgrade head")
        print("✅ Fresh migration completed")
    else:
        print("❌ Migration cancelled")


def migrate_rollback():
    """Rollback last migration"""
    os.system("alembic downgrade -1")


def make_migration(name: str):
    """Create a new migration"""
    os.system(f'alembic revision --autogenerate -m "{name}"')


def seed():
    """Run database seeders"""
    from seeders.run_seeders import run_all_seeders
    asyncio.run(run_all_seeders())


def runserver():
    """Start development server"""
    import uvicorn
    from app.core.config import settings
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    commands = {
        "migrate": migrate,
        "migrate:fresh": migrate_fresh,
        "migrate:rollback": migrate_rollback,
        "seed": seed,
        "runserver": runserver,
        "help": print_help,
    }
    
    if command == "make:migration":
        if len(sys.argv) < 3:
            print("❌ Error: Migration name required")
            print("Usage: python manage.py make:migration <migration_name>")
            sys.exit(1)
        make_migration(sys.argv[2])
    elif command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        print_help()
        sys.exit(1)
