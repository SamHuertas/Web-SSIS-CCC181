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