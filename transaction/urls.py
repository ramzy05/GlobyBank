from django.urls import path
from .views import home_view, welcome_view, recharge_withdraw_view, transfer_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('home', home_view, name='home'),
    path('withdraw_recharge', recharge_withdraw_view, name='withdraw'),
    path('transfer', transfer_view, name='transfer'),
]
