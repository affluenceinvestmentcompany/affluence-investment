from django.shortcuts import render

# Create your views here.
def privacyPolicy(request):
    return render(request, 'privacyPolicy/privacy-policy.html')
