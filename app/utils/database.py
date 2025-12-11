from pymongo import MongoClient
from pymongo.database import Database
from app.config import settings
from typing import Optional


class DatabaseManager:
    """Singleton class to manage MongoDB connections"""
    
    _instance: Optional['DatabaseManager'] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish connection to MongoDB"""
        if self._client is None:
            try:
                self._client = MongoClient(settings.MONGODB_URL)
                self._db = self._client[settings.MONGODB_DB_NAME]
                # Test connection
                self._client.server_info()
                print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")
            except Exception as e:
                print(f"❌ Failed to connect to MongoDB: {e}")
                raise
    
    def get_database(self) -> Database:
        """Get the database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("🔌 MongoDB connection closed")
    
    def get_collection(self, collection_name: str):
        """Get a specific collection"""
        db = self.get_database()
        return db[collection_name]


# Global database manager instance
db_manager = DatabaseManager()