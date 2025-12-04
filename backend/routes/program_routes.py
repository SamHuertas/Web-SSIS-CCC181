from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.program_controller import ProgramController

programs_bp = Blueprint('programs', __name__)
program_controller = ProgramController()

@programs_bp.route('/programs', methods=['GET'])
@jwt_required()
def get_programs():
    """Get all programs"""
    return program_controller.get_all()

@programs_bp.route('/programs', methods=['POST'])
@jwt_required()
def add_program():
    """Add a new program"""
    return program_controller.create()

@programs_bp.route('/programs-list', methods=['GET'])

def get_programs_list():
    """Get all programs as simple list (for dropdowns)"""
    return program_controller.get_all_list()

@programs_bp.route('/programs/<string:program_code>', methods=['PUT'])
@jwt_required()
def update_program(program_code):
    """Update a program"""
    return program_controller.update(program_code)

@programs_bp.route('/programs/<string:program_code>', methods=['DELETE'])
@jwt_required()
def delete_program(program_code):
    """Delete a program"""
    return program_controller.delete(program_code)