__author__ = 'Seth'
from Customer import Customer
import datetime

class Order(object):

    def __init__(self):
        self.id = 0
        self.customer = Customer()
        self.date = datetime.date(0, 0, 0)
        self.pizzas = []

    def __init__(self, id, customer, store_name, server, date, pizzas):
        self.id = id
        self.customer = customer
        self.store_name = store_name
        self.server = server
        self.date = date
        self.pizzas = pizzas
