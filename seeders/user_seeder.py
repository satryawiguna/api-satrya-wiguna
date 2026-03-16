"""
User and role seeders
"""
from sqlalchemy.orm import Session
from app.models.user import User, Role, UserRole
from app.core.security import hash_password


def seed_roles(db: Session):
    """Seed roles table"""
    roles_data = [
        {"name": "Admin"},
        {"name": "Editor"},
        {"name": "Author"},
        {"name": "User"},
    ]
    
    for role_data in roles_data:
        existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
    
    db.commit()
    print("✅ Roles seeded successfully")


def seed_users(db: Session):
    """Seed users table"""
    users_data = [
        {
            "name": "Admin User",
            "email": "admin@satryawiguna.me",
            "password": hash_password("admin123"),
        },
        {
            "name": "John Doe",
            "email": "john@example.com",
            "password": hash_password("password123"),
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": hash_password("password123"),
        },
    ]
    
    for user_data in users_data:
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing_user:
            user = User(**user_data)
            db.add(user)
    
    db.commit()
    print("✅ Users seeded successfully")


def seed_user_roles(db: Session):
    """Seed user_roles table"""
    # Assign Admin role to admin@satryawiguna.me
    admin_user = db.query(User).filter(User.email == "admin@satryawiguna.me").first()
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    
    if admin_user and admin_role:
        existing_user_role = db.query(UserRole).filter(
            UserRole.user_id == admin_user.id,
            UserRole.role_id == admin_role.id
        ).first()
        
        if not existing_user_role:
            user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
            db.add(user_role)
    
    # Assign Author role to john@example.com
    john_user = db.query(User).filter(User.email == "john@example.com").first()
    author_role = db.query(Role).filter(Role.name == "Author").first()
    
    if john_user and author_role:
        existing_user_role = db.query(UserRole).filter(
            UserRole.user_id == john_user.id,
            UserRole.role_id == author_role.id
        ).first()
        
        if not existing_user_role:
            user_role = UserRole(user_id=john_user.id, role_id=author_role.id)
            db.add(user_role)
    
    db.commit()
    print("✅ User roles seeded successfully")
