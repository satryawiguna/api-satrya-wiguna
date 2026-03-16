"""
Other schemas (Skill, Testimonial, ContactMessage, Media, Setting)
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class SkillBase(BaseModel):
    """Base skill schema"""
    name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=255)
    level: Optional[int] = Field(None, ge=0, le=100)
    icon: Optional[str] = Field(None, max_length=255)
    sort_order: int = 0


class SkillCreate(SkillBase):
    """Schema for creating a skill"""
    pass


class SkillUpdate(BaseModel):
    """Schema for updating a skill"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=255)
    level: Optional[int] = Field(None, ge=0, le=100)
    icon: Optional[str] = Field(None, max_length=255)
    sort_order: Optional[int] = None


class SkillResponse(SkillBase):
    """Schema for skill response"""
    id: int
    
    class Config:
        from_attributes = True


class TestimonialBase(BaseModel):
    """Base testimonial schema"""
    name: str = Field(..., min_length=1, max_length=255)
    position: Optional[str] = Field(None, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    content: str = Field(..., min_length=1)
    avatar_id: Optional[int] = None
    featured: bool = False


class TestimonialCreate(TestimonialBase):
    """Schema for creating a testimonial"""
    pass


class TestimonialUpdate(BaseModel):
    """Schema for updating a testimonial"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    position: Optional[str] = Field(None, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    avatar_id: Optional[int] = None
    featured: Optional[bool] = None


class TestimonialResponse(TestimonialBase):
    """Schema for testimonial response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContactMessageBase(BaseModel):
    """Base contact message schema"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    subject: Optional[str] = Field(None, max_length=255)
    message: str = Field(..., min_length=1)


class ContactMessageCreate(ContactMessageBase):
    """Schema for creating a contact message"""
    pass


class ContactMessageResponse(ContactMessageBase):
    """Schema for contact message response"""
    id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MediaBase(BaseModel):
    """Base media schema"""
    file_name: str = Field(..., min_length=1, max_length=255)
    file_path: str = Field(..., min_length=1, max_length=500)
    mime_type: Optional[str] = Field(None, max_length=100)
    size: Optional[int] = None


class MediaCreate(MediaBase):
    """Schema for creating a media"""
    pass


class MediaResponse(MediaBase):
    """Schema for media response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SettingBase(BaseModel):
    """Base setting schema"""
    key: str = Field(..., min_length=1, max_length=255)
    value: Optional[str] = None


class SettingCreate(SettingBase):
    """Schema for creating a setting"""
    pass


class SettingUpdate(BaseModel):
    """Schema for updating a setting"""
    value: Optional[str] = None


class SettingResponse(SettingBase):
    """Schema for setting response"""
    id: int
    
    class Config:
        from_attributes = True
