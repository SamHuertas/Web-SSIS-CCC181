from flask import request, jsonify
from services.program_service import ProgramService
from utils.exceptions import DuplicateEntryError, NotFoundError, ForeignKeyError

class ProgramController:
    def __init__(self):
        self.program_service = ProgramService()
    
    def get_all(self):
        """Get all programs with pagination, search, and sorting"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', '', type=str)
            sort_field = request.args.get('sort_field', 'program_code', type=str)
            sort_direction = request.args.get('sort_direction', 'asc', type=str)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:  # Max 100 items per page
                per_page = 10
            
            result = self.program_service.get_all_programs(
                page, per_page, search, sort_field, sort_direction
            )
            
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
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
    
    def delete(self, program_code):
        """Delete a program"""
        try:
            result = self.program_service.delete_program(program_code)
            return jsonify(result), 200
            
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500