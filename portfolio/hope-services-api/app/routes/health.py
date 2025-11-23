from flask import Blueprint, jsonify
from flasgger import swag_from
from app import db
from app.utils.background_worker import background_worker

health_bp = Blueprint('health', __name__)

@health_bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'description': 'Health check endpoint',
    'responses': {
        200: {
            'description': 'Service health status',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'database': {'type': 'string'},
                    'worker': {'type': 'string'}
                }
            }
        }
    }
})
def health_check():
    """Health check endpoint"""
    # Check database
    db_status = 'ok'
    try:
        db.session.execute('SELECT 1')
    except Exception:
        db_status = 'error'
    
    # Check worker
    worker_status = 'running' if background_worker.running else 'stopped'
    
    overall_status = 'ok' if db_status == 'ok' and worker_status == 'running' else 'degraded'
    
    return jsonify({
        'status': overall_status,
        'database': db_status,
        'worker': worker_status
    }), 200


