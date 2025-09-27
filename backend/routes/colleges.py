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