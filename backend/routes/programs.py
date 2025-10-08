from flask import Blueprint, request, jsonify
from services.program_service import ProgramService
from flask_jwt_extended import jwt_required

programs_bp = Blueprint('programs', __name__)
program_service = ProgramService()

@programs_bp.route('/programs', methods=['GET'])
@jwt_required()
def get_programs():
    """Get all programs"""
    try:
        programs = program_service.get_all_programs()
        return jsonify(programs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@programs_bp.route('/programs', methods=['POST'])
@jwt_required()
def add_program():
    """Add a new program"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Service handles all business logic and duplicate checking
        college = program_service.create_program(data)
        return jsonify(college), 201
        
    except Exception as e:
        # Check if it's a duplicate error (400) or server error (500)
        if 'already exists' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': str(e)}), 500
    
@programs_bp.route('/programs/<string:program_code>', methods=['PUT'])
@jwt_required()
def update_program(program_code):
    """Update a program"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        program = program_service.update_program(program_code, data)
        return jsonify(program), 200
        
    except Exception as e:
        # Check if it's a duplicate error (400) or server error (500)
        if 'already exists' in str(e) or 'not found' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': str(e)}), 500
    
@programs_bp.route('/programs/<string:program_code>', methods=['DELETE'])
@jwt_required()
def delete_program(program_code):
    """Delete a program"""
    try:
        result = program_service.delete_program(program_code)
        return jsonify(result), 200
        
    except Exception as e:
        # Check if it's a not found error (404) or server error (500)
        if 'not found' in str(e):
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 500