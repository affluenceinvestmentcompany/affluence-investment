from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
import json
from urllib.request import urlopen
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token


def activate(request, uidb64, token):
    # user = User()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()

        messages.success(request, 'Thank you! Your email is verified.')
        return redirect('index')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('index')

# Create your views here.
def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        
        if User.objects.filter(email__iexact=email).exists():
            return JsonResponse({'status':"Email already exist, try another..."})
        
        user = User.objects.create_user(full_name=full_name, email=email, 
                                        phone=phone, password=password,
                                        is_verified=False
                                        )
        
        user.save()
        
        user = authenticate(email=email, password=password)

        auth.login(request, user)
        
        verification_email = EmailMessage(
            subject = 'Verify your email',
            body = render_to_string('account/verify-email.html', {
                'user': user.full_name,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            }),
            to = [email],
        )
        verification_email.send()
        
        return JsonResponse({"data": email})

# User Login
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email = email, password = password)
        
        if user is not None:
            auth.login(request, user)
            return JsonResponse({'status':"Login suceessfull"})
        else:
            return JsonResponse({'status':"Invalid email or password"})

# User Logout
def logout(request):
    auth.logout(request)
    return redirect('index')

# Resend verification link
def resendLink(request):
    user = request.user
    email = request.user.email
    verification_email = EmailMessage(
        subject = 'Verify your email',
        body = render_to_string('account/verify-email.html', {
            'user': user.full_name,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }),
        to = [email],
    )
    verification_email.send()
    messages.success(request, 'Verification email resent.')
    return redirect('index')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated and request.user.is_verified:
        return render(request, 'account/dashboard.html')
    else:
        raise Http404("Page not found")

