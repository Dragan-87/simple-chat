from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth.models import User
import json




def login__view(request):
    """
    View function for handling user login.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object.
    Raises:
        None
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return JsonResponse({'fields': {'username': 'Login erfolgreich: ' + username }})
        else:
            return JsonResponse({'fields': {'wrong_password': 'Benutzername oder Passwort falsch'}})
    
    return render(request, "authService/login.html")

def set_user_data(request):
    newUsername = request.POST['username']
    newFirst_name = request.POST['first_name']
    newLast_name = request.POST['last_name']
    newEmail = request.POST['email']
    newPassword = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    user_data = {
        'username': newUsername,
        'first_name': newFirst_name,
        'last_name': newLast_name,
        'email': newEmail,
        'password': newPassword,
        'confirm_password': confirm_password
    }
    
    return user_data


def register(request):
    """
    Register a new user.
    Args:
        request: The HTTP request object.
    Returns:
        If the request method is POST and all required fields are provided, returns a JSON response with a success message.
        If the request method is POST and any required field is missing, returns a JSON response with an error message indicating the missing fields.
        If the request method is POST and the passwords do not match, returns a JSON response with an error message.
        If the request method is POST and the username already exists, returns a JSON response with an error message.
        If the request method is GET, renders the 'register.html' template.
    """
    if request.method == 'POST':
        if not request.POST['username'] or not request.POST['first_name'] or not request.POST['last_name'] or not request.POST['email'] or not request.POST['password']:
            return JsonResponse({'fields': {'fields_empty': 'Bitte füllen Sie alle Felder aus'}})
        
        user_data = set_user_data(request)

        if user_data['password'] != user_data['confirm_password']:
            return JsonResponse({'fields': {'wrong_password': 'Passwörter stimmen nicht überein'}})
        
        if User.objects.filter(username=user_data['username']).exists():
            return JsonResponse({'fields': {'user_exists': 'Benutzername existiert bereits'}})

        newPassword = make_password(user_data['password'])
        user = User.objects.create(username=user_data['username'], first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'], password=newPassword)
        user.save()
        return JsonResponse({'fields': {'username': 'Registrierung erfolgreich: ' + user_data['username']}})
    
    return render(request, 'authService/register.html')


def logout_view(request):
    """
    Logs out the user and returns a JSON response indicating successful logout.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A JSON response with the following structure:
        {
            'fields': {
                'logout': True
            }
        }
    """
    if request.method == 'POST':
        token = request.POST.get('csrfmiddlewaretoken')
        logout(request)
        return JsonResponse({'fields': {'logout': True}})