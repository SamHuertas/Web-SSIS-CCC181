import bcrypt
from db import get_connection
from psycopg2 import errors as pg_errors

class AuthService:
    def register_user(self, username, email, password):
        """Register a new user with hashed password"""
        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING user_id, username, email;
                """, (username, email, password_hash.decode('utf-8')))
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise Exception("Username or email already exists")
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT user_id, username, email, password_hash
                FROM users
                WHERE email = %s;
            """, (email,))
            user = cur.fetchone()
            
            if not user:
                raise Exception("Invalid email or password")
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                raise Exception("Invalid email or password")
            
            # Return user without password hash
            return {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email']
            }