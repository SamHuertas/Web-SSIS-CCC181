class BaseAppException(Exception):
    """Base exception for all application exceptions"""
    pass

class ValidationError(BaseAppException):
    """Exception raised for validation errors"""
    pass

class AuthenticationError(BaseAppException):
    """Exception raised for authentication errors"""
    pass

class DuplicateEntryError(BaseAppException):
    """Exception raised when trying to create a duplicate entry"""
    pass

class NotFoundError(BaseAppException):
    """Exception raised when a requested resource is not found"""
    pass

class ForeignKeyError(BaseAppException):
    """Exception raised when a foreign key constraint is violated"""
    pass

class StorageError(BaseAppException):
    """Exception raised for storage-related errors"""
    pass