import pytest
import json
from app import create_app, db
from app.models import User, InventoryItem, Order, IdempotencyKey
from app.utils.auth import hash_password, generate_token

@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        # Seed test data
        user = User(
            email='test@example.com',
            password_hash=hash_password('password123'),
            name='Test User',
            role='customer'
        )
        db.session.add(user)
        
        item = InventoryItem(
            name='Test Item',
            price=10.00,
            quantity=10,
            sku='TEST-001'
        )
        db.session.add(item)
        db.session.commit()
        
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def auth_token(client):
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    data = json.loads(response.data)
    return data['token']

def test_login_success(client):
    """Test successful login"""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert 'user' in data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401

def test_get_inventory_items(client):
    """Test getting inventory items"""
    response = client.get('/inventory/items')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_create_inventory_item(client, auth_token):
    """Test creating inventory item"""
    response = client.post('/inventory/items',
        json={
            'name': 'New Item',
            'price': 20.00,
            'quantity': 5,
            'sku': 'NEW-001'
        },
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New Item'

def test_create_order(client, auth_token):
    """Test creating an order"""
    # Get inventory item ID
    items_response = client.get('/inventory/items')
    items = json.loads(items_response.data)
    item_id = items[0]['id']
    
    idempotency_key = 'test-key-123'
    
    response = client.post('/orders',
        json={
            'items': [
                {'inventory_item_id': item_id, 'quantity': 1}
            ],
            'shipping_address': '123 Test St'
        },
        headers={
            'Authorization': f'Bearer {auth_token}',
            'Idempotency-Key': idempotency_key
        }
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert 'jobs' in data

def test_order_idempotency(client, auth_token):
    """Test order idempotency - same key returns same order"""
    items_response = client.get('/inventory/items')
    items = json.loads(items_response.data)
    item_id = items[0]['id']
    
    idempotency_key = 'idempotent-test-key'
    
    # First request
    response1 = client.post('/orders',
        json={
            'items': [
                {'inventory_item_id': item_id, 'quantity': 1}
            ]
        },
        headers={
            'Authorization': f'Bearer {auth_token}',
            'Idempotency-Key': idempotency_key
        }
    )
    assert response1.status_code == 201
    data1 = json.loads(response1.data)
    order_id_1 = data1['id']
    
    # Second request with same key
    response2 = client.post('/orders',
        json={
            'items': [
                {'inventory_item_id': item_id, 'quantity': 1}
            ]
        },
        headers={
            'Authorization': f'Bearer {auth_token}',
            'Idempotency-Key': idempotency_key
        }
    )
    assert response2.status_code == 201
    data2 = json.loads(response2.data)
    order_id_2 = data2['id']
    
    # Should return same order ID
    assert order_id_1 == order_id_2

def test_rate_limit(client, auth_token):
    """Test rate limiting on orders"""
    items_response = client.get('/inventory/items')
    items = json.loads(items_response.data)
    item_id = items[0]['id']
    
    # Make 11 requests rapidly (limit is 10 per minute)
    for i in range(11):
        response = client.post('/orders',
            json={
                'items': [
                    {'inventory_item_id': item_id, 'quantity': 1}
                ]
            },
            headers={
                'Authorization': f'Bearer {auth_token}',
                'Idempotency-Key': f'rate-limit-test-{i}'
            }
        )
        if i < 10:
            assert response.status_code in [201, 429]  # May hit rate limit
        else:
            # 11th request should definitely hit rate limit
            assert response.status_code == 429

def test_create_donation(client):
    """Test creating a donation"""
    response = client.post('/donations',
        json={
            'amount': 50.00,
            'donation_type': 'one-time',
            'payment_method': 'credit_card'
        }
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert float(data['amount']) == 50.00

def test_job_status(client, auth_token):
    """Test getting job status"""
    # Create an order first
    items_response = client.get('/inventory/items')
    items = json.loads(items_response.data)
    item_id = items[0]['id']
    
    order_response = client.post('/orders',
        json={
            'items': [
                {'inventory_item_id': item_id, 'quantity': 1}
            ]
        },
        headers={
            'Authorization': f'Bearer {auth_token}',
            'Idempotency-Key': 'job-test-key'
        }
    )
    order_data = json.loads(order_response.data)
    job_id = order_data['jobs']['receipt']
    
    # Wait a bit for job to complete
    import time
    time.sleep(2)
    
    # Check job status
    response = client.get(f'/jobs/{job_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] in ['done', 'running']  # Should be done after 2s

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert 'database' in data
    assert 'worker' in data


