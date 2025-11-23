# Hope Services API

A Flask-based e-commerce and donations API service with JWT authentication, idempotency support, background job processing, and comprehensive OpenAPI documentation.

## Features

- **JWT Authentication**: Secure token-based authentication
- **Inventory Management**: CRUD operations for inventory items
- **Donations**: Accept one-time and recurring donations
- **Order Processing**: Create orders with idempotency support
- **Background Jobs**: Async processing for receipts and inventory sync
- **Rate Limiting**: Configurable rate limits on endpoints
- **OpenAPI Documentation**: Auto-generated Swagger docs at `/docs`
- **Comprehensive Testing**: pytest test suite

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use make
make install
```

### Database Setup

```bash
# Seed the database with test data
python seed.py

# Or use make
make seed
```

### Run the Server

```bash
# Run directly
python run.py

# Or use make
make run
```

The API will be available at `http://localhost:5000`

### Access Swagger Documentation

Open your browser and navigate to:
```
http://localhost:5000/docs
```

## API Endpoints

### Authentication

- `POST /auth/login` - Login with email/password, returns JWT token

### Inventory

- `GET /inventory/items` - Get all inventory items (optional category filter)
- `POST /inventory/items` - Create new inventory item (requires auth)

### Donations

- `POST /donations` - Create a new donation

### Orders

- `POST /orders` - Create a new order (requires auth, idempotency key)
  - Rate limited: 10 requests per minute per user
  - Requires `Idempotency-Key` header

### Jobs

- `GET /jobs/<job_id>` - Get status of a background job

### Health

- `GET /health` - Health check (database + worker status)

## Authentication

All write endpoints (except donations) require JWT authentication:

```bash
# Login to get token
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "customer@example.com", "password": "password123"}'

# Use token in subsequent requests
curl -X GET http://localhost:5000/inventory/items \
  -H "Authorization: Bearer <your-token>"
```

## Idempotency

Order creation supports idempotency to prevent duplicate charges:

```bash
# First request creates order
curl -X POST http://localhost:5000/orders \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: unique-key-123" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"inventory_item_id": 1, "quantity": 2}]}'

# Second request with same key returns same order
curl -X POST http://localhost:5000/orders \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: unique-key-123" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"inventory_item_id": 1, "quantity": 2}]}'
```

## Background Jobs

When an order is created, two background jobs are automatically queued:

1. **Send Receipt**: Simulates sending order confirmation email
2. **Inventory Sync**: Updates inventory quantities

Check job status:

```bash
curl http://localhost:5000/jobs/<job_id>
```

Job statuses: `queued` → `running` → `done` or `failed`

## Testing

```bash
# Run all tests
pytest -q

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Or use make
make test
```

Test coverage includes:
- Authentication (login, token validation)
- Inventory CRUD operations
- Order creation with idempotency
- Rate limiting
- Background job processing
- Donations

## Rate Limiting

Order creation is rate limited to **10 requests per minute per user** to prevent abuse.

If you exceed the limit, you'll receive a `429 Too Many Requests` response.

## CSRF Protection

JWT-based authentication is stateless and does not require CSRF protection for API endpoints. Session-based endpoints (if any) should include CSRF tokens, but the current implementation uses JWT exclusively.

## Development

### Project Structure

```
hope-services-api/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Marshmallow schemas
│   ├── routes/              # API route blueprints
│   │   ├── auth.py
│   │   ├── inventory.py
│   │   ├── donations.py
│   │   ├── orders.py
│   │   ├── jobs.py
│   │   └── health.py
│   └── utils/               # Utility modules
│       ├── auth.py          # JWT auth helpers
│       ├── idempotency.py   # Idempotency handling
│       └── background_worker.py  # Job processing
├── tests/
│   └── test_api.py         # pytest test suite
├── run.py                  # Application entry point
├── seed.py                 # Database seeding script
├── requirements.txt        # Python dependencies
├── Makefile                # Common commands
├── Dockerfile              # Docker configuration
└── README.md              # This file
```

### Adding New Endpoints

1. Create route handler in appropriate `app/routes/` file
2. Add Swagger documentation using `@swag_from` decorator
3. Add validation schema in `app/schemas.py` if needed
4. Add tests in `tests/test_api.py`

## Docker

### Build Image

```bash
docker build -t hope-services-api .
# Or use make
make docker-build
```

### Run Container

```bash
docker run -p 5000:5000 hope-services-api
# Or use make
make docker-run
```

## Default Test Users

After running `seed.py`:

- **Admin**: `admin@hope.org` / `admin123`
- **Customer**: `customer@example.com` / `password123`

## Environment Variables

- `SECRET_KEY`: Flask secret key (default: development key)
- `JWT_SECRET_KEY`: JWT signing key (default: same as SECRET_KEY)
- `DATABASE_URL`: Database connection string (default: SQLite)

## Production Considerations

- Use a proper password hashing library (bcrypt) instead of SHA256
- Use a production database (PostgreSQL, MySQL) instead of SQLite
- Set secure `SECRET_KEY` and `JWT_SECRET_KEY`
- Use Redis for rate limiting storage
- Implement proper Celery for background jobs
- Add request logging and monitoring
- Set up SSL/TLS
- Configure CORS properly for your frontend domains

## License

MIT


