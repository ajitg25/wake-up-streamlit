"""
MongoDB database utilities for managing website URLs
"""
from pymongo import MongoClient
import streamlit as st
from typing import List, Optional

class WebsiteDB:
    """Database handler for website URLs using MongoDB"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection string. If None, will try to get from Streamlit secrets
        """
        if connection_string is None:
            # Try to get from Streamlit secrets
            try:
                connection_string = st.secrets.get("MONGODB_URI", None)
            except:
                connection_string = None
        
        if not connection_string:
            raise ValueError("MongoDB connection string not provided. Please add MONGODB_URI to Streamlit secrets.")
        
        self.client = MongoClient(connection_string)
        self.db = self.client["wake_up_streamlit"]
        self.collection = self.db["websites"]
    
    def add_website(self, website_name: str) -> bool:
        """
        Add a new website to the database
        
        Args:
            website_name: URL of the website to add
            
        Returns:
            True if added successfully, False if already exists
        """
        # Check if website already exists
        if self.collection.find_one({"website_name": website_name}):
            return False
        
        # Insert new website
        self.collection.insert_one({"website_name": website_name})
        return True
    
    def get_all_websites(self) -> List[str]:
        """
        Get all websites from the database
        
        Returns:
            List of website URLs
        """
        websites = self.collection.find({}, {"website_name": 1, "_id": 0})
        return [doc["website_name"] for doc in websites]
    
    def remove_website(self, website_name: str) -> bool:
        """
        Remove a website from the database
        
        Args:
            website_name: URL of the website to remove
            
        Returns:
            True if removed successfully, False if not found
        """
        result = self.collection.delete_one({"website_name": website_name})
        return result.deleted_count > 0
    
    def website_exists(self, website_name: str) -> bool:
        """
        Check if a website exists in the database
        
        Args:
            website_name: URL of the website to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.collection.find_one({"website_name": website_name}) is not None
    
    def close(self):
        """Close the database connection"""
        self.client.close()


def get_db_connection(connection_string: Optional[str] = None) -> WebsiteDB:
    """
    Helper function to get a database connection
    
    Args:
        connection_string: MongoDB connection string. If None, will try to get from Streamlit secrets
        
    Returns:
        WebsiteDB instance
    """
    return WebsiteDB(connection_string)
