from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class OrganizationCreate(BaseModel):
    """Schema for creating an organization"""
    organization_name: str = Field(..., min_length=3, max_length=50, 
                                    description="Unique organization name")
    email: EmailStr = Field(..., description="Admin email address")
    password: str = Field(..., min_length=6, description="Admin password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "organization_name": "acme_corp",
                "email": "admin@acme.com",
                "password": "securepass123"
            }
        }


class OrganizationUpdate(BaseModel):
    """Schema for updating organization settings"""
    organization_name: str = Field(..., min_length=3, max_length=50)
    new_settings: dict = Field(..., description="New organization settings/data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "organization_name": "acme_corp",
                "new_settings": {
                    "company_size": "50-100",
                    "industry": "Technology",
                    "features_enabled": ["analytics", "reports"]
                }
            }
        }


class OrganizationGetRequest(BaseModel):
    """Schema for getting organization data"""
    organization_name: str = Field(..., min_length=3, max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "organization_name": "acme_corp"
            }
        }


class OrganizationDeleteRequest(BaseModel):
    """Schema for deleting an organization"""
    organization_name: str = Field(..., min_length=3, max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "organization_name": "acme_corp"
            }
        }


class OrganizationResponse(BaseModel):
    """Schema for organization response"""
    organization_id: str
    organization_name: str
    email: str
    collection_name: str
    created_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "organization_id": "507f1f77bcf86cd799439011",
                "organization_name": "acme_corp",
                "email": "admin@acme.com",
                "collection_name": "org_acme_corp",
                "created_at": "2024-01-15T10:30:00"
            }
        }