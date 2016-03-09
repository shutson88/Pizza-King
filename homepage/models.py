#
# FILE:     models.py
#
# AUTHOR:   Jonathan Hodnett
# DATE:     03/08/2016
# REVISION: 1.0
#
# DESCRIPTION:  This is a Django models file that corresponds to the Pizza King DCD
#

from django.db import models
# from polymorphic import PolymorphicModel
from django.contrib.auth.models import User
from django.utils import timezone


class Address(models.Model):
    # Mailing or physical address in USA
    address1 = models.TextField(max_length=200)
    address2 = models.TextField(max_length=200, null=True, blank=True)
    address3 = models.TextField(max_length=200)
    city = models.TextField(max_length=100)
    state = models.TextField(max_length=20)
    postal_code = models.TextField(max_length=30)
    used_coupon = models.BooleanField(default=False)
    is_billing = models.BooleanField(default=False)
    user = models.ForeignKey('User', null=True, blank=True)

    class Meta:
        ordering = ['state', 'city', 'postal_code', 'address1', 'address2']
        verbose_name_plural = 'addresses'

    def __str__(self):
        return '%s %s %s %s %s' % (self.address1, self.address2, self.city, self.state, self.postal_code)


class User(User):
    # A registered user the Fish Store. Can have User, Seller, or Admin roles.
    phone = models.TextField(max_length=22)
    used_coupon =models.BooleanField(default=False)
    store = models.ForeignKey("Store", null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class PastCustomer(models.Model):
    # A registered user the Fish Store. Can have User, Seller, or Admin roles.
    Last_NM = models.TextField(max_length=122)
    First_NM = models.TextField(max_length=122)
    Street_NR = models.TextField()
    Street_NM = models.TextField()
    City = models.TextField()
    State = models.TextField()


class Store(models.Model):
    # A registered user the Fish Store. Can Seller or Admin roles.
    store_address = models.TextField(max_length=255)


class Pizza(models.Model):
    # May be sold
    name = models.TextField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '%s %s %s' % (self.name, self.description, self.price)


class Topping(models.Model):
    # May be sold
    name = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '%s %s' % (self.name, self.price)


class PizzaTopping(models.Model):
    # May be sold
    topping = models.ForeignKey('Topping')
    pizza = models.ForeignKey('Pizza')


class Order(models.Model):
    # Permanent record of orders that have been placed
    order_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('User')
    store = models.ForeignKey('Store')

    class Meta:
        ordering = ['order_date', 'user']

    def __str__(self):
        return '%s %s' % (self.order_date, self.user)


class OrderLineItem(models.Model):
    # Permanent record for line items on order
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order = models.ForeignKey('Order')
    pizza = models.ForeignKey('Pizza')


class SiteData(models.Model):
    site_policy = models.TextField()
    privacy_policy = models.TextField()

    def get_seller_policy(self):
        return self.site_policy