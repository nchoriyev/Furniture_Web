from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
import requests
from django.contrib import messages


class AuthPage(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            url = 'http://127.0.0.3:8003/identify/register'
            data = {
                'first_name': first_name,
                'last_name': last_name,
                "username": username,
                "email": email,
                "password": password
            }
            response = requests.post(url, json=data)

            if response.status_code == 200 and response.json().get('detail') == 'User already exist':
                error_message = "User already exists"
                return render(request, 'auth/register.html', {'form': form, 'error_message': error_message})

            elif response.status_code == 200:
                return redirect('login')

            else:
                error_message = response.json().get('detail', 'An unknown error occurred.')
                return render(request, 'auth/register.html', {'form': form, 'error_message': error_message})
        else:
            return render(request, 'auth/register.html', {'form': form})


class LoginPageView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'auth/login.html', {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            url = "http://127.0.0.3:8003/identify/login"
            data = {
                "username": form.cleaned_data['username'],
                "password": form.cleaned_data['password']
            }
            response = requests.post(url, json=data)

            if response.status_code  == 400 and response.json().get('detail') == 'Incorrect password or username':
                error_message = "Username or Password is incorrect"
                return render(request, 'auth/register.html', {'form': form, 'error_message': error_message})

            if response.status_code == 200:
                access_token = response.json()['access_token']

                response = redirect('home')
                response.set_cookie('access_token', access_token, httponly=True)
                return response
            else:
                messages.error(request, "Invalid login credentials")

        return render(request, 'auth/login.html')
