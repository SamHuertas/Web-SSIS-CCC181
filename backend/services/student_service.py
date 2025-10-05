from db import get_connection
from psycopg2 import errors as pg_errors

class StudentService:
    def get_all_students(self):
        """Get all students"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT id_number, first_name, last_name, year_level, gender, program_code
                FROM students;
            """)
            return cur.fetchall()

    def create_student(self, student_data):
        """Create a new student"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_number, first_name, last_name, year_level, gender, program_code;
                """, (student_data['id_number'], student_data['first_name'], student_data['last_name'], student_data['year_level'], student_data['gender'], student_data['program_code']))
                return cur.fetchone()
        except pg_errors.UniqueViolation:
            raise Exception(f"Student ID '{student_data['id_number']}' already exists")
        except pg_errors.ForeignKeyViolation:
            raise Exception(f"Program code '{student_data['program_code']}' does not exist")

    def update_student(self, original_id_number, student_data):
        """Update a student"""
        try:
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    UPDATE students
                    SET id_number = %s, first_name = %s, last_name = %s, year_level = %s, gender = %s, program_code = %s
                    WHERE id_number = %s
                    RETURNING id_number, first_name, last_name, year_level, gender, program_code;
                """, (student_data['id_number'], student_data['first_name'], student_data['last_name'], student_data['year_level'], student_data['gender'], student_data['program_code'], original_id_number))
                
                result = cur.fetchone()
                if not result:
                    raise Exception(f"Student with ID '{original_id_number}' not found")
                return result
        except pg_errors.UniqueViolation:
            raise Exception(f"Student ID '{student_data['id_number']}' already exists")
        except pg_errors.ForeignKeyViolation:
            raise Exception(f"Program code '{student_data['program_code']}' does not exist")

    def delete_student(self, student_id):
        """Delete a student"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                DELETE FROM students
                WHERE id_number = %s
                RETURNING id_number, first_name, last_name, year_level, gender, program_code;
            """, (student_id,))

            result = cur.fetchone()
            if not result:
                raise Exception(f"Student with ID '{student_id}' not found")
            return result

    def get_students_per_program(self):
        """Get number of students per program"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT p.program_code, p.program_name, COUNT(s.id_number) AS student_count
                FROM programs p
                LEFT JOIN students s ON p.program_code = s.program_code
                GROUP BY p.program_code, p.program_name
                ORDER BY student_count DESC;
            """)
            return cur.fetchall()