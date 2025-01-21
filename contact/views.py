from django.shortcuts import render
from .models import ContactUs

# Create your views here.
def contact_us(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        message = request.POST['message']
    
    new_message = ContactUs.objects.create(
        full_name=full_name, email=email, message=message
    )
    
    new_message.save()
