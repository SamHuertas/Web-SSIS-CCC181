from db import get_connection, get_supabase_client
from psycopg2 import errors as pg_errors
from werkzeug.utils import secure_filename
import os

class StudentService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.bucket_name = "student_pictures"
    
    def upload_student_picture(self, file, student_id):
        """Upload student picture to Supabase storage using student ID as filename"""
        try:
            # Get file extension
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            
            # Use student ID as filename 
            new_filename = f"{student_id}{file_ext}"
            
            # Read file data
            file_data = file.read()
            
            # Upload to Supabase storage with upsert=true to replace existing files
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
            
            # Find and delete file that starts with student_id
            for file in files:
                if file['name'].startswith(student_id):
                    self.supabase.storage.from_(self.bucket_name).remove([file['name']])
                    break
                    
        except Exception as e:
            print(f"Warning: Could not delete picture for {student_id}: {str(e)}")
    
    def rename_student_picture(self, old_id, new_id):
        """Rename student picture when ID changes (copy to new name, delete old)"""
        try:
            # List all files to find the old one
            files = self.supabase.storage.from_(self.bucket_name).list()
            
            old_filename = None
            for file in files:
                if file['name'].startswith(old_id):
                    old_filename = file['name']
                    break
            
            if old_filename:
                # Get file extension and determine content type
                file_ext = os.path.splitext(old_filename)[1].lower()
                new_filename = f"{new_id}{file_ext}"
                
                content_type_map = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp'
                }
                content_type = content_type_map.get(file_ext, 'image/jpeg')
                
                # Download old file as bytes
                old_file_data = self.supabase.storage.from_(self.bucket_name).download(old_filename)
                
                # Upload with new filename and proper content-type
                self.supabase.storage.from_(self.bucket_name).upload(
                    path=new_filename,
                    file=old_file_data,
                    file_options={"content-type": content_type, "upsert": "true"}
                )
                
                # Delete old file
                self.supabase.storage.from_(self.bucket_name).remove([old_filename])
                
                # Return new public URL
                return self.supabase.storage.from_(self.bucket_name).get_public_url(new_filename)
            
            return None
                    
        except Exception as e:
            print(f"Warning: Could not rename picture from {old_id} to {new_id}: {str(e)}")
            return None
    
    def get_all_students(self):
        """Get all students"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT id_number, first_name, last_name, year_level, gender, program_code, picture
                FROM students;
            """)
            return cur.fetchall()

    def create_student(self, student_data, picture_file=None):
        """Create a new student with optional picture"""
        picture_url = None
        
        try:
            # Upload picture if provided (filename will be student ID)
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
            if picture_url:
                self.delete_student_picture(student_data['id_number'])
            raise Exception(f"Student ID '{student_data['id_number']}' already exists")
        except pg_errors.ForeignKeyViolation:
            if picture_url:
                self.delete_student_picture(student_data['id_number'])
            raise Exception(f"Program code '{student_data['program_code']}' does not exist")

    def update_student(self, original_id_number, student_data, picture_file=None):
        """Update a student with optional new picture"""
        try:
            picture_url = None
            
            # Get current student data to preserve existing picture URL if needed
            with get_connection() as conn, conn.cursor() as cur:
                cur.execute("""
                    SELECT picture FROM students WHERE id_number = %s;
                """, (original_id_number,))

                current_student = cur.fetchone()

                if not current_student:
                    raise Exception(f"Student with ID '{original_id_number}' not found")
                current_picture_url = current_student['picture']
                
                # IMPORTANT: Check if new ID already exists (if ID is changing)
                if original_id_number != student_data['id_number']:
                    cur.execute("""
                        SELECT id_number FROM students WHERE id_number = %s;
                    """, (student_data['id_number'],))
                    if cur.fetchone():
                        raise pg_errors.UniqueViolation(f"Student ID '{student_data['id_number']}' already exists")
            
            if picture_file:
                # Delete old picture from storage
                self.delete_student_picture(original_id_number)
                
                # Upload new picture with the NEW student_id as filename
                picture_url = self.upload_student_picture(picture_file, student_data['id_number'])
            
            # If ID number changed but no new picture provided
            elif original_id_number != student_data['id_number'] and current_picture_url:
                # Rename the existing picture to match new ID
                picture_url = self.rename_student_picture(original_id_number, student_data['id_number'])
                # If rename failed but there was a picture, keep the old URL
                if not picture_url:
                    picture_url = current_picture_url
            
            # If nothing changed, keep existing picture URL
            else:
                picture_url = current_picture_url
            
            with get_connection() as conn, conn.cursor() as cur:
                # Always update with the picture URL (whether new, renamed, or existing)
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
                
                result = cur.fetchone()
                if not result:
                    raise Exception(f"Student with ID '{original_id_number}' not found")
                return result
                
        except pg_errors.UniqueViolation:
            if picture_file and picture_url:
                self.delete_student_picture(student_data['id_number'])
            elif original_id_number != student_data['id_number'] and current_picture_url and not picture_file:
                self.rename_student_picture(student_data['id_number'], original_id_number)
            raise Exception(f"Student ID '{student_data['id_number']}' already exists")
        
        except pg_errors.ForeignKeyViolation:
            if picture_file and picture_url:
                self.delete_student_picture(student_data['id_number'])
            elif original_id_number != student_data['id_number'] and current_picture_url and not picture_file:
                self.rename_student_picture(student_data['id_number'], original_id_number)
            raise Exception(f"Program code '{student_data['program_code']}' does not exist")

    def delete_student(self, student_id):
        """Delete a student and their picture"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                DELETE FROM students
                WHERE id_number = %s
                RETURNING id_number, first_name, last_name, year_level, gender, program_code, picture;
            """, (student_id,))

            result = cur.fetchone()
            if not result:
                raise Exception(f"Student with ID '{student_id}' not found")
            
            # Delete picture from storage (filename is student ID)
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