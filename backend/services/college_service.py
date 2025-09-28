from supabase import Client

class CollegeService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    def check_duplicate_code(self, college_code):
        """Check if college code already exists"""
        try:
            result = self.supabase.table('colleges').select('college_code').eq('college_code', college_code).execute()
            return len(result.data) > 0
        except Exception as e:
            raise Exception(f"Error checking duplicate code: {str(e)}")

    def check_duplicate_name(self, college_name):
        """Check if college name already exists"""
        try:
            result = self.supabase.table('colleges').select('college_name').eq('college_name', college_name).execute()
            return len(result.data) > 0
        except Exception as e:
            raise Exception(f"Error checking duplicate name: {str(e)}")

    def create_college(self, college_data):
        """Create a new college with duplicate checking"""
        try:
            college_code = college_data['college_code']
            college_name = college_data['college_name']

            # Check for duplicates
            if self.check_duplicate_code(college_code):
                raise Exception(f"College code '{college_code}' already exists")
            
            if self.check_duplicate_name(college_name):
                raise Exception(f"College name '{college_name}' already exists")
            
            # Insert the college
            result = self.supabase.table('colleges').insert(college_data).execute()
            
            if not result.data:
                raise Exception("Failed to create college")
            
            return result.data[0]
            
        except Exception as e:
            raise Exception(str(e))

    def get_all_colleges(self):
        """Get all colleges"""
        try:
            result = self.supabase.table('colleges').select('college_code, college_name').execute()
            return result.data
        except Exception as e:
            raise Exception(f"Error fetching colleges: {str(e)}")

    def update_college(self, original_code, college_data):
        """Update a college with duplicate checking"""
        try:
            new_code = college_data['college_code']
            new_name = college_data['college_name']

            # Check for duplicate code (if code is being changed)
            if new_code != original_code and self.check_duplicate_code(new_code):
                raise Exception(f"College code '{new_code}' already exists")
            
            # Check for duplicate name
            if self.check_duplicate_name(new_name):
                raise Exception(f"College name '{new_name}' already exists")
            
            # Update the college
            result = self.supabase.table('colleges').update(college_data).eq('college_code', original_code).execute()
            
            if not result.data:
                raise Exception("Failed to update college")
            
            return result.data[0]
            
        except Exception as e:
            raise Exception(str(e))