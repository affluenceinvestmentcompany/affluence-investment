from django.urls import path
from . import views

urlpatterns = [
    path('', views.privacyPolicy, name='privacy_policy')
]

