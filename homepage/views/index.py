from django_mako_plus.controller import view_function
from django_mako_plus.controller.router import get_renderer
from homepage import models as hmod


templater = get_renderer('homepage')

@view_function
def process_request(request):
    params = {}

    error_message = False
    if request.urlparams[0] == 'login':
        error_message = True
    params['error_message'] = error_message

    products = hmod.Pizza.objects.all()

    params['products'] = products
    return templater.render_to_response(request, 'index.html', params)