
from .auth_routes import auth_bp
from .college_routes import colleges_bp
from .program_routes import programs_bp
from .student_routes import students_bp

__all__ = [
    'auth_bp',
    'colleges_bp',
    'programs_bp',
    'students_bp'
]