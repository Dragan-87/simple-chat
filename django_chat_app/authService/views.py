from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def login__view(request):
    if request.method == 'POST' and request.POST['username'] and request.POST['password']:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/chat/')
        else:
            print("login failed")
            return render(request, 'login.html', {'loginFail': True})
    else:
        return render(request, "authService/login.html")