# app/repositories/__init__.py
"""
Data access repositories
"""

from app.repositories.organization_repository import OrganizationRepository

__all__ = [
    "OrganizationRepository"
]