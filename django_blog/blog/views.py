from django.shortcuts import render, redirect  # for rendering templates & redirects
from django.contrib import messages  # for flash messages
from django.contrib.auth.forms import AuthenticationForm  # built-in login form
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect

# import your custom forms
from .forms import UserRegisterForm, UserUpdateForm


@csrf_protect
def index(request):
    if request.user.is_authenticated:
        u_form = UserUpdateForm(instance=request.user)
        if request.method == 'POST' and 'username' in request.POST and 'email' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Your profile has been updated!')
        return render(request, 'blog/index.html', {'u_form': u_form})

    login_form = AuthenticationForm()
    register_form = UserRegisterForm()

    if request.method == 'POST':
        if 'password1' in request.POST:  # registration
            register_form = UserRegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Registration successful! Please log in.')
        elif 'password' in request.POST:  # login
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('index')

    return render(request, 'index.html', {
        'login_form': login_form,
        'register_form': register_form
    })
