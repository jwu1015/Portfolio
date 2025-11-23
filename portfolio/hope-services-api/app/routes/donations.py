from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import Donation
from app.schemas import DonationSchema
from app.utils.auth import get_current_user

donations_bp = Blueprint('donations', __name__)
schema = DonationSchema()

@donations_bp.route('', methods=['POST'])
@swag_from({
    'tags': ['Donations'],
    'description': 'Create a new donation',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'amount': {'type': 'number'},
                    'donation_type': {'type': 'string'},
                    'payment_method': {'type': 'string'}
                },
                'required': ['amount']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Donation created',
            'schema': {'type': 'object'}
        },
        400: {
            'description': 'Validation error'
        }
    }
})
def create_donation():
    """Create a new donation"""
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({'error': 'Validation error', 'details': str(e)}), 400
    
    # Try to get current user (optional)
    user = get_current_user()
    if user:
        data['user_id'] = user.id
    
    donation = Donation(**data)
    donation.status = 'completed'  # Auto-complete for simplicity
    db.session.add(donation)
    db.session.commit()
    
    return jsonify(donation.to_dict()), 201


