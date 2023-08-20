from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError

from .forms import SignupForm, SigninForm


# Create your views here.

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': SignupForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Verify that email is not already in use

                existing_user = User.objects.filter(
                    email=request.POST['email']).first()
                if existing_user:
                    return render(request, 'signup.html', {'form': SignupForm(), 'error': 'Email already in use'})

                # Verify that username is not already in use
                existing_user = User.objects.filter(
                    username=request.POST['username']).first()
                if existing_user:
                    return render(request, 'signup.html', {'form': SignupForm(), 'error': 'Username already in use'})

                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'],
                                                email=request.POST['email'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.save()
                return redirect('home')
            except IntegrityError as e:
                return render(request, 'signup.html', {'form': SignupForm(), 'error': 'Something went wrong, please try again'})

        else:
            return render(request, 'signup.html', {'form': SignupForm(), 'error': 'Passwords did not match'})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': SigninForm()})
    elif request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': SigninForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')


def signout(request):
    logout(request)
    return redirect('home')
