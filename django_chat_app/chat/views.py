from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def index(request):
    if request.method == "POST" and request.POST['textmessage'] != '' :
        print("received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)

    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messeges': chatMessages})
