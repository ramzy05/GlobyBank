from django.urls import path
from .views import HomeView, welcome_view, recharge_withdraw_view, transfer_view, HistoryView

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('home', HomeView.as_view(), name='home'),
    path('history', HistoryView.as_view(), name='history'),
    path('transaction/<str:action>', recharge_withdraw_view, name='withdraw_recharge'),
    path('transaction', transfer_view, name='transfer'),
]
