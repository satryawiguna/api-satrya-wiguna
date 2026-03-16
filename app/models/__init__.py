"""
Models package initialization
Import all models to ensure they're registered with SQLAlchemy
"""
from app.models.other import Media, Setting, Skill, Testimonial, ContactMessage
from app.models.user import User, Role, UserRole
from app.models.project import Project, ProjectImage
from app.models.blog import BlogPost, Category, Tag, BlogPostCategory, BlogPostTag

__all__ = [
    # Other models
    "Media",
    "Setting",
    "Skill",
    "Testimonial",
    "ContactMessage",
    # User models
    "User",
    "Role",
    "UserRole",
    # Project models
    "Project",
    "ProjectImage",
    # Blog models
    "BlogPost",
    "Category",
    "Tag",
    "BlogPostCategory",
    "BlogPostTag",
]
