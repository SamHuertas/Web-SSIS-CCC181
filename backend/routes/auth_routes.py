from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    return auth_controller.register()

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    return auth_controller.login()

@auth_bp.route('/auth/verify', methods=['GET'])
def verify_token():
    """Verify if token is valid"""
    return auth_controller.verify_token()