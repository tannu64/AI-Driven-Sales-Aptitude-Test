"""
User model for the sales aptitude test.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """Class representing a user of the sales aptitude test system."""
    
    def __init__(self, id=None, username=None, email=None, password=None, 
                 first_name=None, last_name=None, created_at=None):
        """
        Initialize a user.
        
        Args:
            id (int): Unique identifier for the user
            username (str): Username for login
            email (str): Email address
            password (str): Password (will be hashed)
            first_name (str): User's first name
            last_name (str): User's last name
            created_at (datetime): When the user was created
        """
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password) if password else None
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at or datetime.now()
        self.test_results = []  # List of TestResult objects
    
    def check_password(self, password):
        """
        Check if the provided password matches the stored hash.
        
        Args:
            password (str): Password to check
            
        Returns:
            bool: True if password matches, False otherwise
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """
        Set a new password for the user.
        
        Args:
            password (str): New password to set
        """
        self.password_hash = generate_password_hash(password)
    
    @property
    def full_name(self):
        """Get the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username or "Anonymous User"
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        } 