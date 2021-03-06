from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'User was created successfully')
                    return redirect('accounts:login')
                else:
                    messages.error(request, 'Email already exists')
                    return redirect('accounts:register')
            else:
                messages.error(request, 'Username already exists')
            return redirect('accounts:register')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            # can be used with: {% if user.is_authenticated %}
            messages.success(request, f'{username}, welcome to TAGV!')
            return redirect('layout:index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


@login_required(login_url='accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('layout:index')
