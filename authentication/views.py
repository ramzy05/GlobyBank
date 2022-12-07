import json
from django.shortcuts import render, redirect
from .forms import CreateAccountForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account
from django.http.response import JsonResponse

# Create your views here.


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateAccountForm()
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'result': True, 'url': '/login'}, safe=False, status=201)
        else:
            return JsonResponse({'result': False, 'errors': json.loads(form.errors.as_json())}, safe=False, status=400)
    context = {
        'form': form,
    }
    return render(request, 'auth/signup.html', context)


def signin_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateAccountForm()

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        username = form['username'].value()
        password = form['password1'].value()
        if username == '':
            return JsonResponse({'result': False, 'errors': {'username': [{'message': 'Username cannot be blank'}]}}, status=400, safe=False)

        if password == '':
            return JsonResponse({'result': False, 'errors': {'password1': [{'message': 'Password field cannot be blank'}]}}, status=400, safe=False)

        if not Account.objects.filter(username=username).exists():
            return JsonResponse({'result': False, 'errors': {'username': [{'message': 'User not found, enter another username'}]}}, status=400, safe=False)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return JsonResponse({'result': True, 'url': '/home'}, status=200, safe=False)
        else:
            return JsonResponse({'result': False, 'errors': {'password1': [{'message': 'Invalid password'}]}}, status=400, safe=False)

    context = {
        'form': form,
    }
    return render(request, 'auth/signin.html', context)


@login_required(login_url='login')
def signout_view(request):
    logout(request)
    return redirect('welcome')
