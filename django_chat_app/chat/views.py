from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers



@login_required(login_url='/login/')
def index(request):
    if request.method == "POST" and request.POST['textmessage'] != '':
        myChat = Chat.objects.get(id=1)
        new_msg = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serializerd_obj = serializers.serialize('json', [new_msg])
        return JsonResponse(serializerd_obj[1:-1], safe=False)


    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

