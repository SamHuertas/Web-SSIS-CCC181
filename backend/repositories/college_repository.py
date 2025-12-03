from db import get_connection
from psycopg2 import errors as pg_errors
from utils.exceptions import DuplicateEntryError
from queries.college_queries import CollegeQueries

class CollegeRepository:
    def __init__(self):
        self.queries = CollegeQueries()
    
    def find_all(self):
        """Get all colleges"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_ALL)
            return cur.fetchall()
    
    def find_by_code(self, college_code):
        """Find a college by code"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_BY_CODE, (college_code,))
            return cur.fetchone()
    
    def create(self, college_data):
        """Create a new college"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    self.queries.INSERT,
                    (college_data['college_code'], college_data['college_name'])
                )
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise DuplicateEntryError()
    
    def update(self, original_code, college_data):
        """Update a college"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    self.queries.UPDATE,
                    (college_data['college_code'], college_data['college_name'], original_code)
                )
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise DuplicateEntryError()
    
    def delete(self, college_code):
        """Delete a college"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.DELETE, (college_code,))
            return cur.fetchone()
    
    def get_stats(self):
        """Get college statistics"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_STATS)
            return cur.fetchall()