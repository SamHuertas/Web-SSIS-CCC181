from db import get_connection
from psycopg2 import errors as pg_errors
from utils.exceptions import DuplicateEntryError, ForeignKeyError
from queries.program_queries import ProgramQueries

class ProgramRepository:
    def __init__(self):
        self.queries = ProgramQueries()
    
    def find_all(self):
        """Get all programs with college details"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_ALL_WITH_COLLEGE)
            return cur.fetchall()
    
    def find_by_code(self, program_code):
        """Find a program by code"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_BY_CODE, (program_code,))
            return cur.fetchone()
    
    def create(self, program_data):
        """Create a new program"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    self.queries.INSERT,
                    (
                        program_data['program_code'],
                        program_data['program_name'],
                        program_data['college_code']
                    )
                )
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise DuplicateEntryError()
        except pg_errors.ForeignKeyViolation:
            raise ForeignKeyError()
    
    def update(self, original_code, program_data):
        """Update a program"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    self.queries.UPDATE,
                    (
                        program_data['program_code'],
                        program_data['program_name'],
                        program_data['college_code'],
                        original_code
                    )
                )
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise DuplicateEntryError()
        except pg_errors.ForeignKeyViolation:
            raise ForeignKeyError()
    
    def delete(self, program_code):
        """Delete a program"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.DELETE, (program_code,))
            return cur.fetchone()