from flask import Blueprint, request, jsonify
from services.student_service import StudentService 
from flask_jwt_extended import jwt_required

students_bp = Blueprint('students', __name__)
student_service = StudentService()

@students_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """Get all students"""
    try:
        result = student_service.get_all_students()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@students_bp.route('/students', methods=['POST'])
@jwt_required()
def add_student():
    """Add a new student"""
    try:
        # Get form data instead of JSON
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

        # Service handles all business logic and duplicate checking
        student = student_service.create_student(data, picture_file)
        return jsonify(student), 201

    except Exception as e:
        # Check if it's a duplicate error (400) or server error (500)
        if 'already exists' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': str(e)}), 500
    
@students_bp.route('/students/<string:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    """Update a student"""
    try:
        # Get form data instead of JSON 
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
        
        student = student_service.update_student(student_id, data, picture_file)
        return jsonify(student), 200
        
    except Exception as e:
        # Check if it's a duplicate error (400) or server error (500)
        if 'already exists' in str(e) or 'not found' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': str(e)}), 500
    
@students_bp.route('/students/<string:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    """Delete a student"""
    try:
        result = student_service.delete_student(student_id)
        return jsonify(result), 200
        
    except Exception as e:
        # Check if it's a not found error (404) or server error (500)
        if 'not found' in str(e):
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 500

@students_bp.route('/students/programs', methods=['GET'])
@jwt_required()
def get_students_per_program():
    """Get number of students per program"""
    try:
        result = student_service.get_students_per_program()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500