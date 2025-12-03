from repositories.dashboard_repository import DashboardRepository

class DashboardService:
    def __init__(self):
        self.dashboard_repository = DashboardRepository()
    
    def get_dashboard_summary(self):
        """Get comprehensive dashboard summary"""
        return self.dashboard_repository.get_dashboard_summary()
    
    def get_totals(self):
        """Get only total counts"""
        return {
            'total_students': self.dashboard_repository.get_total_students(),
            'total_programs': self.dashboard_repository.get_total_programs(),
            'total_colleges': self.dashboard_repository.get_total_colleges()
        }
    
    def get_students_per_college(self):
        """Get students per college"""
        return self.dashboard_repository.get_students_per_college()
    
    def get_top_programs(self):
        """Get top programs by enrollment"""
        return self.dashboard_repository.get_top_programs()
    
    def get_college_stats(self):
        """Get comprehensive college statistics"""
        return self.dashboard_repository.get_college_stats()