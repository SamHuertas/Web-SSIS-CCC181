import bcrypt
from repositories.auth_repository import AuthRepository
from utils.exceptions import AuthenticationError, DuplicateEntryError

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()
    
    def register_user(self, username, email, password):
        """Register a new user with hashed password"""
        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            user = self.auth_repository.create_user(
                username, 
                email, 
                password_hash.decode('utf-8')
            )
            return user
        except DuplicateEntryError:
            raise Exception("Username or email already exists")
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        user = self.auth_repository.find_by_email(email)
        
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            raise AuthenticationError("Invalid email or password")
        
        # Return user without password hash
        return {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email']
        }