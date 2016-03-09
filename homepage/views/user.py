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
@permission_required('homepage.change_user', login_url=settings.LOGIN_REDIRECT_URL)
def process_request(request):
    params = {}
    users = hmod.User.objects.all().order_by('first_name', 'last_name')
    address = hmod.Address.objects.filter(user_id__gt=0)
    params['users'] = users
    params['address'] = address

    error_message = False
    if request.urlparams[0] == 'username_error':
        error_message = True
    params['error_message'] = error_message
    return templater.render_to_response(request, 'user.html', params)

