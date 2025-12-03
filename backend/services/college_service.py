from repositories.college_repository import CollegeRepository
from utils.exceptions import DuplicateEntryError, NotFoundError

class CollegeService:
    def __init__(self):
        self.college_repository = CollegeRepository()
    
    def get_all_colleges(self):
        """Get all colleges"""
        return self.college_repository.find_all()
    
    def create_college(self, college_data):
        """Create a new college"""
        try:
            return self.college_repository.create(college_data)
        except DuplicateEntryError:
            raise DuplicateEntryError(
                f"College code '{college_data['college_code']}' already exists"
            )
    
    def update_college(self, original_code, college_data):
        """Update a college"""
        try:
            result = self.college_repository.update(original_code, college_data)
            if not result:
                raise NotFoundError(f"College with code '{original_code}' not found")
            return result
        except DuplicateEntryError:
            raise DuplicateEntryError(
                f"College code '{college_data['college_code']}' already exists"
            )
    
    def delete_college(self, college_code):
        """Delete a college"""
        result = self.college_repository.delete(college_code)
        if not result:
            raise NotFoundError(f"College with code '{college_code}' not found")
        return result
    
    def get_stats_per_college(self):
        """Get college stats: number of programs and students per college"""
        return self.college_repository.get_stats()