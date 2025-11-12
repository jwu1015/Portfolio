from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import db
from app.models import Order, OrderItem, InventoryItem
from app.schemas import OrderSchema
from app.utils.auth import require_auth, get_current_user
from app.utils.idempotency import require_idempotency
from app.utils.background_worker import background_worker
from flask_limiter.util import get_remote_address
from app import limiter

orders_bp = Blueprint('orders', __name__)
schema = OrderSchema()

@orders_bp.route('', methods=['POST'])
@require_auth
@require_idempotency
@limiter.limit("10 per minute", key_func=lambda: get_current_user().id if get_current_user() else get_remote_address())
@swag_from({
    'tags': ['Orders'],
    'description': 'Create a new order (idempotent)',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'Idempotency-Key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Unique idempotency key for this request'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'inventory_item_id': {'type': 'integer'},
                                'quantity': {'type': 'integer'}
                            },
                            'required': ['inventory_item_id', 'quantity']
                        }
                    },
                    'shipping_address': {'type': 'string'}
                },
                'required': ['items']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Order created',
            'schema': {'type': 'object'}
        },
        400: {
            'description': 'Validation error'
        },
        401: {
            'description': 'Authentication required'
        },
        429: {
            'description': 'Rate limit exceeded'
        }
    }
})
def create_order():
    """Create a new order"""
    try:
        data = schema.load(request.json)
    except Exception as e:
        return jsonify({'error': 'Validation error', 'details': str(e)}), 400
    
    user = get_current_user()
    total_amount = 0
    order_items_data = []
    
    # Validate items and calculate total
    for item_data in data['items']:
        inventory_item = InventoryItem.query.get(item_data['inventory_item_id'])
        if not inventory_item:
            return jsonify({'error': f'Inventory item {item_data["inventory_item_id"]} not found'}), 404
        
        if inventory_item.quantity < item_data['quantity']:
            return jsonify({'error': f'Insufficient quantity for item {inventory_item.name}'}), 400
        
        item_total = float(inventory_item.price) * item_data['quantity']
        total_amount += item_total
        
        order_items_data.append({
            'inventory_item': inventory_item,
            'quantity': item_data['quantity'],
            'price': inventory_item.price
        })
    
    # Create order
    order = Order(
        user_id=user.id,
        total_amount=total_amount,
        status='processing',
        shipping_address=data.get('shipping_address')
    )
    db.session.add(order)
    db.session.flush()  # Get order.id
    
    # Create order items
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            inventory_item_id=item_data['inventory_item'].id,
            quantity=item_data['quantity'],
            price_at_purchase=item_data['price']
        )
        db.session.add(order_item)
    
    db.session.commit()
    
    # Enqueue background jobs
    receipt_job_id = background_worker.enqueue_job('send_receipt', order.id)
    inventory_job_id = background_worker.enqueue_job('inventory_sync', order.id)
    
    order_dict = order.to_dict()
    order_dict['jobs'] = {
        'receipt': receipt_job_id,
        'inventory_sync': inventory_job_id
    }
    
    return jsonify(order_dict), 201

