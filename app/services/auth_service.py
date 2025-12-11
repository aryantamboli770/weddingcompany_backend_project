from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.repositories.organization_repository import OrganizationRepository
from app.utils.security import SecurityManager
from app.utils.database import DatabaseManager


security = HTTPBearer()


class AuthService:
    """Service for authentication and authorization"""
    
    def __init__(self, db_manager: DatabaseManager, security_manager: SecurityManager):
        self.repository = OrganizationRepository(db_manager)
        self.security_manager = security_manager
    
    def authenticate_admin(self, email: str, password: str) -> dict:
        """
        Authenticate admin user and return JWT token
        
        Args:
            email: Admin email
            password: Admin password
        
        Returns:
            Dictionary with access token and organization details
        
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find organization by email
        org = self.repository.get_organization_by_email(email)
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify password
        if not self.security_manager.verify_password(password, org['password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Create JWT token
        token_data = {
            "sub": email,
            "organization_id": str(org['_id']),
            "organization_name": org['organization_name']
        }
        
        access_token = self.security_manager.create_access_token(token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "organization_name": org['organization_name'],
            "organization_id": str(org['_id'])
        }
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        """
        Verify JWT token and return decoded payload
        
        Args:
            credentials: HTTP Authorization credentials with Bearer token
        
        Returns:
            Decoded token payload
        
        Raises:
            HTTPException: If token is invalid or expired
        """
        token = credentials.credentials
        
        payload = self.security_manager.decode_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return payload
    
    def get_current_organization(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        """
        Get current authenticated organization from token
        
        Args:
            credentials: HTTP Authorization credentials
        
        Returns:
            Organization details
        
        Raises:
            HTTPException: If token is invalid or organization not found
        """
        payload = self.verify_token(credentials)
        
        organization_name = payload.get("organization_name")
        
        if not organization_name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Get organization from database
        org = self.repository.get_organization_by_name(organization_name)
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        
        return {
            "organization_id": str(org['_id']),
            "organization_name": org['organization_name'],
            "email": org['email'],
            "collection_name": org['collection_name']
        }