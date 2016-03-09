from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django.contrib.auth import logout, hashers
from django.contrib.auth import authenticate, login
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django_mako_plus.controller.router import get_renderer
from django import forms
from django.contrib.auth.models import Group

templater = get_renderer('homepage')


# ########### Show list of records ###########
@view_function
def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/index')

    return HttpResponseRedirect('/homepage/account.edit/%s' % request.user.id)


# ######### Edit record ################
@view_function
def edit(request):
    params = {}

    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
        a = hmod.Address.objects.get(user=user)
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/index')

    if request.user.is_authenticated():
        if user.id is not request.user.id:
            return HttpResponseRedirect('/homepage/account.edit/%s' % request.user.id)
    else:
        return HttpResponseRedirect('/homepage/account.create')

    # TODO: get address to work
    # Pre-populate form
    form = EditForm(initial={
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'address1': a.address1,
        'address2': a.address2,
        'city': a.city,
        'state': a.state,
        'postal_code': a.postal_code,
        'phone': user.phone,
    })

    # clean form data, save to db
    if request.method == 'POST':
        form = EditForm(request.POST)
        form.user_id = user.id
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            user.save()


    params['form'] = form
    params['user'] = user
    params['addresses'] = a
    return templater.render_to_response(request, 'account.edit.html', params)


# ############ Create record ################
@view_function
def create(request):
    params = {}

    if request.user.is_authenticated():
        return HttpResponseRedirect('/homepage/account.edit/%s' % request.user.id)

    form = CreateForm()
    user = hmod.User()
    a = hmod.Address()

    # clean form data, save to db
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user.set_password(user.password)
            user.phone = form.cleaned_data['phone_number']
            user.save()

            a.user = user
            a.address1 = form.cleaned_data['address1']
            a.address2 = form.cleaned_data['address2']
            a.city = form.cleaned_data['city']
            a.state = form.cleaned_data['state']
            a.postal_code = form.cleaned_data['postal_code']
            a.save()

            # Add to user group
            g = Group.objects.get(name='User')
            user.groups.clear()
            user.groups.add(g)

            # Log the user in
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponseRedirect('/homepage/index')

    params['form'] = form
    params['user'] = user
    return templater.render_to_response(request, 'account.create.html', params)


# ############## Delete record #############
@view_function
def delete(request):

    if request.user.is_authenticated():
        try:
            user = hmod.User.objects.get(id=request.urlparams[0])
        except hmod.User.DoesNotExist:
            return HttpResponseRedirect('/homepage/account.create')

        if user.id is not request.user.id:
            return HttpResponseRedirect('/homepage/account.edit/%s' % request.user.id)
    else:
        return HttpResponseRedirect('/homepage/index')

    user.is_active = False
    user.save()

    return HttpResponseRedirect('/homepage/account.logout_user')


# ############# Logout User ######################
@view_function
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/homepage/index')


# ############# Change Password ######################
@view_function
def change_password(request):
    params = {}

    if request.user.is_authenticated():
        try:
            user = hmod.User.objects.get(id=request.urlparams[0])
        except hmod.User.DoesNotExist:
            return HttpResponseRedirect('/homepage/index')

        if user.id is not request.user.id:
            return HttpResponseRedirect('/homepage/account.edit/%s' % request.user.id)
    else:
        return HttpResponseRedirect('/homepage/index')

    form = ChangePasswordForm()

    # clean form data, save to db
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        form.user_id = user.id
        if form.is_valid():
            user.password = form.cleaned_data['new_password']
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/homepage/account.edit/%s' % request.user.id)

    # TODO: do we need the user param? what about in other functions here?
    params['form'] = form
    params['user'] = user
    return templater.render_to_response(request, 'account.change_password.html', params)


# TODO: how to combine CreateForm and EditForm???
# Create class w/ requirements and validation
class CreateForm(forms.Form):
    username = forms.CharField(required=True, min_length=1, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, min_length=1, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, min_length=1, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, min_length=5, max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    address1 = forms.CharField(required=True, min_length=5, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address2 = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(required=True, min_length=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(required=True, min_length=5, max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, min_length=3, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, min_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        user_name = self.cleaned_data['username']
        user_count = hmod.User.objects.filter(username=user_name).count()
        if user_count >= 1:
            raise forms.ValidationError('Username "%s" is already taken.' % user_name)
        return user_name


# Edit Form class w/ requirements and validation
class EditForm(forms.Form):
    username = forms.CharField(required=True, min_length=1, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, min_length=1, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, min_length=1, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, min_length=5, max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    address1 = forms.CharField(required=True, min_length=5, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address2 = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=True, min_length=3, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(required=True, min_length=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(required=True, min_length=5, max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, min_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        user_name = self.cleaned_data['username']
        user_count = hmod.User.objects.filter(username=user_name).exclude(id=self.user_id).count()
        if user_count >= 1:
            raise forms.ValidationError('Username "%s" is already taken.' % user_name)
        return user_name

# Change Password Form class w/ requirements and validation
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(required=True, min_length=3, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(required=True, min_length=3, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    retype_password = forms.CharField(required=True, min_length=3, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_current_password(self):
        db_user = hmod.User.objects.get(id=self.user_id)
        db_password = db_user.password
        curr_password = self.cleaned_data['current_password']
        if not hashers.check_password(curr_password, db_password):
            raise forms.ValidationError('This is not your current password')
        # TODO: what does this return do?
        return curr_password

    def clean_retype_password(self):
        new_password = self.cleaned_data['new_password']
        retype_password = self.cleaned_data['retype_password']
        if retype_password != new_password:
            raise forms.ValidationError('Passwords no not match!')
        return retype_password

