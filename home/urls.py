from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('invest/<str:goto_url>/', views.invest, name='invest'),
    path('create-investment/', views.create_investment, name='create_investment'),
]

