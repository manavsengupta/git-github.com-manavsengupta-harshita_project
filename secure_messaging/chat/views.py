from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .utils import generate_hmac, verify_hmac

# --- NEW INDEX VIEW ---
def index(request):
    # If the user is already logged in, send them straight to their inbox
    if request.user.is_authenticated:
        return redirect('inbox')
    return render(request, 'chat/index.html')

@login_required
def send_message(request):
    # ... (Keep your existing send_message code here)
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')
        receiver = User.objects.get(id=receiver_id)
        signature = generate_hmac(content)
        Message.objects.create(sender=request.user, receiver=receiver, content=content, hmac_signature=signature)
        return redirect('inbox')
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/send_message.html', {'users': users})

@login_required
def inbox(request):
    # ... (Keep your existing inbox code here)
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    for msg in messages:
        msg.is_authentic = verify_hmac(msg.content, msg.hmac_signature)
    return render(request, 'chat/inbox.html', {'messages': messages})