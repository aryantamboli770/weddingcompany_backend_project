from fastapi import APIRouter, HTTPException, status
from app.models.admin import AdminLogin, TokenResponse
from app.services.auth_service import AuthService
from app.utils.database import db_manager
from app.utils.security import security_manager


router = APIRouter(prefix="/admin", tags=["Admin"])

# Initialize auth service
auth_service = AuthService(db_manager, security_manager)


@router.post("/login", response_model=TokenResponse)
async def admin_login(credentials: AdminLogin):
    """
    Admin login endpoint
    
    Authenticate admin user and return JWT access token
    
    - **email**: Admin email address
    - **password**: Admin password
    
    Returns JWT token with organization details
    """
    result = auth_service.authenticate_admin(
        email=credentials.email,
        password=credentials.password
    )
    return result