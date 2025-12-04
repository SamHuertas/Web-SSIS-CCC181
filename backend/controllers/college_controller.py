from flask import request, jsonify
from services.college_service import CollegeService
from utils.exceptions import DuplicateEntryError, NotFoundError

class CollegeController:
    def __init__(self):
        self.college_service = CollegeService()
    
    def get_all(self):
        """Get all colleges with pagination, search, and sorting"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', '', type=str)
            sort_field = request.args.get('sort_field', 'college_code', type=str)
            sort_direction = request.args.get('sort_direction', 'asc', type=str)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:  # Max 100 items per page
                per_page = 10
            
            result = self.college_service.get_all_colleges(
                page, per_page, search, sort_field, sort_direction
            )
            
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_all_list(self):
        """Get all colleges without pagination (for dropdowns)"""
        try:
            result = self.college_service.get_all_colleges_list()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def create(self):
        """Create a new college"""
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            college = self.college_service.create_college(data)
            return jsonify(college), 201
            
        except DuplicateEntryError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update(self, college_code):
        """Update a college"""
        try:
            data = request.json
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            college = self.college_service.update_college(college_code, data)
            return jsonify(college), 200
            
        except (DuplicateEntryError, NotFoundError) as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def delete(self, college_code):
        """Delete a college"""
        try:
            result = self.college_service.delete_college(college_code)
            return jsonify(result), 200
            
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_stats(self):
        """Get college statistics"""
        try:
            stats = self.college_service.get_stats_per_college()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500