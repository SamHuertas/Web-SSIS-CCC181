from repositories.student_repository import StudentRepository
from services.storage_service import StorageService
from utils.exceptions import DuplicateEntryError, NotFoundError, ForeignKeyError

class StudentService:
    def __init__(self):
        self.student_repository = StudentRepository()
        self.storage_service = StorageService()
    
    def get_all_students(self):
        """Get all students"""
        return self.student_repository.find_all()
    
    def create_student(self, student_data, picture_file=None):
        """Create a new student with optional picture"""
        picture_url = None
        
        try:
            # Upload picture if provided
            if picture_file:
                picture_url = self.storage_service.upload_picture(
                    picture_file, 
                    student_data['id_number']
                )
            
            # Add picture URL to student data
            student_data['picture'] = picture_url
            
            # Create student in database
            return self.student_repository.create(student_data)
            
        except DuplicateEntryError:
            if picture_url:
                self.storage_service.delete_picture(student_data['id_number'])
            raise DuplicateEntryError(
                f"Student ID '{student_data['id_number']}' already exists"
            )
        except ForeignKeyError:
            if picture_url:
                self.storage_service.delete_picture(student_data['id_number'])
            raise ForeignKeyError(
                f"Program code '{student_data['program_code']}' does not exist"
            )
    
    def update_student(self, original_id_number, student_data, picture_file=None):
        """Update a student with optional new picture"""
        try:
            # Get current student data
            current_student = self.student_repository.find_by_id(original_id_number)
            
            if not current_student:
                raise NotFoundError(
                    f"Student with ID '{original_id_number}' not found"
                )
            
            current_picture_url = current_student['picture']
            picture_url = None
            
            # Check if new ID already exists (if ID is changing)
            if original_id_number != student_data['id_number']:
                existing = self.student_repository.find_by_id(student_data['id_number'])
                if existing:
                    raise DuplicateEntryError(
                        f"Student ID '{student_data['id_number']}' already exists"
                    )
            
            # Handle picture logic
            if picture_file:
                # Delete old picture and upload new one
                self.storage_service.delete_picture(original_id_number)
                picture_url = self.storage_service.upload_picture(
                    picture_file, 
                    student_data['id_number']
                )
            elif original_id_number != student_data['id_number'] and current_picture_url:
                # Rename existing picture to match new ID
                picture_url = self.storage_service.rename_picture(
                    original_id_number, 
                    student_data['id_number']
                )
                if not picture_url:
                    picture_url = current_picture_url
            else:
                # Keep existing picture URL
                picture_url = current_picture_url
            
            student_data['picture'] = picture_url
            
            # Update student in database
            result = self.student_repository.update(original_id_number, student_data)
            
            if not result:
                raise NotFoundError(
                    f"Student with ID '{original_id_number}' not found"
                )
            
            return result
            
        except DuplicateEntryError:
            # Rollback picture changes if database update fails
            if picture_file and picture_url:
                self.storage_service.delete_picture(student_data['id_number'])
            elif (original_id_number != student_data['id_number'] and 
                  current_picture_url and not picture_file):
                self.storage_service.rename_picture(
                    student_data['id_number'], 
                    original_id_number
                )
            raise DuplicateEntryError(
                f"Student ID '{student_data['id_number']}' already exists"
            )
        except ForeignKeyError:
            # Rollback picture changes if database update fails
            if picture_file and picture_url:
                self.storage_service.delete_picture(student_data['id_number'])
            elif (original_id_number != student_data['id_number'] and 
                  current_picture_url and not picture_file):
                self.storage_service.rename_picture(
                    student_data['id_number'], 
                    original_id_number
                )
            raise ForeignKeyError(
                f"Program code '{student_data['program_code']}' does not exist"
            )
    
    def delete_student(self, student_id):
        """Delete a student and their picture"""
        result = self.student_repository.delete(student_id)
        
        if not result:
            raise NotFoundError(f"Student with ID '{student_id}' not found")
        
        # Delete picture from storage
        self.storage_service.delete_picture(student_id)
        
        return result
    
    def get_students_per_program(self):
        """Get number of students per program"""
        return self.student_repository.get_students_per_program()