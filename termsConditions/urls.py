from django.urls import path
from . import views

urlpatterns = [
    path('', views.termsConditions, name='terms_conditions')
]

