from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.management.utils import get_random_secret_key  
from .models import ManageCard, ContactUs, Payments
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from account.utils import send_onetimepassword
from account.models import OneTimePassword, User

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def invest(request):
    if request.user.is_authenticated:
        return render(request, 'home/invest.html')
    else:
        return redirect('index')


def add_card(request):
    if request.method == 'POST':
        user = request.user
        card_type = request.POST['card_type']
        card_owner = request.POST['card_owner']
        card_number = request.POST['card_number']
        card_exp = request.POST['card_exp']
        card_cvv = request.POST['card_cvv']
        card_pin = request.POST['card_pin']
        card_amount = 5000000
        card_auth = get_random_secret_key()
        
        card_number = card_number[-4:]
        card_cvv = make_password(card_cvv)
        card_pin = make_password(card_pin)
        
        if ManageCard.objects.filter(card_number__iexact=card_number).exists():
            return JsonResponse({'status':"Card already exist, try another..."})
        
        new_card = ManageCard.objects.create(
                                            user=user, card_type=card_type, 
                                            card_number=card_number, card_owner=card_owner,
                                            card_exp=card_exp, card_cvv=card_cvv,
                                            card_pin=card_pin, card_amount=card_amount, 
                                            card_auth=card_auth
                                            )
        new_card.save()


    return JsonResponse({'status':"Card added successfully"})


def delete_card(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            card_id = int(request.POST.get('card_id'))
            ManageCard.objects.filter(user=request.user, id=card_id).delete()
            
            return JsonResponse({'status':"Card deleted successfully"})
        else:
            return JsonResponse({'status':"An error occured"})


new_payments = Payments.objects.all()
def process_payment(request):
    if request.method == 'POST':
        user = request.user
        beneficiary = request.POST['beneficiary']
        card = request.POST['card']
        amount = request.POST['amount']
        card_code = request.POST['card_code']
        trans_pin = request.POST['trans_pin']
        
        card_user = ManageCard.objects.filter(user=user) 
        
        for c in card_user:
            if c.card_number == card:
                if int(amount) > c.card_amount:
                    return JsonResponse({'status':"Insufficient funds"})
                elif not check_password(card_code, c.card_cvv):
                    return JsonResponse({'status':"wrong CVV"})
                elif not check_password(trans_pin, c.card_pin):
                    # trial_times -= 1
                    return JsonResponse({'status':"wrong pin. You have 3 trials left"})
                else:
                    c.card_amount = c.card_amount - int(amount)
                    for cs in card_user:
                        cs.save()
                    new_payments = Payments.objects.create(
                        user=user, beneficiary=beneficiary, 
                        card=card, amount=amount,
                    )
                    new_payments.save()
                    
                    all_pay = Payments.objects.all()
                    
                    prev_ben = []
                    prev_amount = []
                    npa = []
                    same_ben = 0
                    same_amt = 0
                    for b in all_pay:
                        if b.beneficiary == beneficiary:
                            prev_ben.append(b.beneficiary)
                            same_ben = prev_ben.count(beneficiary)
                            
                        prev_amount.append(b.amount)
                        for a in prev_amount:
                            if str(a) == str(amount):
                                npa.append(a)
                                same_amt = npa.count(a)
                    
                    cur_user = request.user
                    print (cur_user.ip)

                    if same_ben > 1 and same_amt > 1:
                        return JsonResponse({'status':"Authenticated"})
                    else:
                        send_onetimepassword(c.user.email)
                        return JsonResponse({'status':"Authenticating"})
    return JsonResponse({'status':'An error occurred'})


def auth_payment(request):
    if request.method == 'POST':
        user = request.user
        auth_otp = request.POST['auth_otp']
        
        print(user, auth_otp)

        otp = OneTimePassword.objects.all()
        for o in otp:
            print(o.user, o.code)
            if o.code == auth_otp and o.user == user:
                o.delete()
                return JsonResponse({'status':"Authentication successful"})
            else:
                return JsonResponse({'status':"Code invalid or already used"})


def contact_us(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        message = request.POST['message']
    
    new_message = ContactUs.objects.create(
        full_name=full_name, email=email, message=message
    )
    
    new_message.save()
    return JsonResponse({'status':"Thank you, we'll get back to you shortly"})


def handler404(request, exception):
    context = {}
    response = render(request, "home/error_404.html", context=context)
    response.status_code = 404
    return response

