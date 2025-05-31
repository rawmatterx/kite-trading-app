#!/usr/bin/env python3
"""
Script to create a default user for the Kite Trading App.
This should be run once during initial setup.
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.db.session import SessionLocal, engine
from app.models.user import User
from app.core.security import get_password_hash

def create_default_user():
    """Create a default admin user if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if default user already exists
        default_email = "admin@example.com"
        user = db.query(User).filter(User.email == default_email).first()
        
        if user:
            print(f"Default user {default_email} already exists.")
            return
        
        # Create default user
        default_password = "admin123"  # In a real app, this should be set via environment variable
        hashed_password = get_password_hash(default_password)
        
        new_user = User(
            email=default_email,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        print(f"Successfully created default user with email: {default_email}")
        print(f"Password: {default_password}")
        print("Please change this password after first login!")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating default user: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating default user...")
    create_default_user()
