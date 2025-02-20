from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('resend-link/', views.resend_link, name='resend_link'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('reset/<uid>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/add-payment/', views.add_payment, name='add_payment'),
    path('dashboard/add-user/', views.add_user, name='add_user'),
    path('dashboard/edit-profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/edit-package/', views.edit_package, name='edit_package'),
    path('dashboard/change-password/', views.change_password, name='change_password'),
    path('dashboard/withdraw/', views.withdraw, name='withdraw'),
    path('dashboard/users/delete-user/', views.delete_user, name='delete_user'),
    path('dashboard/payments/delete-payment/', views.delete_payment, name='delete_payment'),
    path('dashboard/transactions/accept-transaction/', views.accept_transaction, name='accept_transaction'),
    path('dashboard/transactions/reject-transaction/', views.reject_transaction, name='reject_transaction'),
    path('dashboard/withdrawals/accept-withdrawal/', views.accept_withdrawal, name='accept_withdrawal'),
    path('dashboard/withdrawals/reject-withdrawal/', views.reject_withdrawal, name='reject_withdrawal'),
    
    path('api/fuckof/@/fuckof/get-chart-data/', views.get_chart_data, name='get_chart_data'),
    path('api/fuckof/@/fuckof/get-user-chart-data/', views.get_user_chart_data, name='get_user_chart_data'),
    path('api/update-roi/', views.update_roi, name='update_roi'),
]

