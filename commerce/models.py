
# Create your models here.
import uuid

# Register your models here.
from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)


class Product(Entity):
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', null=True, blank=True)
    cost = models.DecimalField('cost', max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField('price', max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField('discounted price', max_digits=10, decimal_places=2)
    category = models.ForeignKey('commerce.Category', verbose_name='category', related_name='products',
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    is_featured = models.BooleanField('is featured')
    is_active = models.BooleanField('is active')
    image = models.ImageField('image', upload_to='product/')

    def __str__(self):
        return self.image.url


class ProductImage(Entity):
    image = models.ImageField('image')
    is_default_image = models.BooleanField('is default image')

    def __str__(self):
        pass


class Category(Entity):
    parent = models.ForeignKey('self', verbose_name='parent', related_name='children',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    name = models.CharField('name', max_length=255)


    def __str__(self):
        if self.parent:
            return f'-   {self.name}'
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'


class Address(Entity):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    address1 = models.CharField('address1', max_length=255)
    name = models.CharField('name', null=True, blank=True, max_length=255)
    phone = models.CharField('phone', max_length=255)

    def __str__(self):
        return f' {self.address1} - {self.phone}'


class Order(Entity):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    address = models.ForeignKey('Address', verbose_name='address', null=True, blank=True,
                                on_delete=models.CASCADE)
    total = models.DecimalField('total', blank=True, null=True, max_digits=1000, decimal_places=0 ,default=0)
    PROCESSING = 'Processing'  # Payment confirmed, processing order.
    SHIPPED = 'SHIPPED'  # Shipped to customer.
    COMPLETED = 'COMPLETED'  # Completed and received by customer.
    REFUNDED = 'REFUNDED'  # Fully refunded by seller.

    title = models.CharField('title', max_length=255, choices=[
        (PROCESSING, PROCESSING),
        (SHIPPED, SHIPPED),
        (COMPLETED, COMPLETED),
        (REFUNDED, REFUNDED),
    ],
                             default=PROCESSING,
                             )

    ref_code = models.CharField('ref code', max_length=255)
    ordered = models.BooleanField('ordered', default=True)
    items = models.ManyToManyField('commerce.Item', verbose_name='items', related_name='order')

    def __str__(self):
        return f'{self.uid} + {self.total}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        self.addres = get_object_or_404(Address, uid=self.uid)
        self.ref_cod = 'noneref'
        super().save(*args, **kwargs)




class Item(Entity):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey('commerce.Product', verbose_name='product',
                                on_delete=models.CASCADE)
    item_qty = models.IntegerField('item_qty')
    ordered = models.BooleanField('ordered')

    def __str__(self):
        return self.product.name


