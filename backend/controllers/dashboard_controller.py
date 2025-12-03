from flask import jsonify
from services.dashboard_service import DashboardService

class DashboardController:
    def __init__(self):
        self.dashboard_service = DashboardService()
    
    def get_summary(self):
        """Get complete dashboard summary"""
        try:
            summary = self.dashboard_service.get_dashboard_summary()
            return jsonify(summary), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_totals(self):
        """Get only total counts"""
        try:
            totals = self.dashboard_service.get_totals()
            return jsonify(totals), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_students_per_college(self):
        """Get students per college"""
        try:
            data = self.dashboard_service.get_students_per_college()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_top_programs(self):
        """Get top programs"""
        try:
            data = self.dashboard_service.get_top_programs()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_college_stats(self):
        """Get college statistics"""
        try:
            data = self.dashboard_service.get_college_stats()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500