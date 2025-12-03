from db import get_connection
from psycopg2 import errors as pg_errors
from utils.exceptions import DuplicateEntryError
from queries.auth_queries import AuthQueries

class AuthRepository:
    def __init__(self):
        self.queries = AuthQueries()
    
    def create_user(self, username, email, password_hash):
        """Insert a new user into the database"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    self.queries.INSERT_USER,
                    (username, email, password_hash)
                )
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise DuplicateEntryError("Username or email already exists")
    
    def find_by_email(self, email):
        """Find a user by email"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_USER_BY_EMAIL, (email,))
            return cur.fetchone()
    
    def find_by_id(self, user_id):
        """Find a user by ID"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_USER_BY_ID, (user_id,))
            return cur.fetchone()