from db import get_connection
from queries.dashboard_queries import DashboardQueries

class DashboardRepository:
    def __init__(self):
        self.queries = DashboardQueries()
    
    def get_total_students(self):
        """Get total number of students"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_TOTAL_STUDENTS)
            result = cur.fetchone()
            return result['total_students'] if result else 0
    
    def get_total_programs(self):
        """Get total number of programs"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_TOTAL_PROGRAMS)
            result = cur.fetchone()
            return result['total_programs'] if result else 0
    
    def get_total_colleges(self):
        """Get total number of colleges"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_TOTAL_COLLEGES)
            result = cur.fetchone()
            return result['total_colleges'] if result else 0
    
    def get_students_per_college(self):
        """Get top 7 colleges by student count"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_STUDENTS_PER_COLLEGE)
            return cur.fetchall()
    
    def get_top_programs(self):
        """Get top 7 programs by enrollment"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_TOP_PROGRAMS)
            return cur.fetchall()
    
    def get_college_stats(self):
        """Get comprehensive college statistics"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_COLLEGE_STATS)
            return cur.fetchall()
    
    def get_dashboard_summary(self):
        """Get all dashboard data - FIXED: No shared cursor context"""
        # Each method opens its own connection and cursor
        total_students = self.get_total_students()
        total_programs = self.get_total_programs()
        total_colleges = self.get_total_colleges()
        students_per_college = self.get_students_per_college()
        top_programs = self.get_top_programs()
        college_stats = self.get_college_stats()
        
        # Debug log to check counts
        print(f"DEBUG: students_per_college count: {len(students_per_college)}")
        print(f"DEBUG: top_programs count: {len(top_programs)}")
        print(f"DEBUG: college_stats count: {len(college_stats)}")
        
        return {
            'total_students': total_students,
            'total_programs': total_programs,
            'total_colleges': total_colleges,
            'students_per_college': students_per_college,
            'top_programs': top_programs,
            'college_stats': college_stats
        }