from flask import request, jsonify
from flask_jwt_extended import jwt_required
from services.student_service import StudentService
from utils.exceptions import DuplicateEntryError, NotFoundError, ForeignKeyError

class StudentController:
    def __init__(self):
        self.student_service = StudentService()
    
    @jwt_required()
    def get_all(self):
        """Get all students"""
        try:
            result = self.student_service.get_all_students()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def create(self):
        """Create a new student"""
        try:
            # Get form data
            data = {
                'id_number': request.form.get('id_number'),
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'year_level': request.form.get('year_level'),
                'gender': request.form.get('gender'),
                'program_code': request.form.get('program_code')
            }
            
            # Get the file if it exists
            picture_file = request.files.get('picture')
            
            if not data['id_number']:
                return jsonify({'error': 'No data provided'}), 400
            
            student = self.student_service.create_student(data, picture_file)
            return jsonify(student), 201
            
        except (DuplicateEntryError, ForeignKeyError) as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def update(self, student_id):
        """Update a student"""
        try:
            # Get form data
            data = {
                'id_number': request.form.get('id_number'),
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'year_level': request.form.get('year_level'),
                'gender': request.form.get('gender'),
                'program_code': request.form.get('program_code')
            }
            
            # Get the file if it exists
            picture_file = request.files.get('picture')
            
            if not data['id_number']:
                return jsonify({'error': 'No data provided'}), 400
            
            student = self.student_service.update_student(student_id, data, picture_file)
            return jsonify(student), 200
            
        except (DuplicateEntryError, NotFoundError, ForeignKeyError) as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def delete(self, student_id):
        """Delete a student"""
        try:
            result = self.student_service.delete_student(student_id)
            return jsonify(result), 200
            
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def get_students_per_program(self):
        """Get number of students per program"""
        try:
            result = self.student_service.get_students_per_program()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500