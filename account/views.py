from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from .models import *
from django.db.models import Sum
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
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
            subject = "Verify Your Email"
            title = "Email Verification"
            message = "Thank you for registering with us! Please click the link below to verify your email and complete your registration."
            cta_text = "Verify Email"
            logo_url = f"{get_current_site(request).domain}/static/images/logo2.png"
            company_name = "Stapfund"
            website_url = 'https://192.168.43.88:8000'
            
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
                subject=subject,
                body=render_to_string('account/email-template.html', {
                    # 'user': user.full_name,
                    'subject': subject,
                    'title': title,
                    'message': message,
                    'protocol': 'https' if request.is_secure() else 'http',
                    'cta_url': f"{get_current_site(request).domain}/account/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}",
                    'cta_text': cta_text,
                    'logo_url': logo_url,
                    'company_name': company_name,
                    'website_url': website_url,
                }),
                to=[email],
            )
            verification_email.content_subtype = 'html'
            verification_email.send()
            
            return JsonResponse({"success": 'Account created successfully'})
        except Exception as e:
            print(e)
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
        # try:
        user = request.user
        email = user.email
        subject = "Verify Your Email"
        title = "Email Verification"
        message = "Thank you for registering with us! Please click the link below to verify your email and complete your registration."
        cta_url = f"{get_current_site(request).domain}/account/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}"
        cta_text = "Verify Email"
        logo_url = f"{get_current_site(request).domain}/static/images/logo2.png"
        company_name = "Stapfund"
        website_url = 'https://192.168.43.88:8000'
        
        verification_email = EmailMessage(
            subject=subject,
            body=render_to_string('account/email-template.html', {
                'user': user.full_name,
                'subject': subject,
                'title': title,
                'message': message,
                'protocol': 'https' if request.is_secure() else 'http',
                'cta_url': cta_url,
                'cta_text': cta_text,
                'logo_url': logo_url,
                'company_name': company_name,
                'website_url': website_url,
            }),
            to=[email],
        )
        verification_email.content_subtype = 'html'
        verification_email.send()
        return JsonResponse({'success': 'Verification email resent.'})
        # except Exception as e:
        #     print(e)
        #     return JsonResponse({'error': 'Error sending email'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


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
                subject = "Reset Your Password"
                title = "Password Reset Request"
                message = "We received a request to reset your password. Click the link below to reset your password."
                cta_url = f"{get_current_site(request).domain}/account/reset/{user_uid}/{user_token}"
                cta_text = "Reset Password"
                logo_url = f"{get_current_site(request).domain}/static/images/logo2.png"
                company_name = "Stapfund"
                website_url = 'https://192.168.43.88:8000'
                
                password_reset_email = EmailMessage(
                subject=subject,
                body=render_to_string('account/email-template.html', {
                    'subject': subject,
                    'title': title,
                    'message': message,
                    'protocol': 'https' if request.is_secure() else 'http',
                    'cta_url': cta_url,
                    'cta_text': cta_text,
                    'logo_url': logo_url,
                    'company_name': company_name,
                    'website_url': website_url,
                }),
                to=[email],
                )
                password_reset_email.content_subtype = 'html'
                password_reset_email.send()
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
        transactions = Transactions.objects.all()
        investments = Investments.objects.all()
        withdrawals = Withdrawal.objects.all()
        total_users = User.objects.filter(is_superuser=False)
        
        total_amount = Investments.objects.filter(Q(active=True) | Q(closed=True)).aggregate(Sum('amount'))['amount__sum']
        total_roi = Investments.objects.filter(Q(active=True) | Q(closed=True)).aggregate(Sum('roi'))['roi__sum']
        
        user_amount = Investments.objects.filter(Q(active=True) | Q(closed=True), user=request.user).aggregate(Sum('amount'))['amount__sum']
        user_roi = Investments.objects.filter(Q(active=True) | Q(closed=True), user=request.user).aggregate(Sum('roi'))['roi__sum']
        user_withdraw = Withdrawal.objects.filter(user=request.user, completed=True).aggregate(Sum('amount'))['amount__sum']

        total_amount = total_amount or 0
        total_roi = total_roi or 0
        user_amount = user_amount or 0
        user_roi = user_roi or 0
        user_withdraw = user_withdraw or 0

        context = {
            'users':users, 'payments':payments, 'packages':packages,
            'transactions':transactions, 'investments':investments,
            'withdrawals':withdrawals, 'total_amount':total_amount,
            'total_roi':total_roi, 'user_amount':user_amount,
            'user_roi':user_roi, 'total_users':total_users,
            'user_withdraw':user_withdraw
        }
        
        return render(request, 'account/dashboard.html', context)
    else:
        raise Http404("Page not found")

# Get dashboard data
def get_dashboard_data(request):
    users = User.objects.all().values('id', 'full_name', 'email')  # Replace with actual field names
    payments = Payments.objects.all().values('id', 'method', 'address')  # Replace with actual field names
    packages = Packages.objects.all().values('id', 'plan', 'profit')  # Replace with actual field names
    transactions = Transactions.objects.all().values('id', 'method', 'amount')  # Replace with actual field names
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

#Accept Transaction
def accept_transaction(request):
    if request.method == 'POST':
        transaction_id = int(request.POST.get('transaction_id'))
        transaction = Transactions.objects.get(id=transaction_id)
        transaction.pending = False
        transaction.confirmed = True
        transaction.rejected = False
        transaction.save()
        
        investment = Investments.objects.get(id=transaction_id)
        if transaction.confirmed:
            investment.active = True
            investment.pending = False
            investment.closed = False
        else: 
            investment.pending = True
            investment.active = False
            investment.closed = False

        investment.save()

        return JsonResponse({'success':"Transaction confirmed"})
    else:
        return JsonResponse({'error':"An error occured..."})

#Reject Transaction
def reject_transaction(request):
    if request.method == 'POST':
        if request.user.is_admin:
            transaction_id = int(request.POST.get('transaction_id'))
            transaction = Transactions.objects.get(id=transaction_id)
            transaction.pending = False
            transaction.confirmed = False
            transaction.rejected = True
            transaction.save()
            
            investment = Investments.objects.get(id=transaction_id)
            if transaction.rejected:
                investment.active = False
                investment.pending = False
                investment.closed = False
                investment.rejected = True
            else: 
                investment.pending = True
                investment.active = False
                investment.closed = False
                investment.rejected = False

            investment.save()

            return JsonResponse({'success':"Transaction rejected"})
        else:
            return JsonResponse({'error':"An error occured..."})

#Withdrawal
def withdraw(request):
    if request.method == 'POST':
        investment_id = request.POST.get('investment_id')
        method = request.POST.get('method')
        address = request.POST.get('address')
        
        if not method:
            return JsonResponse({'error': 'Select a wallet'})
        if not address:
            return JsonResponse({'error': 'Enter a valid address'})
        else:
            investment = Investments.objects.get(id=investment_id)
            investment.pending = False
            investment.active = False
            investment.closed = True
            investment.rejected = False
            investment.save()
            
            w_amount = float(investment.amount)
            w_roi = float(investment.roi)
            t_amount = w_amount + w_roi
            
            withdrawal = Withdrawal.objects.create(
                user=request.user, plan=investment.plan,
                amount=t_amount, method=method,
                address=address
            )
            withdrawal.save()
            
            return JsonResponse({'success': 'Withdrawal request successful'})
    return JsonResponse({'error': 'An error occurred'})

#Accept Transaction
def accept_withdrawal(request):
    if request.method == 'POST':
        withdrawal_id = int(request.POST.get('withdrawal_id'))
        withdrawal = Withdrawal.objects.get(id=withdrawal_id)
        withdrawal.processing = False
        withdrawal.completed = True
        withdrawal.rejected = False
        withdrawal.save()

        return JsonResponse({'success':"Withdrawal confirmed"})
    else:
        return JsonResponse({'error':"An error occured..."})

#Reject Transaction
def reject_withdrawal(request):
    if request.method == 'POST':
        withdrawal_id = int(request.POST.get('withdrawal_id'))
        withdrawal = Withdrawal.objects.get(id=withdrawal_id)
        withdrawal.processing = False
        withdrawal.completed = False
        withdrawal.rejected = True
        withdrawal.save()

        return JsonResponse({'success':"Withdrawal rejected"})
    else:
        return JsonResponse({'error':"An error occured..."})

#Get chart data
def get_chart_data(request):
    # Get labels for each month from January to December
    labels = [datetime(2025, month, 1).strftime('%b') for month in range(1, 13)]

    # Example: Count of users per month
    user_counts = []
    for month in range(1, 13):
        count = User.objects.filter(is_superuser=False, is_verified=True, date_joined__year=2025, date_joined__month=month).count()
        user_counts.append(count)

    # Example: Sum of investments per month
    investment_sums = []
    for month in range(1, 13):
        total = Investments.objects.filter(Q(active=True) | Q(closed=True), date__year=2025, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        investment_sums.append(total)

    # Example: Sum of ROI per month
    roi_sums = []
    for month in range(1, 13):
        total = Investments.objects.filter(Q(active=True) | Q(closed=True), date__year=2025, date__month=month).aggregate(total=Sum('roi'))['total'] or 0
        roi_sums.append(total)

    return JsonResponse({
        'labels': labels,
        'users': user_counts,
        'investments': investment_sums,
        'roi': roi_sums
    })


#Get user chart data
def get_user_chart_data(request):
    user = request.user
    labels = [datetime(2025, month, 1).strftime('%b') for month in range(1, 13)]

    # Example: Sum of investments per month for the user
    user_investment_sums = []
    for month in range(1, 13):
        total = Investments.objects.filter(user=user, date__year=2025, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        user_investment_sums.append(total)

    # Example: Sum of ROI per month for the user
    user_roi_sums = []
    for month in range(1, 13):
        total = Investments.objects.filter(user=user, date__year=2025, date__month=month).aggregate(total=Sum('roi'))['total'] or 0
        user_roi_sums.append(total)

    return JsonResponse({
        'labels': labels,
        'investments': user_investment_sums,
        'roi': user_roi_sums
    })

#update ROI
# @csrf_exempt  
def update_roi(request):
    if request.method == 'POST':
        investments = Investments.objects.filter(active=True)

        if not investments.exists():
            return JsonResponse({'error': 'No active investments found'}, status=404)

        for investment in investments:
            investment.update_roi()  # ✅ Call the update method

        return JsonResponse({'success': 'ROI updated successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

