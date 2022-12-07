from django.urls import path
from .views import registration_view, signin_view, signout_view

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', signin_view, name='login'),
    path('logout', signout_view, name='logout'),
]
