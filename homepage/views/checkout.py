from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django_mako_plus.controller.router import get_renderer
from django import forms
from django.core import serializers
from datetime import datetime
from django.utils import formats
# import requests
# from django.core.mail import send_mail

templater = get_renderer('homepage')

# TODO: set username as email

# ########### Show list of records ###########
@view_function
def process_request(request):
    params = {}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/index/login')

    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart = request.session['cart']

    products = []
    for key in cart:
        try:
            product = hmod.Pizza.objects.get(id=key)
        except hmod.Pizza.DoesNotExist:
            return HttpResponseRedirect('/')
        products.append(product)

    card_form = CardForm()

    params['card_form'] = card_form
    params['products'] = products
    params['cart'] = cart
    return templater.render_to_response(request, 'checkout.html', params)


@view_function
def thanks(request):
    params = {}
    order = hmod.Order()

    products = []
    if request.method == 'POST':
        card_form = CardForm(request.POST)
        if 'cart' in request.session:
            if card_form.is_valid():
                cart = request.session['cart']
                order.user = request.user
                # order.seller = product.seller
                order.save()

                for key in cart:
                    product = hmod.Pizza.objects.get(id=key)
                    order_item = hmod.OrderLineItem()
                    order_item.quantity = cart[key]
                    order_item.price = product.current_price
                    order_item.order = order
                    order_item.product = product
                    order_item.save()
                    products.append(product)

        params['order'] = order
        params['post_data'] = request.POST
        params['products'] = products

        # email_body = templater.render(request, '/checkout_email.html', params)

        # send_mail('Purchase Receipt', email_body, 'jonathan@colonialheritagefoundation.us',
        #           [order.user.email], html_message=email_body, fail_silently=True)

    del request.session['cart']

    return templater.render_to_response(request, 'checkout.thanks.html', params)


@view_function
def delete(request):

    if 'cart' not in request.session:
        request.session['cart'] = {}
    pid = request.urlparams[0]

    if pid in request.session['cart']:
        del request.session['cart'][pid]

    request.session.modified = True

    return HttpResponseRedirect('/homepage/checkout')


@view_function
def update(request):

    if 'cart' not in request.session:
        request.session['cart'] = {}
    pid = request.urlparams[0]
    pqty = request.urlparams[1]

    if pid in request.session['cart']:
        request.session['cart'][pid] = pqty

    request.session.modified = True

    return HttpResponseRedirect('/homepage/checkout')


class CardForm(forms.Form):
    name = forms.CharField(required=True, min_length=2, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    exp_month = forms.IntegerField(required=True, min_value=1, max_value=12, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    exp_year = forms.IntegerField(required=True, min_value=0, max_value=99, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cvc = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(required=True, min_value=0, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'disabled': True}))
