from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('invest', views.invest, name='invest'),
    path('invest/basic-plan', views.invest, name='invest_basic'),
    path('invest/standard-plan', views.invest, name='invest_standard'),
    path('invest/premium-plan', views.invest, name='invest_premium'),
    path('invest/ultimate-plan', views.invest, name='invest_ultimate'),
]

