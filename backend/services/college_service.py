from db import get_connection
from psycopg2 import errors as pg_errors

class CollegeService:
    def get_all_colleges(self):
        """Get all colleges"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT college_code, college_name
                FROM colleges;
            """)
            return cur.fetchall()

    def create_college(self, college_data):
        """Create a new college"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO colleges (college_code, college_name)
                    VALUES (%s, %s)
                    RETURNING college_code, college_name;
                """, (college_data['college_code'], college_data['college_name']))
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise Exception(f"College code '{college_data['college_code']}' already exists")

    def update_college(self, original_code, college_data):
        """Update a college"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    UPDATE colleges
                    SET college_code = %s, college_name = %s
                    WHERE college_code = %s
                    RETURNING college_code, college_name;
                """, (college_data['college_code'], college_data['college_name'], original_code))
                
                result = cur.fetchone()
                if not result:
                    raise Exception(f"College with code '{original_code}' not found")
                return result
        except pg_errors.UniqueViolation:
            raise Exception(f"College code '{college_data['college_code']}' already exists")
    
    def delete_college(self, college_code):
        """Delete a college"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                DELETE FROM colleges
                WHERE college_code = %s
                RETURNING college_code, college_name;
            """, (college_code,))
            
            result = cur.fetchone()
            if not result:
                raise Exception(f"College with code '{college_code}' not found")
            return result