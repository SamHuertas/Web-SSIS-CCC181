from db import get_connection
from psycopg2 import errors as pg_errors
from utils.exceptions import DuplicateEntryError, ForeignKeyError
from queries.program_queries import ProgramQueries

class ProgramRepository:
    def __init__(self):
        self.queries = ProgramQueries()
    
    ALLOWED_SORT_FIELDS = ['program_code', 'program_name', 'college_code', 'college_name']
    
    def find_all(self, page=1, per_page=10, search='', sort_field='program_code', sort_direction='asc'):
        """Get paginated programs with optional search and sorting"""
        # Validate sort parameters
        if sort_field not in self.ALLOWED_SORT_FIELDS:
            sort_field = 'program_code'
        if sort_direction.lower() not in ['asc', 'desc']:
            sort_direction = 'asc'
        
        offset = (page - 1) * per_page
        
        with get_connection() as conn, conn.cursor() as cur:
            if search:
                # Add wildcards for LIKE search
                search_pattern = f'%{search.lower()}%'
                search_params = (search_pattern,) * 4  # 4 search fields
                
                # Get total count
                cur.execute(self.queries.COUNT_ALL_SEARCH, search_params)
                total = cur.fetchone()['total']
                
                # Get paginated results
                query = self.queries.FIND_ALL_SEARCH.format(
                    sort_field=sort_field, 
                    sort_direction=sort_direction
                )
                cur.execute(query, search_params + (per_page, offset))
            else:
                # Get total count
                cur.execute(self.queries.COUNT_ALL)
                total = cur.fetchone()['total']
                
                # Get paginated results
                query = self.queries.FIND_ALL.format(
                    sort_field=sort_field, 
                    sort_direction=sort_direction
                )
                cur.execute(query, (per_page, offset))
            
            programs = cur.fetchall()
            
            return {
                'programs': programs,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page  # Ceiling division
            }
    
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
        
    def find_all_list(self):
        """Get all programs without pagination (for dropdowns)"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.PROGRAM_LIST)
            return cur.fetchall()