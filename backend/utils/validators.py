from utils.exceptions import ValidationError

class Validator:
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """Validate that all required fields are present"""
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
    
    @staticmethod
    def validate_email(email):
        """Basic email validation"""
        if not email or '@' not in email:
            raise ValidationError("Invalid email format")
        return True
    
    @staticmethod
    def validate_password(password, min_length=8):
        """Validate password requirements"""
        if not password or len(password) < min_length:
            raise ValidationError(
                f"Password must be at least {min_length} characters"
            )
        return True
    
    @staticmethod
    def validate_file_extension(filename, allowed_extensions):
        """Validate file extension"""
        import os
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise ValidationError(
                f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        return True
    
    @staticmethod
    def validate_file_size(file, max_size):
        """Validate file size"""
        file.seek(0, 2)  # Seek to end of file
        size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if size > max_size:
            raise ValidationError(
                f"File size exceeds maximum allowed size of {max_size / (1024*1024)}MB"
            )
        return True