from django.shortcuts import render

# Create your views here.
def termsConditions(request):
    return render(request, 'termsConditions/terms-conditions.html')


