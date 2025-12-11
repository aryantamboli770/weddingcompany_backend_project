from typing import Optional, Dict, List
from datetime import datetime
from bson import ObjectId
from app.utils.database import DatabaseManager


class OrganizationRepository:
    """Repository for organization data operations"""
    
    ORGANIZATIONS_COLLECTION = "organizations"
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db = db_manager.get_database()
    
    def create_organization(self, org_data: Dict) -> Dict:
        """
        Create a new organization in the master database
        
        Args:
            org_data: Dictionary containing organization details
        
        Returns:
            Created organization document
        """
        collection = self.db[self.ORGANIZATIONS_COLLECTION]
        
        # Add metadata
        org_data['created_at'] = datetime.utcnow()
        org_data['updated_at'] = datetime.utcnow()
        
        result = collection.insert_one(org_data)
        org_data['_id'] = result.inserted_id
        
        return org_data
    
    def get_organization_by_name(self, organization_name: str) -> Optional[Dict]:
        """
        Get organization by name
        
        Args:
            organization_name: Name of the organization
        
        Returns:
            Organization document or None
        """
        collection = self.db[self.ORGANIZATIONS_COLLECTION]
        return collection.find_one({"organization_name": organization_name})
    
    def get_organization_by_email(self, email: str) -> Optional[Dict]:
        """
        Get organization by admin email
        
        Args:
            email: Admin email address
        
        Returns:
            Organization document or None
        """
        collection = self.db[self.ORGANIZATIONS_COLLECTION]
        return collection.find_one({"email": email})
    
    def get_organization_by_id(self, org_id: str) -> Optional[Dict]:
        """
        Get organization by ID
        
        Args:
            org_id: Organization ID
        
        Returns:
            Organization document or None
        """
        collection = self.db[self.ORGANIZATIONS_COLLECTION]
        return collection.find_one({"_id": ObjectId(org_id)})
    
    def update_organization(self, organization_name: str, update_data: Dict) -> bool:
        """
        Update organization metadata
        
        Args:
            organization_name: Name of the organization
            update_data: Data to update
        
        Returns:
            True if updated, False otherwise
        """
        collection = self.db[self.ORGANIZATIONS_COLLECTION]
        update_data['updated_at'] = datetime.utcnow()
        
        result = collection.update_one(
            {"organization_name": organization_name},
            {"$set": update_data}
        )
        
        return result.modified_count > 0
    
    def delete_organization(self, organization_name: str) -> bool:
        """
        Delete organization from master database
        
        Args:
            organization_name: Name of the organization
        
        Returns:
            True if deleted, False otherwise
        """
        collection = self.db[self.ORGANIZATIONS_COLLECTION]
        result = collection.delete_one({"organization_name": organization_name})
        return result.deleted_count > 0
    
    def create_organization_collection(self, collection_name: str) -> bool:
        """
        Create a dedicated collection for an organization
        
        Args:
            collection_name: Name of the collection to create
        
        Returns:
            True if created successfully
        """
        try:
            # Create collection with validation (optional)
            self.db.create_collection(collection_name)
            return True
        except Exception as e:
            print(f"Error creating collection {collection_name}: {e}")
            return False
    
    def drop_organization_collection(self, collection_name: str) -> bool:
        """
        Drop an organization's collection
        
        Args:
            collection_name: Name of the collection to drop
        
        Returns:
            True if dropped successfully
        """
        try:
            self.db.drop_collection(collection_name)
            return True
        except Exception as e:
            print(f"Error dropping collection {collection_name}: {e}")
            return False
    
    def get_organization_data(self, collection_name: str) -> List[Dict]:
        """
        Get all data from an organization's collection
        
        Args:
            collection_name: Name of the organization's collection
        
        Returns:
            List of documents
        """
        collection = self.db[collection_name]
        return list(collection.find())
    
    def insert_organization_data(self, collection_name: str, data: Dict) -> bool:
        """
        Insert data into an organization's collection
        
        Args:
            collection_name: Name of the organization's collection
            data: Data to insert
        
        Returns:
            True if inserted successfully
        """
        try:
            collection = self.db[collection_name]
            collection.insert_one(data)
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
    
    def migrate_organization_data(self, old_collection: str, new_collection: str) -> bool:
        """
        Migrate data from old collection to new collection
        
        Args:
            old_collection: Source collection name
            new_collection: Destination collection name
        
        Returns:
            True if migration successful
        """
        try:
            # Get all data from old collection
            old_data = self.get_organization_data(old_collection)
            
            if not old_data:
                return True  # No data to migrate
            
            # Insert into new collection
            new_col = self.db[new_collection]
            new_col.insert_many(old_data)
            
            return True
        except Exception as e:
            print(f"Error migrating data: {e}")
            return False