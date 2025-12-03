from flask import request, jsonify
from flask_jwt_extended import jwt_required
from services.college_service import CollegeService
from utils.exceptions import DuplicateEntryError, NotFoundError

class CollegeController:
    def __init__(self):
        self.college_service = CollegeService()
    
    @jwt_required()
    def get_all(self):
        """Get all colleges"""
        try:
            colleges = self.college_service.get_all_colleges()
            return jsonify(colleges), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @jwt_required()
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
    
    @jwt_required()
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
    
    @jwt_required()
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