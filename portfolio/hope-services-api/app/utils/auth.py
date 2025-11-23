from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from app import db
from app.models import User

def generate_token(user_id, secret_key):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_token(token, secret_key):
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Get current user from JWT token"""
    from flask import current_app
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(' ')[1]  # Remove 'Bearer ' prefix
    except IndexError:
        return None
    
    secret_key = current_app.config.get('JWT_SECRET_KEY', current_app.config.get('SECRET_KEY'))
    user_id = verify_token(token, secret_key)
    if not user_id:
        return None
    
    return User.query.get(user_id)

def require_auth(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Simple password hashing (use bcrypt in production)"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

