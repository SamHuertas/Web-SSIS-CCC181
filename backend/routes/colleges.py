from flask import Blueprint, request, jsonify
from utils import SupabaseManager

colleges_bp = Blueprint('colleges', __name__)

supabase_manager = SupabaseManager()
supabase = supabase_manager.get_client()

@colleges_bp.route('/colleges', methods=['GET'])
def get_colleges():
    """Get all colleges"""
    try:
        result = supabase.table('colleges').select('college_code, college_name').execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@colleges_bp.route('/colleges', methods=['POST'])
def add_college():
    """Add a new college"""
    try:
        data = request.json
        result = supabase.table('colleges').insert({
            'college_code': data['college_code'],
            'college_name': data['college_name']
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@colleges_bp.route('/colleges/<string:college_code>', methods=['PUT'])
def update_college(college_code):
    """Update a college"""
    try:
        data = request.json
        
        # If college_code is being changed, check if new code already exists
        if data['college_code'] != college_code:
            existing_new_code = supabase.table('colleges').select('*').eq('college_code', data['college_code']).execute()
            if existing_new_code.data:
                return jsonify({'error': 'College code already exists'}), 400
        
        # Update college using the original college_code as filter
        result = supabase.table('colleges').update({
            'college_code': data['college_code'],
            'college_name': data['college_name']
        }).eq('college_code', college_code).execute()
        
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500