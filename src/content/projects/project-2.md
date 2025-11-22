---
title: "Hope Services E-Commerce API"
date: "2025-01-20"
summary: "Production-grade Flask REST API with JWT auth, idempotency, background jobs, and comprehensive OpenAPI documentation"
tags: ["python", "flask", "sqlalchemy", "jwt", "rest-api", "pytest", "openapi"]
cover: "/images/projects/hope-api-cover.jpg"
links:
  demo: "https://hope-services-api-docs.netlify.app"
  code: "https://github.com/yourusername/Portfolio/tree/main/hope-services-api"
published: true
---

Architected and shipped a complete e-commerce and donations API that handles inventory management, order processing, and donation flows with enterprise-grade reliability. The system implements JWT authentication, idempotent order creation (preventing duplicate charges), rate limiting, and background job processing that simulates Celery behavior. Every endpoint is validated with Marshmallow schemas, documented with Flasgger/Swagger, and covered by a comprehensive pytest test suite. The API supports both customer-facing operations and admin inventory management, with structured logging and health checks for production monitoring.

**Key Features:**
- JWT-based authentication with protected endpoints
- SQLAlchemy models for users, inventory, orders, donations, and idempotency keys
- Background worker thread for receipt sending and inventory synchronization
- Rate limiting (10 requests/minute per user on orders)
- Auto-generated OpenAPI/Swagger documentation at `/docs`
- Full test coverage with pytest (auth, CRUD, idempotency, rate limits, jobs)
- Docker support and seed scripts for easy setup

**My Role:** Backend engineer, DevOps

**Impact:** Delivered a production-ready API that demonstrates best practices in security, reliability, and developer experience. The idempotency system prevents costly duplicate transactions, while the comprehensive documentation and tests make it easy for teams to integrate and maintain.

