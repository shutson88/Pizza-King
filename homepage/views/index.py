from django.conf import settings
from django_mako_plus.controller import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_response

@view_function
def process_request(request):
  template_vars = {
    'now': datetime.now(),
  }
  return dmp_render_to_response(request, 'index.html', template_vars)