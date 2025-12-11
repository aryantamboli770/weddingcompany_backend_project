from typing import Optional, Dict
from fastapi import HTTPException, status
from app.repositories.organization_repository import OrganizationRepository
from app.utils.database import DatabaseManager
from app.utils.security import SecurityManager
from datetime import datetime


class OrganizationService:
    """Service layer for organization business logic"""
    
    def __init__(self, db_manager: DatabaseManager, security_manager: SecurityManager):
        self.repository = OrganizationRepository(db_manager)
        self.security_manager = security_manager
    
    def create_organization(self, organization_name: str, email: str, password: str) -> Dict:
        """
        Create a new organization with its own collection
        
        Args:
            organization_name: Unique name for the organization
            email: Admin email
            password: Admin password
        
        Returns:
            Created organization details
        
        Raises:
            HTTPException: If organization already exists
        """
        # Check if organization already exists
        existing_org = self.repository.get_organization_by_name(organization_name)
        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization '{organization_name}' already exists"
            )
        
        # Check if email already exists
        existing_email = self.repository.get_organization_by_email(email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{email}' is already registered"
            )
        
        # Hash the password
        hashed_password = self.security_manager.hash_password(password)
        
        # Create collection name
        collection_name = f"org_{organization_name}"
        
        # Prepare organization data
        org_data = {
            "organization_name": organization_name,
            "email": email,
            "password": hashed_password,
            "collection_name": collection_name,
        }
        
        # Create organization in master database
        created_org = self.repository.create_organization(org_data)
        
        # Create dedicated collection for the organization
        collection_created = self.repository.create_organization_collection(collection_name)
        
        if not collection_created:
            # Rollback: delete the organization if collection creation fails
            self.repository.delete_organization(organization_name)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create organization collection"
            )
        
        # Return response (exclude password)
        return {
            "organization_id": str(created_org['_id']),
            "organization_name": created_org['organization_name'],
            "email": created_org['email'],
            "collection_name": created_org['collection_name'],
            "created_at": created_org['created_at'].isoformat()
        }
    
    def get_organization(self, organization_name: str) -> Dict:
        """
        Get organization details
        
        Args:
            organization_name: Name of the organization
        
        Returns:
            Organization details
        
        Raises:
            HTTPException: If organization not found
        """
        org = self.repository.get_organization_by_name(organization_name)
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{organization_name}' not found"
            )
        
        # Get data from organization's collection
        org_data = self.repository.get_organization_data(org['collection_name'])
        
        return {
            "organization_id": str(org['_id']),
            "organization_name": org['organization_name'],
            "email": org['email'],
            "collection_name": org['collection_name'],
            "created_at": org['created_at'].isoformat(),
            "data_count": len(org_data),
            "data": org_data[:10] if org_data else []  # Return first 10 records
        }
    
    def update_organization(self, organization_name: str, new_settings: Dict) -> Dict:
        """
        Update organization settings and migrate data if name changes
        
        Args:
            organization_name: Current organization name
            new_settings: New settings to apply
        
        Returns:
            Updated organization details
        
        Raises:
            HTTPException: If organization not found or update fails
        """
        # Get existing organization
        org = self.repository.get_organization_by_name(organization_name)
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{organization_name}' not found"
            )
        
        old_collection_name = org['collection_name']
        
        # Check if organization name is being changed
        new_org_name = new_settings.get('organization_name', organization_name)
        
        if new_org_name != organization_name:
            # Check if new name already exists
            existing = self.repository.get_organization_by_name(new_org_name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Organization name '{new_org_name}' already exists"
                )
            
            # Create new collection name
            new_collection_name = f"org_{new_org_name}"
            
            # Create new collection
            self.repository.create_organization_collection(new_collection_name)
            
            # Migrate data from old to new collection
            migration_success = self.repository.migrate_organization_data(
                old_collection_name, 
                new_collection_name
            )
            
            if not migration_success:
                # Rollback: delete new collection
                self.repository.drop_organization_collection(new_collection_name)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to migrate organization data"
                )
            
            # Update organization metadata
            update_data = {
                "organization_name": new_org_name,
                "collection_name": new_collection_name,
                **new_settings
            }
            
            updated = self.repository.update_organization(organization_name, update_data)
            
            if updated:
                # Delete old collection
                self.repository.drop_organization_collection(old_collection_name)
            
        else:
            # Just update metadata without migration
            updated = self.repository.update_organization(organization_name, new_settings)
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update organization"
            )
        
        # Get updated organization
        updated_org = self.repository.get_organization_by_name(new_org_name)
        
        return {
            "organization_id": str(updated_org['_id']),
            "organization_name": updated_org['organization_name'],
            "email": updated_org['email'],
            "collection_name": updated_org['collection_name'],
            "message": "Organization updated successfully"
        }
    
    def delete_organization(self, organization_name: str) -> Dict:
        """
        Delete an organization and its collection
        
        Args:
            organization_name: Name of the organization
        
        Returns:
            Deletion confirmation
        
        Raises:
            HTTPException: If organization not found or deletion fails
        """
        # Get organization
        org = self.repository.get_organization_by_name(organization_name)
        
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{organization_name}' not found"
            )
        
        collection_name = org['collection_name']
        
        # Drop organization collection
        collection_dropped = self.repository.drop_organization_collection(collection_name)
        
        # Delete from master database
        deleted = self.repository.delete_organization(organization_name)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete organization"
            )
        
        return {
            "message": f"Organization '{organization_name}' deleted successfully",
            "collection_dropped": collection_dropped
        }