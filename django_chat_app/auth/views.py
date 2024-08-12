from django.shortcuts import render

# Create your views here.

def creat_new_user(request):
    pass

def login__view(request):
    return render(request, 'auth/index.html')