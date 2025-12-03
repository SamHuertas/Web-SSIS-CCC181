from db import get_connection
from psycopg2 import errors as pg_errors
from utils.exceptions import DuplicateEntryError
from queries.college_queries import CollegeQueries

class CollegeRepository:
    def __init__(self):
        self.queries = CollegeQueries()
        
    ALLOWED_SORT_FIELDS = ['college_code', 'college_name']
    
    def find_all(self, page=1, per_page=10, search='', sort_field='college_code', sort_direction='asc'):
        """Get paginated colleges with optional search and sorting"""
        # Validate sort parameters
        if sort_field not in self.ALLOWED_SORT_FIELDS:
            sort_field = 'college_code'
        if sort_direction.lower() not in ['asc', 'desc']:
            sort_direction = 'asc'
        
        offset = (page - 1) * per_page
        
        with get_connection() as conn, conn.cursor() as cur:
            if search:
                # Add wildcards for LIKE search
                search_pattern = f'%{search.lower()}%'
                
                # Get total count
                cur.execute(self.queries.COUNT_ALL_SEARCH, (search_pattern, search_pattern))
                total = cur.fetchone()['total']
                
                # Get paginated results
                query = self.queries.FIND_ALL_SEARCH.format(
                    sort_field=sort_field, 
                    sort_direction=sort_direction
                )
                cur.execute(query, (search_pattern, search_pattern, per_page, offset))
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
            
            colleges = cur.fetchall()
            
            return {
                'colleges': colleges,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page  # Ceiling division
            }
    
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