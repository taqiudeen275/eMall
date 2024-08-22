from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q
from .models import Conversation, Message
from accounts.models import User
from business.models import Business
from django.core.paginator import Paginator



@login_required
def start_conversation(request, business_id):
    business_user = get_object_or_404(User, business__id=business_id)
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=business_user
    ).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, business_user)
    
    return redirect('chat:conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    conversations =  Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    messages = conversation.messages.order_by('timestamp')
    
    # Mark messages as read if the viewer is a business user
    if request.user.user_type == 'Business':
        unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
        unread_messages.update(is_read=True)
    

    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'conversations': conversations,
        'cmessages': messages,
    })

@require_POST
@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    content = request.POST.get('content')
    
    if content:
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        conversation.updated_at = message.timestamp
        conversation.save()
        
        return JsonResponse({
            'status': 'success',
            'message_id': message.id,
            'message_content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def get_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.order_by('timestamp')
    
    message_list = [{
        'id': message.id,
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': message.is_read
    } for message in messages]
    
    return JsonResponse({'messages': message_list})


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    
    return render(request, 'chat/conversation_list.html', {
        'conversations': conversations
    })




@login_required
def business_message_inbox(request):
    business_user = request.user
    conversations = Conversation.objects.filter(participants=business_user).order_by('-updated_at')
    
    paginator = Paginator(conversations, 10)  # Show 10 conversations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'chat/business_message_inbox.html', {
        'page_obj': page_obj,
    })
