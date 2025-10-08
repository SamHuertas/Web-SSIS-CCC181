from flask import Blueprint, request, jsonify
from services.college_service import CollegeService
from flask_jwt_extended import jwt_required

colleges_bp = Blueprint('colleges', __name__)
college_service = CollegeService()

@colleges_bp.route('/colleges', methods=['GET'])
@jwt_required()
def get_colleges():
    """Get all colleges"""
    try:
        colleges = college_service.get_all_colleges()
        return jsonify(colleges)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@colleges_bp.route('/colleges', methods=['POST'])
@jwt_required()
def add_college():
    """Add a new college"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Service handles all business logic and duplicate checking
        college = college_service.create_college(data)
        return jsonify(college), 201
        
    except Exception as e:
        # Check if it's a duplicate error (400) or server error (500)
        if 'already exists' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': str(e)}), 500
    
@colleges_bp.route('/colleges/<string:college_code>', methods=['PUT'])
@jwt_required()
def update_college(college_code):
    """Update a college"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        college = college_service.update_college(college_code, data)
        return jsonify(college), 200
        
    except Exception as e:
        # Check if it's a duplicate error (400) or server error (500)
        if 'already exists' in str(e) or 'not found' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': str(e)}), 500
    
@colleges_bp.route('/colleges/<string:college_code>', methods=['DELETE'])
@jwt_required()
def delete_college(college_code):
    """Delete a college"""
    try:
        result = college_service.delete_college(college_code)
        return jsonify(result), 200
        
    except Exception as e:
        # Check if it's a not found error (404) or server error (500)
        if 'not found' in str(e):
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 500

@colleges_bp.route('/colleges/stats', methods=['GET'])
def get_stats_per_college():
    """Get number of students per college"""
    try:
        stats = college_service.get_stats_per_college()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500