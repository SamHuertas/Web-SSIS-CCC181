from flask import Blueprint, request, jsonify
from utils import SupabaseManager
from services.college_service import CollegeService

colleges_bp = Blueprint('colleges', __name__)

supabase_manager = SupabaseManager()
supabase = supabase_manager.get_client()
college_service = CollegeService(supabase)

@colleges_bp.route('/colleges', methods=['GET'])
def get_colleges():
    """Get all colleges"""
    try:
        colleges = college_service.get_all_colleges()
        return jsonify(colleges)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@colleges_bp.route('/colleges', methods=['POST'])
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