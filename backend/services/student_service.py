from db import get_connection, get_supabase_client
from psycopg2 import errors as pg_errors
from werkzeug.utils import secure_filename
import os

class StudentService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.bucket_name = "student_pictures"
    
    def upload_student_picture(self, file, student_id):
        """Upload student picture to Supabase storage and return public URL"""
        try:
            # Get file extension
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            
            # Create new filename using student_id
            new_filename = f"{student_id}{file_ext}"
            
            # Read file data
            file_data = file.read()
            
            # Upload to Supabase storage
            self.supabase.storage.from_(self.bucket_name).upload(
                path=new_filename,
                file=file_data,
                file_options={"content-type": file.content_type, "upsert": "true"}
            )
            
            # Get public URL
            public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(new_filename)
            
            return public_url
            
        except Exception as e:
            raise Exception(f"Failed to upload picture: {str(e)}")
    
    def delete_student_picture(self, student_id):
        """Delete student picture from Supabase storage"""
        try:
            # List all files in bucket to find the one matching student_id
            files = self.supabase.storage.from_(self.bucket_name).list()
            
            # Find file that starts with student_id
            for file in files:
                if file['name'].startswith(student_id):
                    self.supabase.storage.from_(self.bucket_name).remove([file['name']])
                    break
                    
        except Exception as e:
            # Don't raise error if picture doesn't exist
            print(f"Warning: Could not delete picture for {student_id}: {str(e)}")
    
    def get_all_students(self):
        """Get all students"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT id_number, first_name, last_name, year_level, gender, program_code, picture
                FROM students;
            """)
            return cur.fetchall()

    def create_student(self, student_data, picture_file=None):
        """Create a new student"""
        picture_url = None
        
        try:
            # Upload picture if provided
            if picture_file:
                picture_url = self.upload_student_picture(picture_file, student_data['id_number'])
            
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code, picture)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
                """, (
                    student_data['id_number'], 
                    student_data['first_name'], 
                    student_data['last_name'], 
                    student_data['year_level'], 
                    student_data['gender'], 
                    student_data['program_code'],
                    picture_url
                ))
                return cur.fetchone()
                
        except pg_errors.UniqueViolation:
            # If database insert fails, delete uploaded picture
            if picture_url:
                self.delete_student_picture(student_data['id_number'])
            raise Exception(f"Student ID '{student_data['id_number']}' already exists")
        except pg_errors.ForeignKeyViolation:
            # If database insert fails, delete uploaded picture
            if picture_url:
                self.delete_student_picture(student_data['id_number'])
            raise Exception(f"Program code '{student_data['program_code']}' does not exist")

    def update_student(self, original_id_number, student_data, picture_file=None):
        """Update a student"""
        try:
            picture_url = None
            
            # If new picture is provided, delete old one first and upload new one
            if picture_file:
                # Delete old picture from storage
                self.delete_student_picture(original_id_number)
                
                # Upload new picture with the new student_id
                picture_url = self.upload_student_picture(picture_file, student_data['id_number'])
            
            with get_connection() as conn, conn.cursor() as cur:
                if picture_url:
                    # Update with new picture
                    cur.execute("""
                        UPDATE students
                        SET id_number = %s, first_name = %s, last_name = %s, year_level = %s, gender = %s, program_code = %s, picture = %s
                        WHERE id_number = %s
                        RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
                    """, (
                        student_data['id_number'], 
                        student_data['first_name'], 
                        student_data['last_name'], 
                        student_data['year_level'], 
                        student_data['gender'], 
                        student_data['program_code'],
                        picture_url,
                        original_id_number
                    ))
                else:
                    # Update without picture
                    cur.execute("""
                        UPDATE students
                        SET id_number = %s, first_name = %s, last_name = %s, year_level = %s, gender = %s, program_code = %s
                        WHERE id_number = %s
                        RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
                    """, (
                        student_data['id_number'], 
                        student_data['first_name'], 
                        student_data['last_name'], 
                        student_data['year_level'], 
                        student_data['gender'], 
                        student_data['program_code'],
                        original_id_number
                    ))
                
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
                RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
            """, (student_id,))

            result = cur.fetchone()
            if not result:
                raise Exception(f"Student with ID '{student_id}' not found")
            
            # Delete picture from storage
            self.delete_student_picture(student_id)
            
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