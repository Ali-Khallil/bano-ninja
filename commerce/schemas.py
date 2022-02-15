from typing import List

from ninja import Schema, ModelSchema
from pydantic import UUID4

from commerce.models import Order


class MessageOut(Schema):
    detail: str


class CategoryOut(Schema):
    id: UUID4
    name: str


class Productphotos(Schema):
    id: UUID4
    image: str


class ProductOut(Schema):
    id: UUID4
    is_featured: bool
    is_active: bool
    name: str
    description: str
    price: int
    cost: int
    discounted_price: int
    category: CategoryOut
    image: str


class AddToCartPayload(Schema):
    product_id: UUID4
    qty: int


class Items(Schema):
    id: UUID4
    item_qty: int
    product: ProductOut


class Addresscreate(Schema):
    uid: UUID4
    address1: str
    name: str
    phone: str


class CreateOrder(Schema):
    address_id: UUID4
    ordered: bool


#class CreateOrder(Schema):
#    uid: UUID4

class reOrder(ModelSchema):
    class Config:
        model = Order
        model_exclude = ["created", "updated", "uid", "ref_code", "address"]