from db import get_supabase_client
from werkzeug.utils import secure_filename
from config.storage_config import StorageConfig
import os

class StorageService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.bucket_name = StorageConfig.BUCKET_NAME
        self.content_types = StorageConfig.CONTENT_TYPES
    
    def upload_picture(self, file, student_id):
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
                file_options={
                    "content-type": file.content_type, 
                    "upsert": "true"
                }
            )
            
            # Get public URL
            public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(
                new_filename
            )
            
            return public_url
            
        except Exception as e:
            raise Exception(f"Failed to upload picture: {str(e)}")
    
    def delete_picture(self, student_id):
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
    
    def rename_picture(self, old_id, new_id):
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
                
                content_type = self.content_types.get(file_ext, 'image/jpeg')
                
                # Download old file as bytes
                old_file_data = self.supabase.storage.from_(self.bucket_name).download(
                    old_filename
                )
                
                # Upload with new filename and proper content-type
                self.supabase.storage.from_(self.bucket_name).upload(
                    path=new_filename,
                    file=old_file_data,
                    file_options={
                        "content-type": content_type, 
                        "upsert": "true"
                    }
                )
                
                # Delete old file
                self.supabase.storage.from_(self.bucket_name).remove([old_filename])
                
                # Return new public URL
                return self.supabase.storage.from_(self.bucket_name).get_public_url(
                    new_filename
                )
            
            return None
                    
        except Exception as e:
            print(f"Warning: Could not rename picture from {old_id} to {new_id}: {str(e)}")
            return None