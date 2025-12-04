from db import get_connection
from psycopg2 import errors as pg_errors
from utils.exceptions import DuplicateEntryError, ForeignKeyError
from queries.student_queries import StudentQueries

class StudentRepository:
    def __init__(self):
        self.queries = StudentQueries()
    
    ALLOWED_SORT_FIELDS = ['id_number', 'first_name', 'last_name', 'year_level', 'gender', 'program_code']
    
    def find_all(self, page=1, per_page=10, search='', sort_field='id_number', sort_direction='asc', filters=None):
        """Get paginated students with optional search, sorting, and filters"""
        # Validate sort parameters
        if sort_field not in self.ALLOWED_SORT_FIELDS:
            sort_field = 'id_number'
        if sort_direction.lower() not in ['asc', 'desc']:
            sort_direction = 'asc'
        
        offset = (page - 1) * per_page
        
        # Build filter clause and params
        filter_clause = ""
        filter_params = []
        
        if filters:
            if filters.get('gender'):
                filter_clause += " AND gender = %s"
                filter_params.append(filters['gender'])
            
            if filters.get('year_level'):
                filter_clause += " AND year_level = %s"
                filter_params.append(filters['year_level'])
            
            if filters.get('program_code'):
                filter_clause += " AND program_code = %s"
                filter_params.append(filters['program_code'])
        
        with get_connection() as conn, conn.cursor() as cur:
            if search:
                # Add wildcards for LIKE search
                search_pattern = f'%{search.lower()}%'
                search_params = (search_pattern,) * 5  # 5 search fields
                
                # Get total count
                count_query = self.queries.COUNT_ALL_SEARCH.format(filter_clause=filter_clause)
                cur.execute(count_query, search_params + tuple(filter_params))
                total = cur.fetchone()['total']
                
                # Get paginated results
                query = self.queries.FIND_ALL_SEARCH.format(
                    sort_field=sort_field, 
                    sort_direction=sort_direction,
                    filter_clause=filter_clause
                )
                cur.execute(query, search_params + tuple(filter_params) + (per_page, offset))
            elif filter_clause:
                # Only filters, no search
                count_query = self.queries.COUNT_ALL_FILTER.format(filter_clause=filter_clause)
                cur.execute(count_query, tuple(filter_params))
                total = cur.fetchone()['total']
                
                query = self.queries.FIND_ALL_FILTER.format(
                    sort_field=sort_field,
                    sort_direction=sort_direction,
                    filter_clause=filter_clause
                )
                cur.execute(query, tuple(filter_params) + (per_page, offset))
            else:
                # No search, no filters
                cur.execute(self.queries.COUNT_ALL)
                total = cur.fetchone()['total']
                
                query = self.queries.FIND_ALL.format(
                    sort_field=sort_field, 
                    sort_direction=sort_direction
                )
                cur.execute(query, (per_page, offset))
            
            students = cur.fetchall()
            
            return {
                'students': students,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page  # Ceiling division
            }
    
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
    
    def get_programs(self):
        """Get all programs for dropdown filter"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_ALL_PROGRAMS)
            return cur.fetchall()