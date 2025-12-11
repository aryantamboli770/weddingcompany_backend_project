from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from app.models.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationGetRequest,
    OrganizationDeleteRequest,
    OrganizationResponse
)
from app.services.organization_service import OrganizationService
from app.services.auth_service import AuthService, security
from app.utils.database import db_manager
from app.utils.security import security_manager


router = APIRouter(prefix="/org", tags=["Organization"])

# Initialize services
org_service = OrganizationService(db_manager, security_manager)
auth_service = AuthService(db_manager, security_manager)


@router.post("/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(org_data: OrganizationCreate):
    """
    Create a new organization with admin user
    
    - **organization_name**: Unique name (3-50 characters)
    - **email**: Admin email address
    - **password**: Admin password (minimum 6 characters)
    """
    result = org_service.create_organization(
        organization_name=org_data.organization_name,
        email=org_data.email,
        password=org_data.password
    )
    return result


@router.get("/get")
async def get_organization(organization_name: str):
    """
    Get organization details by name
    
    - **organization_name**: Name of the organization to retrieve
    """
    result = org_service.get_organization(organization_name)
    return result


@router.put("/update")
async def update_organization(
    org_data: OrganizationUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Update organization settings (requires authentication)
    
    - **organization_name**: Current organization name
    - **new_settings**: New settings/data to apply
    
    Requires JWT token in Authorization header
    """
    # Verify user is authenticated and belongs to this organization
    current_org = auth_service.get_current_organization(credentials)
    
    if current_org['organization_name'] != org_data.organization_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own organization"
        )
    
    result = org_service.update_organization(
        organization_name=org_data.organization_name,
        new_settings=org_data.new_settings
    )
    return result


@router.delete("/delete")
async def delete_organization(
    organization_name: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Delete organization (requires authentication)
    
    - **organization_name**: Name of the organization to delete
    
    Only authenticated admin of the organization can delete it
    Requires JWT token in Authorization header
    """
    # Verify user is authenticated and belongs to this organization
    current_org = auth_service.get_current_organization(credentials)
    
    if current_org['organization_name'] != organization_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own organization"
        )
    
    result = org_service.delete_organization(organization_name)
    return result