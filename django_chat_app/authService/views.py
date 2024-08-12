from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.
def login__view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/chat/')
        else:
            print("login failed")
            return render(request, 'authService/login.html', {'loginFail': True})
    else:
        return render(request, "authService/login.html")

def register(request):
    if request.method == 'POST':
        NewUsername = request.POST['username']
        NewFirst_name = request.POST['first_name']
        NewLast_name = request.POST['last_name']
        NewEmail = request.POST['email']
        NewPassword = request.POST['password']
        if User.objects.filter(username=NewUsername).exists():
            return render(request, 'authService/register.html', {'registerFailed': "Der Nutzer Existiert bereits"} )

        user = User.objects.create(username=NewUsername, first_name=NewFirst_name, last_name=NewLast_name, email=NewEmail, password=NewPassword)
        user.save()
        return render(request, 'authService/login.html')

    else:
        return render(request, 'authService/register.html', {'registerFailed': True})