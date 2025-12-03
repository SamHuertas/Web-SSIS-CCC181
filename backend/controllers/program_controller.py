from flask import request, jsonify
from flask_jwt_extended import jwt_required
from services.program_service import ProgramService
from utils.exceptions import DuplicateEntryError, NotFoundError, ForeignKeyError

class ProgramController:
    def __init__(self):
        self.program_service = ProgramService()
    
    @jwt_required()
    def get_all(self):
        """Get all programs"""
        try:
            programs = self.program_service.get_all_programs()
            return jsonify(programs), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def create(self):
        """Create a new program"""
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            program = self.program_service.create_program(data)
            return jsonify(program), 201
            
        except (DuplicateEntryError, ForeignKeyError) as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def update(self, program_code):
        """Update a program"""
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            program = self.program_service.update_program(program_code, data)
            return jsonify(program), 200
            
        except (DuplicateEntryError, NotFoundError, ForeignKeyError) as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
    def delete(self, program_code):
        """Delete a program"""
        try:
            result = self.program_service.delete_program(program_code)
            return jsonify(result), 200
            
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500