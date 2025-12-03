from db import get_connection
from psycopg2 import errors as pg_errors
from utils.exceptions import DuplicateEntryError, ForeignKeyError
from queries.student_queries import StudentQueries

class StudentRepository:
    def __init__(self):
        self.queries = StudentQueries()
    
    def find_all(self):
        """Get all students"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_ALL)
            return cur.fetchall()
    
    def find_by_id(self, student_id):
        """Find a student by ID"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.FIND_BY_ID, (student_id,))
            return cur.fetchone()
    
    def create(self, student_data):
        """Create a new student"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    self.queries.INSERT,
                    (
                        student_data['id_number'],
                        student_data['first_name'],
                        student_data['last_name'],
                        student_data['year_level'],
                        student_data['gender'],
                        student_data['program_code'],
                        student_data['picture']
                    )
                )
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise DuplicateEntryError()
        except pg_errors.ForeignKeyViolation:
            raise ForeignKeyError()
    
    def update(self, original_id_number, student_data):
        """Update a student"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute(
                    self.queries.UPDATE,
                    (
                        student_data['id_number'],
                        student_data['first_name'],
                        student_data['last_name'],
                        student_data['year_level'],
                        student_data['gender'],
                        student_data['program_code'],
                        student_data['picture'],
                        original_id_number
                    )
                )
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise DuplicateEntryError()
        except pg_errors.ForeignKeyViolation:
            raise ForeignKeyError()
    
    def delete(self, student_id):
        """Delete a student"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.DELETE, (student_id,))
            return cur.fetchone()
    
    def get_students_per_program(self):
        """Get number of students per program"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_STUDENTS_PER_PROGRAM)
            return cur.fetchall()