from pydantic import BaseModel, EmailStr
from typing import Optional


class AdminLogin(BaseModel):
    """Schema for admin login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@acme.com",
                "password": "securepass123"
            }
        }


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"
    organization_name: str
    organization_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "organization_name": "acme_corp",
                "organization_id": "507f1f77bcf86cd799439011"
            }
        }