from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.dashboard_controller import DashboardController

dashboard_bp = Blueprint('dashboard', __name__)
dashboard_controller = DashboardController()

@dashboard_bp.route('/dashboard/summary', methods=['GET'])
@jwt_required()
def get_dashboard_summary():
    """Get complete dashboard summary"""
    return dashboard_controller.get_summary()

@dashboard_bp.route('/dashboard/totals', methods=['GET'])
@jwt_required()
def get_dashboard_totals():
    """Get only total counts"""
    return dashboard_controller.get_totals()

@dashboard_bp.route('/dashboard/students-per-college', methods=['GET'])
@jwt_required()
def get_dashboard_students_per_college():
    """Get students per college"""
    return dashboard_controller.get_students_per_college()

@dashboard_bp.route('/dashboard/top-programs', methods=['GET'])
@jwt_required()
def get_dashboard_top_programs():
    """Get top programs by enrollment"""
    return dashboard_controller.get_top_programs()

@dashboard_bp.route('/dashboard/college-stats', methods=['GET'])
@jwt_required()
def get_dashboard_college_stats():
    """Get college statistics"""
    return dashboard_controller.get_college_stats()