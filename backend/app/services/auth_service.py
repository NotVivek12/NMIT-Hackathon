import os
import json
import time
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional, Dict, Any

# This is a simple in-memory user store for demo purposes
# In a real application, you would use a database
USERS_FILE = os.path.join(os.path.dirname(__file__), "../../data/users.json")
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

class AuthService:
    def __init__(self):
        # Initialize password hashing context
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # JWT settings
        self.secret_key = os.getenv("JWT_SECRET_KEY", "omnibot_secret_key_change_in_production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60 * 24  # 1 day
        
        # Initialize users from file or create empty dict
        self.users = self._load_users()
        
    def _load_users(self) -> Dict[str, Any]:
        """Load users from file or create an empty dict if file doesn't exist."""
        try:
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, "r") as f:
                    return json.load(f)
            else:
                # Create a demo user
                users = {
                    "1": {
                        "id": "1",
                        "email": "demo@example.com",
                        "name": "Demo User",
                        "hashed_password": self.pwd_context.hash("password123")
                    }
                }
                self._save_users(users)
                return users
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    
    def _save_users(self, users: Dict[str, Any]) -> None:
        """Save users to file."""
        try:
            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate a password hash."""
        return self.pwd_context.hash(password)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by email."""
        for user_id, user in self.users.items():
            if user["email"] == email:
                return user
        return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user by email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        return user
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and verify a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
    
    def register_user(self, name: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Register a new user."""
        # Check if user with this email already exists
        if self.get_user_by_email(email):
            return None
        
        # Create a new user
        user_id = str(int(time.time()))
        new_user = {
            "id": user_id,
            "email": email,
            "name": name,
            "hashed_password": self.get_password_hash(password)
        }
        
        # Add user to dict and save
        self.users[user_id] = new_user
        self._save_users(self.users)
        
        # Return user without password
        user_data = new_user.copy()
        user_data.pop("hashed_password")
        return user_data 