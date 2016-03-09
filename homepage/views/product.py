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

# ########### Show list of records ###########
@view_function
def process_request(request):

    return HttpResponseRedirect('/')


# ########### Show list of records ###########
@view_function
def detail(request):
    params = {}

    try:
        product = hmod.Pizza.objects.get(id=request.urlparams[0])
    except hmod.Pizza.DoesNotExist:
        return HttpResponseRedirect('/')

    params['product'] = product
    return templater.render_to_response(request, 'product.detail.html', params)


# ########### Show list of records ###########
@view_function
def search(request):
    params = {}

    # TODO: also check description
    products = hmod.Pizza.objects.all().filter(name__icontains=request.urlparams[0])

    params['products'] = products
    return templater.render_to_response(request, 'product.html', params)
