from db import get_connection
from psycopg2 import errors as pg_errors

class ProgramService:
    def get_all_programs(self):
        """Get all programs with college details (including NULL colleges)"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT p.program_code, p.program_name, p.college_code, c.college_name
                FROM programs p
                LEFT JOIN colleges c ON p.college_code = c.college_code;
            """)
            return cur.fetchall()

    def create_program(self, program_data):
        """Create a new program"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO programs (program_code, program_name, college_code)
                    VALUES (%s, %s, %s)
                    RETURNING program_code, program_name, college_code;
                """, (program_data['program_code'], program_data['program_name'], program_data['college_code']))
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise Exception(f"Program code '{program_data['program_code']}' already exists")
        except pg_errors.ForeignKeyViolation:
            raise Exception(f"College code '{program_data['college_code']}' does not exist")

    def update_program(self, original_code, program_data):
        """Update a program"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    UPDATE programs
                    SET program_code = %s, program_name = %s, college_code = %s
                    WHERE program_code = %s
                    RETURNING program_code, program_name, college_code;
                """, (program_data['program_code'], program_data['program_name'], program_data['college_code'], original_code))
                
                result = cur.fetchone()
                if not result:
                    raise Exception(f"Program with code '{original_code}' not found")
                return result
        except pg_errors.UniqueViolation:
            raise Exception(f"Program code '{program_data['program_code']}' already exists")
        except pg_errors.ForeignKeyViolation:
            raise Exception(f"College code '{program_data['college_code']}' does not exist")

    def delete_program(self, program_code):
        """Delete a program by code"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                DELETE FROM programs
                WHERE program_code = %s
                RETURNING program_code, program_name, college_code;
            """, (program_code,))
            
            result = cur.fetchone()
            if not result:
                raise Exception(f"Program with code '{program_code}' not found")
            return result