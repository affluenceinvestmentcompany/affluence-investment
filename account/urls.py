from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('resend-link/', views.resendLink, name='resend_link'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('reset/<uid>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-user/', views.add_user, name='add_user'),
    path('dashboard/edit-profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/change-password/', views.change_password, name='change_password'),
    # path('api/get-dashboard-data/', get_dashboard_data, name='get_dashboard_data'),
    
    path('dashboard/users/delete-user/', views.delete_user, name='delete_user'),
    
]

