
from django.contrib import admin

from .models import Product, ProductImage, Category, Address, Order, Item


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'name',
        'description',
        'price',
        'discounted_price',
        'category',
        'is_featured',
        'is_active',
        'image',
    )
    list_filter = (
        'created',
        'updated',
        'category',
        'is_featured',
        'is_active',
    )
    search_fields = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated', 'image', 'is_default_image')
    list_filter = ('created', 'updated', 'is_default_image')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name', 'created', 'updated')
    list_filter = ('parent', 'created', 'updated')
    search_fields = ('name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'uid',
        'address1',
        'name',
        'phone',
    )
    list_filter = ('created', 'updated')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'uid',
        'address',
        'total',
        'title',
        'ref_code',
        'ordered',
    )
    list_filter = ('created', 'updated', 'address', 'ordered')
    raw_id_fields = ('items',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'updated',
        'uid',
        'product',
        'item_qty',
        'ordered',
    )
    list_filter = ('created', 'updated', 'product', 'ordered')