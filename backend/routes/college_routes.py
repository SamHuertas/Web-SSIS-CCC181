from flask import Blueprint
from controllers.college_controller import CollegeController

colleges_bp = Blueprint('colleges', __name__)
college_controller = CollegeController()

@colleges_bp.route('/colleges', methods=['GET'])
def get_colleges():
    """Get all colleges"""
    return college_controller.get_all()

@colleges_bp.route('/colleges', methods=['POST'])
def add_college():
    """Add a new college"""
    return college_controller.create()

@colleges_bp.route('/colleges/<string:college_code>', methods=['PUT'])
def update_college(college_code):
    """Update a college"""
    return college_controller.update(college_code)

@colleges_bp.route('/colleges/<string:college_code>', methods=['DELETE'])
def delete_college(college_code):
    """Delete a college"""
    return college_controller.delete(college_code)

@colleges_bp.route('/colleges/stats', methods=['GET'])
def get_stats_per_college():
    """Get number of students per college"""
    return college_controller.get_stats()