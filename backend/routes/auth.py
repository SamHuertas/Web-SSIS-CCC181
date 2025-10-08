from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        
        # Validate input
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if len(data['password']) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        user = auth_service.register_user(
            data['username'],
            data['email'],
            data['password']
        )
        
        # Create access token
        access_token = create_access_token(identity=str(user['user_id']))
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = auth_service.authenticate_user(
            data['email'],
            data['password']
        )
        
        # Create access token
        access_token = create_access_token(identity=str(user['user_id']))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify if token is valid"""
    try:
        current_user_id = get_jwt_identity()
        return jsonify({
            'valid': True,
            'user_id': current_user_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401