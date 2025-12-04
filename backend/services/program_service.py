from repositories.program_repository import ProgramRepository
from utils.exceptions import DuplicateEntryError, NotFoundError, ForeignKeyError

class ProgramService:
    def __init__(self):
        self.program_repository = ProgramRepository()
    
    def get_all_programs(self, page=1, per_page=10, search='', sort_field='program_code', sort_direction='asc'):
        """Get paginated programs with optional search and sorting"""
        return self.program_repository.find_all(page, per_page, search, sort_field, sort_direction)
    
    def get_all_programs_list(self):
        """Get all programs without pagination (for dropdowns)"""
        return self.program_repository.find_all_list()
    
    def create_program(self, program_data):
        """Create a new program"""
        try:
            return self.program_repository.create(program_data)
        except DuplicateEntryError:
            raise DuplicateEntryError(
                f"Program code '{program_data['program_code']}' already exists"
            )
        except ForeignKeyError:
            raise ForeignKeyError(
                f"College code '{program_data['college_code']}' does not exist"
            )
    
    def update_program(self, original_code, program_data):
        """Update a program"""
        try:
            result = self.program_repository.update(original_code, program_data)
            if not result:
                raise NotFoundError(f"Program with code '{original_code}' not found")
            return result
        except DuplicateEntryError:
            raise DuplicateEntryError(
                f"Program code '{program_data['program_code']}' already exists"
            )
        except ForeignKeyError:
            raise ForeignKeyError(
                f"College code '{program_data['college_code']}' does not exist"
            )
    
    def delete_program(self, program_code):
        """Delete a program"""
        result = self.program_repository.delete(program_code)
        if not result:
            raise NotFoundError(f"Program with code '{program_code}' not found")
        return result