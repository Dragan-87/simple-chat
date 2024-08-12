from django.shortcuts import render

# Create your views here.
def login__view(request):
    return render(request, "authService/login.html")