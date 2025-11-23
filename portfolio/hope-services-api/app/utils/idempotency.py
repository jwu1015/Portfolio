from functools import wraps
from flask import request, jsonify
from app import db
from app.models import IdempotencyKey
from datetime import datetime, timedelta
import json

def require_idempotency(f):
    """Decorator to handle idempotency keys for POST requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        idempotency_key = request.headers.get('Idempotency-Key')
        
        if not idempotency_key:
            return jsonify({'error': 'Idempotency-Key header is required'}), 400
        
        # Check if this key already exists
        existing_key = IdempotencyKey.query.filter_by(key=idempotency_key).first()
        
        if existing_key:
            # Check if expired
            if existing_key.expires_at < datetime.utcnow():
                # Delete expired key
                db.session.delete(existing_key)
                db.session.commit()
            else:
                # Return cached response
                import flask
                response = flask.make_response(existing_key.response_body)
                response.status_code = existing_key.response_status
                response.headers['Content-Type'] = 'application/json'
                return response
        
        # Store response after execution
        original_response = None
        
        try:
            # Execute the original function
            result = f(*args, **kwargs)
            
            # Extract response data
            if isinstance(result, tuple):
                response_data, status_code = result
                if isinstance(response_data, dict):
                    response_body = json.dumps(response_data)
                else:
                    response_body = str(response_data)
            else:
                status_code = 200
                if isinstance(result, dict):
                    response_body = json.dumps(result)
                else:
                    response_body = str(result)
            
            # Store idempotency key
            idempotency_record = IdempotencyKey(
                key=idempotency_key,
                request_method=request.method,
                request_path=request.path,
                response_status=status_code,
                response_body=response_body,
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.session.add(idempotency_record)
            db.session.commit()
            
            return result
            
        except Exception as e:
            # Don't store failed requests as idempotent
            raise
    
    return decorated_function


