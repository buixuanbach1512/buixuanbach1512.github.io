from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    cat_name = models.CharField(max_length=255, verbose_name=_('name'))
    cat_img = models.ImageField(null= True, verbose_name=_('image'))
    cat_status = models.BooleanField(default=False, verbose_name=_('status'))
    date = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.cat_name

class Product(models.Model):
    pro_name = models.CharField(max_length=255, verbose_name=_('name'))
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('category'))
    pro_img = models.ImageField(null=True, verbose_name=_('image'))
    pro_size = models.CharField(max_length=10, verbose_name=_('size'))
    pro_material = models.CharField(max_length=10, verbose_name=_('material'))
    pro_price = models.IntegerField(verbose_name=_('price'))
    pro_quantity = models.IntegerField(verbose_name=_('quantity'))
    pro_desc = models.TextField(verbose_name=_('description'))
    date = models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.pro_name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,related_name="customer", verbose_name=_('user'))
    name = models.CharField(max_length=255, null=True, verbose_name=_('name'))
    email = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self):
        return self.name
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('orderitem')
        verbose_name_plural = _('OrderItems')

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.pro_price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=False, verbose_name=_('address'))
    phone = models.BigIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('shippingaddress')
        verbose_name_plural = _('Shipping Address')
 
    def __str__(self):
        return str(self.address)
