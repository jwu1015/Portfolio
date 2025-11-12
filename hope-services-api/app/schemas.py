from marshmallow import Schema, fields, validate, ValidationError

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class InventoryItemSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0))
    quantity = fields.Int(validate=validate.Range(min=0))
    category = fields.Str(validate=validate.Length(max=100))
    sku = fields.Str(validate=validate.Length(max=100))

class DonationSchema(Schema):
    amount = fields.Decimal(required=True, places=2, validate=validate.Range(min=0.01))
    donation_type = fields.Str(validate=validate.OneOf(['one-time', 'recurring', 'monthly', 'annual']))
    payment_method = fields.Str(validate=validate.Length(max=50))
    user_id = fields.Int(allow_none=True)

class OrderItemSchema(Schema):
    inventory_item_id = fields.Int(required=True, validate=validate.Range(min=1))
    quantity = fields.Int(required=True, validate=validate.Range(min=1))

class OrderSchema(Schema):
    items = fields.List(fields.Nested(OrderItemSchema), required=True, validate=validate.Length(min=1))
    shipping_address = fields.Str(allow_none=True)


