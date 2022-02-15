
from typing import List

from django.db.models import Q   # Q object working with search
from django.shortcuts import get_object_or_404
from ninja import Router

# Create your views here.
from pydantic import UUID4

from commerce.models import Order, Product, Category, Item, Address
from commerce.schemas import MessageOut, CreateOrder, ProductOut, CategoryOut, AddToCartPayload, \
    Items, Addresscreate, reOrder

commerce_controller = Router(tags=['products'])
order_controller = Router(tags=['order'])


@commerce_controller.get('products', response={
    200: List[ProductOut],
})
def list_products(request, search: str = None, Categorys: UUID4 = None, featuerd: bool = None, is_active: bool = None, ):
    products = Product.objects.all()

    if q:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    if Categorys:
        products = products.filter(category__id=Categorys
                                   )
    if featuerd:
        products = products.filter(is_featured=featuerd
                                   )
    if is_active:
        products = products.filter(is_active=is_active
                                   )
    return products


@commerce_controller.get('products/{id}', response={
    200: ProductOut
})
def retrieve_product(request, id):
    return get_object_or_404(Product, id=id)


@commerce_controller.post('address', response={
    201: Addresscreate,
    400: MessageOut
})
def create_address(request, payload: Addresscreate):
    try:

        adress = Address.objects.create(**payload.dict())
    except:
        return 400, {'detail': 'something wrong happened!'}
    adress.save()
    return 201, adress


@commerce_controller.get('Categorys', response={
    200: List[CategoryOut],
})
def list_Categorys(request):
    categorys = Category.objects.all()
    return categorys


@order_controller.get('Items/{user_id}', response={
    200: List[Items],
})
def list_itmes(request, user_id):
    items = Item.objects.all().filter(uid=user_id, ordered=False)
    return items


@order_controller.post('add-to-cart/{user_id}', response=MessageOut, )
def add_to_cart(request, payload: AddToCartPayload, user_id: UUID4):
    payload_validated = payload.copy()
    if payload.qty < 1:
        payload_validated.qty = 1

    try:
        item = Item.objects.get(product_id=payload.product_id, uid=user_id, ordered=False)
    except Item.DoesNotExist:
        Item.objects.create(product_id=payload.product_id, uid=user_id, item_qty=payload_validated.qty,
                            ordered=False)
        return 200, {'detail': 'item added to cart successfully!'}

    item.item_qty += payload_validated.qty
    item.save()
    return 200, {'detail': 'item qty updated successfully!'}


@order_controller.post('increase-item/{user_id}/{item_id}', response=MessageOut)
def increase_item_qty(request, item_id: UUID4, user_id: UUID4):
    item = get_object_or_404(Item, id=item_id, uid=user_id)
    item.item_qty += 1
    item.save()

    return 200, {'detail': 'Item qty increased successfully!'}


@order_controller.post('decrease-item/{user_id}/{item_id}', response=MessageOut)
def decrease_item_qty(request, item_id: UUID4, user_id: UUID4):
    item = get_object_or_404(Item, id=item_id, uid=user_id)
    item.item_qty -= 1
    if item.item_qty == 0:
        item.delete()
    else:
        item.save()
    return 200, {'detail': 'Item qty decreased successfully!'}


@order_controller.post('create_order', response=MessageOut)
def creat_order(request, payload: CreateOrder, ):

    order = Order.objects.create(**payload.dict())



    return 200, {'detail': 'Order is created '}


@order_controller.get('delete_order/{order_id}', response={
    200: MessageOut,
    400: MessageOut
})
def delete_order(request, order_id: UUID4):
    try:
        order = get_object_or_404(Order, id=order_id, )
        order.delete()
    except:
        return 400, {'detail': 'something went wrong'}

    return 200, {'detail': ' deleted'}


@order_controller.get('get_user_order/{uid}', response={
    200: List[reOrder],
    400: MessageOut
})
def get_user_order(request, uid: UUID4):
    try:
        orders = Order.objects.filter(uid=uid, )
    except:
        return 400, {'detail': 'something went wrong'}

    return 200, orders