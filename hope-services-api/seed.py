from app import create_app, db
from app.models import User, InventoryItem
from app.utils.auth import hash_password

app = create_app()

def seed_database():
    with app.app_context():
        # Clear existing data (optional - comment out in production)
        # db.drop_all()
        # db.create_all()
        
        # Create users
        if not User.query.filter_by(email='admin@hope.org').first():
            admin = User(
                email='admin@hope.org',
                password_hash=hash_password('admin123'),
                name='Admin User',
                role='admin'
            )
            db.session.add(admin)
        
        if not User.query.filter_by(email='customer@example.com').first():
            customer = User(
                email='customer@example.com',
                password_hash=hash_password('password123'),
                name='John Doe',
                role='customer'
            )
            db.session.add(customer)
        
        # Create inventory items
        items_data = [
            {
                'name': 'Food Box',
                'description': 'Emergency food supply box',
                'price': 25.00,
                'quantity': 100,
                'category': 'food',
                'sku': 'FB-001'
            },
            {
                'name': 'Blanket',
                'description': 'Warm winter blanket',
                'price': 15.00,
                'quantity': 50,
                'category': 'clothing',
                'sku': 'BL-001'
            },
            {
                'name': 'Hygiene Kit',
                'description': 'Personal hygiene essentials',
                'price': 10.00,
                'quantity': 75,
                'category': 'hygiene',
                'sku': 'HK-001'
            },
            {
                'name': 'School Supplies',
                'description': 'Backpack with school supplies',
                'price': 30.00,
                'quantity': 40,
                'category': 'education',
                'sku': 'SS-001'
            },
        ]
        
        for item_data in items_data:
            if not InventoryItem.query.filter_by(sku=item_data['sku']).first():
                item = InventoryItem(**item_data)
                db.session.add(item)
        
        db.session.commit()
        print("Database seeded successfully!")
        print("\nTest users:")
        print("  Admin: admin@hope.org / admin123")
        print("  Customer: customer@example.com / password123")

if __name__ == '__main__':
    seed_database()


