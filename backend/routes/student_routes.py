from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.student_controller import StudentController

students_bp = Blueprint('students', __name__)
student_controller = StudentController()


@students_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """Get all students"""
    return student_controller.get_all()

@students_bp.route('/students', methods=['POST'])
@jwt_required()
def add_student():
    """Add a new student"""
    return student_controller.create()

@students_bp.route('/students/<string:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    """Update a student"""
    return student_controller.update(student_id)

@students_bp.route('/students/<string:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    """Delete a student"""
    return student_controller.delete(student_id)

@students_bp.route('/students/programs', methods=['GET'])
@jwt_required()
def get_students_per_program():
    """Get number of students per program"""
    return student_controller.get_students_per_program()