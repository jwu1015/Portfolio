from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.utils.background_worker import background_worker

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/<job_id>', methods=['GET'])
@swag_from({
    'tags': ['Jobs'],
    'description': 'Get job status by ID',
    'parameters': [
        {
            'name': 'job_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Job ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Job status',
            'schema': {
                'type': 'object',
                'properties': {
                    'job_id': {'type': 'string'},
                    'job_type': {'type': 'string'},
                    'status': {'type': 'string'},
                    'order_id': {'type': 'integer'}
                }
            }
        },
        404: {
            'description': 'Job not found'
        }
    }
})
def get_job_status(job_id):
    """Get job status"""
    status = background_worker.get_job_status(job_id)
    
    if not status:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(status), 200


