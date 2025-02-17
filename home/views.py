from django.shortcuts import render, redirect
from .models import *
from django.http import Http404, JsonResponse
from account.models import User

# Create your views here.
def index(request):
    packages = Packages.objects.all()
    context = {'packages':packages}
    return render(request, 'home/index.html', context)

def invest(request, goto_url):
    if request.user.is_authenticated and request.user.is_verified:
        package = Packages.objects.get(goto_url=goto_url)
        payments = Payments.objects.all()
        context = {'package':package, 'payments':payments}
        return render(request, 'home/invest.html', context)
    else:
        raise Http404("Page not found")

def create_investment(request):
    if request.method == 'POST':
        user = request.user
        plan = request.POST.get('plan')
        method = request.POST.get('method')
        amount = request.POST.get('amount')
        
        method = Payments.objects.get(method=method)
        amount = amount.replace(",", "")
        
        def bonus(amount):
            plan_bonuses = {'Basic': 0.5, 'Standard': 1.0, 'Premium': 1.5, 'Ultimate': 2.0}
            return int(amount) * plan_bonuses.get(plan, 0) / 100
        
        transaction = Transactions.objects.create(user = user, method = method, amount = amount, bonus = bonus(amount))
        transaction.save()
        
        investment = Investments.objects.create(user = user, plan = plan, amount = amount, roi = 0)
        investment.save()
        return JsonResponse({'success':"Transaction successful"})



