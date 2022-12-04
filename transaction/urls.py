from django.urls import path
from .views import home_view, welcome_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('home', home_view, name='home'),
]
