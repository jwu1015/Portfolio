from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import InventoryItem
from app.schemas import InventoryItemSchema
from app.utils.auth import require_auth

inventory_bp = Blueprint('inventory', __name__)
schema = InventoryItemSchema()

@inventory_bp.route('/items', methods=['GET'])
@swag_from({
    'tags': ['Inventory'],
    'description': 'Get all inventory items',
    'parameters': [
        {
            'name': 'category',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by category'
        }
    ],
    'responses': {
        200: {
            'description': 'List of inventory items',
            'schema': {
                'type': 'array',
                'items': {'type': 'object'}
            }
        }
    }
})
def get_items():
    """Get all inventory items"""
    category = request.args.get('category')
    query = InventoryItem.query
    
    if category:
        query = query.filter_by(category=category)
    
    items = query.all()
    return jsonify([item.to_dict() for item in items]), 200

@inventory_bp.route('/items', methods=['POST'])
@require_auth
@swag_from({
    'tags': ['Inventory'],
    'description': 'Create a new inventory item',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'price': {'type': 'number'},
                    'quantity': {'type': 'integer'},
                    'category': {'type': 'string'},
                    'sku': {'type': 'string'}
                },
                'required': ['name', 'price']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Inventory item created',
            'schema': {'type': 'object'}
        },
        400: {
            'description': 'Validation error'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def create_item():
    """Create a new inventory item"""
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({'error': 'Validation error', 'details': str(e)}), 400
    
    # Check if SKU already exists
    if 'sku' in data and data['sku']:
        existing = InventoryItem.query.filter_by(sku=data['sku']).first()
        if existing:
            return jsonify({'error': 'SKU already exists'}), 400
    
    item = InventoryItem(**data)
    db.session.add(item)
    db.session.commit()
    
    return jsonify(item.to_dict()), 201


