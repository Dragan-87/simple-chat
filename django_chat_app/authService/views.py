from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


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
        if request.POST['username'] or request.POST['first_name'] or request.POST['last_name'] or request.POST['email'] or request.POST['password'] is None:
            return render(request, 'authService/register.html', {'registerFailed': "Bitte füllen sie alle Felder aus"} )
        newUsername = request.POST['username']
        newFirst_name = request.POST['first_name']
        newLast_name = request.POST['last_name']
        newEmail = request.POST['email']
        newPassword = make_password(request.POST['password'])
        confirm_password = request.POST['confirm_password']
        if newPassword is not confirm_password:
            return render(request, 'authService/register.html', {'registerFailed': "Passwort stimmt nicht überein"} )
        
        if User.objects.filter(username=newUsername).exists():
            return render(request, 'authService/register.html', {'registerFailed': "Der Nutzer Existiert bereits"} )

        user = User.objects.create(username=newUsername, first_name=newFirst_name, last_name=newLast_name, email=newEmail, password=newPassword)
        user.save()
        return render(request, 'authService/login.html')

    else:
        return render(request, 'authService/register.html')