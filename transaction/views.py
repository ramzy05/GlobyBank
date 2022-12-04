from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def welcome_view(request):
    context = {}
    return render(request, 'auth/index.html', context)


@login_required(login_url='login')
def home_view(request):
    context = {'transactions': {}}
    return render(request, 'auth/home.html', context)
