from django.shortcuts import render
from .models import Message, Chat
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required(login_url='/login/')
def index(request):
    if request.method == "POST" and request.POST['textmessage'] != '':
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        latest_msg = Message.objects.latest('id')
    
        response_data = {
            'success': True,
            'message': 'Nachricht erfolgreich gesendet.',
            'messageText': latest_msg.text,
            'messageAuthor': latest_msg.author,
            'messageCreate': latest_msg.created_at,
        }
        return JsonResponse(response_data)


    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

