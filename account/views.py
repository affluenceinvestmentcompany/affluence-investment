from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from .models import *
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import base64
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist

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
        try:
            full_name = request.POST['full_name']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            
            if User.objects.filter(email__iexact=email).exists():
                return JsonResponse({'error':"Email already exist, try login..."})
            
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
            
            return JsonResponse({"success": 'Account created successfully'})
        except Exception as e:
            return JsonResponse({'error': 'An error occurred...'})

# User Login
def login(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email = email, password = password)
            
            if user is not None:
                auth.login(request, user)
                return JsonResponse({'success':"Login successful"})
            else:
                return JsonResponse({'error':"Invalid email or password"})
        except Exception as e:
            return JsonResponse({'error': 'An error occurred...'})

# User Logout
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return JsonResponse({'success': 'Logout successful'})
    return JsonResponse({'error': 'An error occurred...'}, status=400)

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

#Forgotten password
def password_reset_request(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            if user:
                verification_email = EmailMessage(
                    subject = 'Password reset request',
                    body = render_to_string('account/password_reset_email.html', {
                        'user': user.full_name,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.id)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http'
                    }),
                    to = [email],
                )
                verification_email.send()
                return JsonResponse({"success": "Password reset email sent"})
            else:
                return JsonResponse({"error": "Email is not registered"})
        except Exception as e:
            err_msg = str(e)
            if err_msg == 'User matching query does not exist.':
                return JsonResponse({"error": "Email is not registered"})
            return JsonResponse({"error": "An error occurred"})
    else:
        return JsonResponse({"error": "Invalid request"})

#Reset password
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except Exception as e:
        print(e)
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            try:
                new_password1 = request.POST.get('new_password')
                if new_password1:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, 'Your reset successful')
                    return redirect('index')
                else:
                    messages.error(request, 'Please provide a valid password.')
            except Exception as e:
                print(e)
        
        return render(request, 'account/password_reset_confirm.html', {'uid': uid, 'token': token})
    else:
        raise Http404("Invalid password reset link")

# Dashboard
def dashboard(request):
    if request.user.is_authenticated and request.user.is_verified:
        return render(request, 'account/dashboard.html')
    else:
        raise Http404("Page not found")

#Add User
def add_user(request):
    if request.method == 'POST':
        try:
            full_name = request.POST['full_name']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            
            if User.objects.filter(email__iexact=email).exists():
                return JsonResponse({'error':"User already exist"})
            
            user = User.objects.create_user(full_name=full_name, email=email, 
                                            phone=phone, password=password,
                                            is_verified=True
                                            )
            
            user.save()
            
            return JsonResponse({"success": 'User added successfully'})
        except Exception as e:
            return JsonResponse({'error': 'An error occurred...'})

#Edit Profile
def edit_profile(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        user = request.user
        if full_name != '':
            user.full_name = full_name
        if phone != '':
            user.phone = phone
        user.save()
        return JsonResponse({'success': 'Profile update successful'})

#Change Password
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({"error": "Invalid old password"})
        if new_password1 != new_password2:
            return JsonResponse({"error": "New passwords do not match"})
        if old_password == new_password1:
            return JsonResponse({"error": "Same old password & new password"})
        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({"success": "Password change successful"})

# Get dashboard data
def get_dashboard_data(request):
    # Replace these with actual data fetching logic
    total_users = 1000  # Example total users
    total_investment = 50000  # Example total investment
    total_roi = 15  # Example total ROI percentage

    # Return the data as a JSON response
    return JsonResponse({
        'total_users': total_users,
        'total_investment': total_investment,
        'total_roi': total_roi
    })

