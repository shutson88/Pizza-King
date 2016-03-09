from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django_mako_plus.controller.router import get_renderer
from django import forms
import json
from django.contrib.auth.models import Group

templater = get_renderer('homepage')

########## Login User ################
@view_function
def process_request(request):
    params = {}

    return templater.render_to_response(request, 'login.html', params)


@view_function
def loginForm(request):
    params = {}

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Log in
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
        return HttpResponse('''
            <script>
                window.location.href = window.location.href;
            </script>
        ''')

    params['form'] = form
    return templater.render_to_response(request, 'login.loginForm.html', params)


# Form class w/ requirements and validation
class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError('User does not exist!')
        else:
            if user.is_active:
                return self.cleaned_data
            else:
                raise forms.ValidationError('This account has been disabled!')