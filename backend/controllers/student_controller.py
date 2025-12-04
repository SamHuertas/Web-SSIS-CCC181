from flask import request, jsonify
from services.student_service import StudentService
from utils.exceptions import DuplicateEntryError, NotFoundError, ForeignKeyError

class StudentController:
    def __init__(self):
        self.student_service = StudentService()
    
    def get_all(self):
        """Get all students with pagination, search, sorting, and filtering"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', '', type=str)
            sort_field = request.args.get('sort_field', 'id_number', type=str)
            sort_direction = request.args.get('sort_direction', 'asc', type=str)
            
            # Get filter parameters
            filters = {}
            if request.args.get('gender'):
                filters['gender'] = request.args.get('gender', type=str)
            if request.args.get('year_level'):
                filters['year_level'] = request.args.get('year_level', type=str)
            if request.args.get('program_code'):
                filters['program_code'] = request.args.get('program_code', type=str)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:  # Max 100 items per page
                per_page = 10
            
            result = self.student_service.get_all_students(
                page, per_page, search, sort_field, sort_direction, filters if filters else None
            )
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def create(self):
        """Create a new student"""
        try:
            data = request.form.to_dict()
            picture_file = request.files.get('picture')
            
            student = self.student_service.create_student(data, picture_file)
            return jsonify(student), 200
            
        except DuplicateEntryError as e:
            return jsonify({'error': str(e)}), 409
        except ForeignKeyError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update(self, student_id):
        """Update a student"""
        try:
            data = request.form.to_dict()
            picture_file = request.files.get('picture')
            
            student = self.student_service.update_student(student_id, data, picture_file)
            return jsonify(student), 200
            
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except DuplicateEntryError as e:
            return jsonify({'error': str(e)}), 409
        except ForeignKeyError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def delete(self, student_id):
        """Delete a student"""
        try:
            student = self.student_service.delete_student(student_id)
            return jsonify(student), 200
            
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_students_per_program(self):
        """Get number of students per program"""
        try:
            result = self.student_service.get_students_per_program()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_programs(self):
        """Get all programs for dropdown filter"""
        try:
            result = self.student_service.get_programs()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500