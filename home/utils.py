import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings


def generateOtp():
    otp = ''
    for i in range(6):
        otp += str(random.randint(1, 9))
    return otp


def send_onetimepassword(email):
    subject = 'One Time Password for authentication'
    otp_code = generateOtp()
    print(f"===============\n{otp_code}\n================")
    user = User.objects.get(email=email)
    # domaim = get_current_site(request).domain,
    message = f'Hi {user.full_name}, please use this code to authenticate your payment request {otp_code}'
    sender = settings.DEFAULT_FROM_EMAIL
    
    OneTimePassword.objects.create(user=user, code=otp_code)
    
    send_email = EmailMessage(subject=subject, body=message, from_email=sender, to=[email])
    send_email.send(fail_silently=True)


def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()