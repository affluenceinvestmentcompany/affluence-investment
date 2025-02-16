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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from home.models import *
import random
import string
import secrets

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
def resend_link(request):
    if request.method == 'POST':
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
        return JsonResponse({'success': 'Verification email resent.'})

def generate_secret(length=64):
    secret = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return secret

def generate_token(length=64):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token

#Forgotten password
def password_reset_request(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            if user:
                
                user_uid = generate_secret()
                user_token = generate_token()
                reset_password = ResetPassword.objects.create(user=user, uid=user_uid, token=user_token)
                reset_password.save()
                
                verification_email = EmailMessage(
                    subject = 'Password reset request',
                    body = render_to_string('account/password_reset_email.html', {
                        'user': user.full_name,
                        'domain': get_current_site(request).domain,
                        'uid': user_uid,
                        'token': user_token,
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
def password_reset_confirm(request, uid, token):
    try:
        reset_password_instance = ResetPassword.objects.get(uid=uid, token=token)
        usr = reset_password_instance.user
    except ResetPassword.DoesNotExist:
        raise Http404("Page not found")

    if usr is not None:
        if request.method == 'POST':
            new_password1 = request.POST.get('password')
            if new_password1:
                usr.set_password(new_password1)
                usr.save()
                ResetPassword.objects.filter(user=usr).delete()
                return JsonResponse({'success': "Password reset successful"})
            else:
                return JsonResponse({'error': "Password field is empty"}, status=400)
        return render(request, 'account/password_reset_confirm.html', {'uid': uid, 'token': token})
    else:
        raise Http404("Page not found")

# Dashboard
def dashboard(request):
    if request.user.is_authenticated and request.user.is_verified: 
        users = User.objects.all()
        payments = Payments.objects.all()
        packages = Packages.objects.all()
        transactions = Transaction.objects.all()
        investments = Investments.objects.all()
        withdrawals = Withdrawal.objects.all()
        
        context = {
            'users':users, 'payments':payments, 'packages':packages,
            'transactions':transactions, 'investments':investments,
            'withdrawals':withdrawals, 
        }
        
        return render(request, 'account/dashboard.html', context)
    else:
        raise Http404("Page not found")

# Get dashboard data
def get_dashboard_data(request):
    users = User.objects.all().values('id', 'full_name', 'email')  # Replace with actual field names
    payments = Payments.objects.all().values('id', 'method', 'address')  # Replace with actual field names
    packages = Packages.objects.all().values('id', 'plan', 'profit')  # Replace with actual field names
    transactions = Transaction.objects.all().values('id', 'method', 'amount')  # Replace with actual field names
    investments = Investments.objects.all().values('id', 'plan', 'amount')  # Replace with actual field names
    withdrawals = Withdrawal.objects.all().values('id', 'user', 'balance')  # Replace with actual field names

    data = {
        'users': list(users),
        # 'payments': list(payments),
        # 'packages': list(packages),
        # 'transactions': list(transactions),
        # 'investments': list(investments),
        # 'withdrawals': list(withdrawals),
    }

    return JsonResponse(data)

#Add Payment
def add_payment(request):
    if request.method == 'POST':
        try:
            method = request.POST['method']
            address = request.POST['address']
            payment = Payments.objects.create(
                method=method, address=address, 
            )
            payment.save()
            return JsonResponse({"success": 'Payment added successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred...'})

#Add User
def add_user(request):
    if request.method == 'POST':
        try:
            full_name = request.POST['full_name']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            is_admin = request.POST['makeUserAdmin']
            
            print(is_admin)
            print(is_admin)
            print(is_admin)
            print(is_admin)
            
            if User.objects.filter(email__iexact=email).exists():
                return JsonResponse({'error':"User already exist"})
            
            user = User.objects.create_user(
                full_name=full_name, email=email, 
                phone=phone, password=password,
                is_verified=True
            )
            user.save()
            
            if is_admin == 'true':
                user.is_admin = True
            user.save()
            
            return JsonResponse({"success": 'User added successfully'})
        except Exception as e:
            print(e)
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

#Delete User
def delete_user(request):
    if request.method == 'POST':
        if request.user.is_admin:
            user_id = int(request.POST.get('user_id'))
            User.objects.filter(id=user_id).delete()
            
            return JsonResponse({'success':"User deleted successfully"})
        else:
            return JsonResponse({'error':"An error occured..."})

#Delete Payment
def delete_payment(request):
    if request.method == 'POST':
        if request.user.is_admin:
            payment_id = int(request.POST.get('payment_id'))
            Payments.objects.filter(id=payment_id).delete()
            
            return JsonResponse({'success':"Payment deleted successfully"})
        else:
            return JsonResponse({'error':"An error occured..."})

#Edit Package
def edit_package(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        plan = request.POST.get('plan')
        profit = request.POST.get('profit')
        bonus = request.POST.get('bonus')
        min_amount = request.POST.get('min_amount')
        min_days = request.POST.get('min_days')
        
        package = Packages.objects.get(id=package_id)
        package.plan = plan
        package.profit = profit
        package.bonus = bonus
        package.min_amount = min_amount
        package.min_days = min_days
        package.save()
        return JsonResponse({'success': 'Package update successful'})






