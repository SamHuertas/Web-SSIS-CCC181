from flask import Blueprint, request, jsonify
from utils import SupabaseManager

students_bp = Blueprint('students', __name__)

supabase_manager = SupabaseManager()
supabase = supabase_manager.get_client()

@students_bp.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        result = supabase.table('students').select('id_number, first_name, last_name, program_code, year_level, gender').execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500