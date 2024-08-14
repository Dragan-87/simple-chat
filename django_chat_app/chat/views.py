from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
import json



@login_required(login_url='/login/')
def index(request):

    if request.method == "POST" and request.POST['textmessage'] is not None:
        try:
            myChat = Chat.objects.get(id=1)
            new_msg = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
            author_name = new_msg.author.username
            serializerd_obj = serializers.serialize('json', [new_msg])
            
            msg_data = json.loads(serializerd_obj)
            msg_data[0]['fields']['author'] = author_name
            msg_json = json.dumps(msg_data)
            return JsonResponse(msg_json[1:-1], safe=False)
        except :
            pass

    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})


