from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage-card', views.manage_card, name='manage_card'),
    path('add-card/', views.add_card, name='add_card'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('auth-payment/', views.auth_payment, name='auth_payment'),
    path('delete-card/', views.delete_card, name='delete_card'),
    path('contact-us/', views.contact_us, name='contact_us'),
]

