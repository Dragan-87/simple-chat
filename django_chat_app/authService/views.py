from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import logout
import json


# Create your views here.
def login__view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializerd_obj = serializers.serialize('json', [user])
            return JsonResponse(serializerd_obj[1:-1], safe=False)

        else:
            print("login failed")
            return render(request, 'authService/login.html', {'loginFail': True})
    else:
        return render(request, "authService/login.html")


def register(request):
    if request.method == 'POST':
        if not request.POST['username'] or not request.POST['first_name'] or not request.POST['last_name'] or not request.POST['email'] or not request.POST['password']:
            return JsonResponse({'fields': {'fields_empty': 'Bitte füllen Sie alle Felder aus'}})
        
        newUsername = request.POST['username']
        newFirst_name = request.POST['first_name']
        newLast_name = request.POST['last_name']
        newEmail = request.POST['email']
        newPassword = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if newPassword != confirm_password:
            return JsonResponse({'fields': {'wrong_password': 'Passwörter stimmen nicht überein'}})
        
        if User.objects.filter(username=newUsername).exists():
            return JsonResponse({'fields': {'user_exists': 'Benutzername existiert bereits'}})

        newPassword = make_password(newPassword)
        user = User.objects.create(username=newUsername, first_name=newFirst_name, last_name=newLast_name, email=newEmail, password=newPassword)
        user.save()
        return JsonResponse({'user': {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}})
    
    return render(request, 'authService/register.html')
