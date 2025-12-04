from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.college_controller import CollegeController

colleges_bp = Blueprint('colleges', __name__)
college_controller = CollegeController()

@colleges_bp.route('/colleges', methods=['GET'])
@jwt_required()
def get_colleges():
    """Get all colleges"""
    return college_controller.get_all()

@colleges_bp.route('/colleges', methods=['POST'])
@jwt_required()
def add_college():
    """Add a new college"""
    return college_controller.create()

@colleges_bp.route('/colleges-list', methods=['GET'])
def get_colleges_list():
    """Get all colleges as simple list (for dropdowns)"""
    return college_controller.get_all_list()

@colleges_bp.route('/colleges/<string:college_code>', methods=['PUT'])
@jwt_required()
def update_college(college_code):
    """Update a college"""
    return college_controller.update(college_code)

@colleges_bp.route('/colleges/<string:college_code>', methods=['DELETE'])
@jwt_required()
def delete_college(college_code):
    """Delete a college"""
    return college_controller.delete(college_code)

@colleges_bp.route('/colleges/stats', methods=['GET'])
@jwt_required()
def get_stats_per_college():
    """Get number of students per college"""
    return college_controller.get_stats()