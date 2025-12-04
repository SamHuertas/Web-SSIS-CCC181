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
        """Get colleges by student count"""
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(self.queries.GET_STUDENTS_PER_COLLEGE)
            return cur.fetchall()
    
    def get_top_programs(self, limit=7):
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
        """Get all dashboard data using optimized separate queries"""
        with get_connection() as conn, conn.cursor() as cur:
            # Get totals
            cur.execute(self.queries.GET_TOTAL_STUDENTS)
            total_students = cur.fetchone()['total_students'] or 0
            
            cur.execute(self.queries.GET_TOTAL_PROGRAMS)
            total_programs = cur.fetchone()['total_programs'] or 0
            
            cur.execute(self.queries.GET_TOTAL_COLLEGES)
            total_colleges = cur.fetchone()['total_colleges'] or 0
            
            # Get top 7 colleges
            cur.execute(self.queries.GET_STUDENTS_PER_COLLEGE)
            students_per_college = cur.fetchall() or []
            
            # Get top 7 programs
            cur.execute(self.queries.GET_TOP_PROGRAMS)
            top_programs = cur.fetchall() or []
            
            # Get all college stats
            cur.execute(self.queries.GET_COLLEGE_STATS)
            college_stats = cur.fetchall() or []
            
            return {
                'total_students': total_students,
                'total_programs': total_programs,
                'total_colleges': total_colleges,
                'students_per_college': students_per_college,
                'top_programs': top_programs,
                'college_stats': college_stats
            }