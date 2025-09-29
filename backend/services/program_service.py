from supabase import Client

class ProgramService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    def check_duplicate_code(self, program_code):
        """Check if program code already exists"""
        try:
            result = self.supabase.table('programs').select('program_code').eq('program_code', program_code).execute()
            return len(result.data) > 0
        except Exception as e:
            raise Exception(f"Error checking duplicate code: {str(e)}")
    
    def check_duplicate_name(self, program_name):
        """Check if program name already exists"""
        try:
            result = self.supabase.table('programs').select('program_name').eq('program_name', program_name).execute()
            return len(result.data) > 0
        except Exception as e:
            raise Exception(f"Error checking duplicate name: {str(e)}")
        
    def create_program(self, program_data):
        """Create a new college with duplicate checking"""
        try:
            program_code = program_data['program_code']
            program_name = program_data['program_name']

            # Check for duplicates
            if self.check_duplicate_code(program_code):
                raise Exception(f"Program code '{program_code}' already exists")
            
            if self.check_duplicate_name(program_name):
                raise Exception(f"Program name '{program_name}' already exists")
            
            # Insert the program
            result = self.supabase.table('programs').insert(program_data).execute()
            
            if not result.data:
                raise Exception("Failed to create program")
            
            return result.data[0]
            
        except Exception as e:
            raise Exception(str(e))
        
    def get_all_programs(self):
        """Get all programs"""
        try:
            result = self.supabase.table('programs').select('program_code, program_name, college_code').execute()
            return result.data
        except Exception as e:
            raise Exception(f"Error fetching programs: {str(e)}")
    
    def update_program(self, original_code, program_data):
        """Update a college with duplicate checking"""
        try:
            new_code = program_data['program_code']
            new_name = program_data['program_name']
            new_college = program_data['college_code']

            # Check for duplicate code (if code is being changed)
            if new_code != original_code and self.check_duplicate_code(new_code):
                raise Exception(f"Program code '{new_code}' already exists")
            
            # Check for duplicate name
            if self.check_duplicate_name(new_name):
                raise Exception(f"Program name '{new_name}' already exists")
            
            # Update the program
            result = self.supabase.table('programs').update(program_data).eq('program_code', original_code).execute()
            
            if not result.data:
                raise Exception("Failed to update program")
            
            return result.data[0]
            
        except Exception as e:
            raise Exception(str(e))
        
    def delete_program(self, program_code):
        """delete a program by code"""
        try:
            result = self.supabase.table('programs').delete().eq('program_code', program_code).execute()

            if not result.data:
                raise Exception("Failed to delete program")
            
        except Exception as e:
            raise Exception(str(e))