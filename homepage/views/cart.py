from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django_mako_plus.controller.router import get_renderer
from django import forms

templater = get_renderer('homepage')

# TODO: set username as email
# TODO: use more try/catch
# TODO: add subtotal
# TODO: update qty
# TODO: control qty updates by product type
# TODO: add color

# ########### Show list of records ###########
@view_function
def process_request(request):
    params = {}

    # get the items in the shopping cart in an ajax ($.loadmodal) dialog
    cart = request.session['cart']

    products = []
    for key in cart:
        try:
            product = hmod.Pizza.objects.get(id=key)
        except hmod.Pizza.DoesNotExist:
            return HttpResponseRedirect('/')
        products.append(product)

    params['products'] = products
    params['cart'] = cart
    return templater.render_to_response(request, 'cart.html', params)


@view_function
def add(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    pid = request.urlparams[0]
    qty = request.urlparams[1]


    if pid in request.session['cart']:
        qty = int(qty)
        s_qty = request.session['cart'][pid]
        s_qty = int(s_qty)
        qty = (qty + s_qty)
        qty = str(qty)
        request.session['cart'][pid] = qty
    else:
        request.session['cart'][pid] = qty

    request.session.modified = True

    return HttpResponseRedirect('/homepage/cart')


@view_function
def delete(request):

    if 'cart' not in request.session:
        request.session['cart'] = {}
    pid = request.urlparams[0]

    if pid in request.session['cart']:
        del request.session['cart'][pid]

    request.session.modified = True

    return HttpResponse('works')


@view_function
def update(request):

    if 'cart' not in request.session:
        request.session['cart'] = {}
    pid = request.urlparams[0]
    pqty = request.urlparams[1]

    if pid in request.session['cart']:
        request.session['cart'][pid] = pqty

    request.session.modified = True

    return HttpResponse('works')