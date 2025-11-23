from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import User
from app.schemas import UserLoginSchema
from app.utils.auth import hash_password, verify_password, generate_token
from flask import current_app

auth_bp = Blueprint('auth', __name__)
schema = UserLoginSchema()

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Login with email and password to get JWT token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'user': {'type': 'object'}
                }
            }
        },
        401: {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    """Login endpoint"""
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({'error': 'Invalid input', 'details': str(e)}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not verify_password(data['password'], user.password_hash):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    secret_key = current_app.config.get('JWT_SECRET_KEY', current_app.config.get('SECRET_KEY'))
    token = generate_token(user.id, secret_key)
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200

