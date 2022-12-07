from authentication.models import Account
from .models import Transaction, SelfTransaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import decimal


def welcome_view(request):
    context = {}
    return render(request, 'auth/index.html', context)


@login_required(login_url='login')
def home_view(request):
    context = {'transactions': {}}
    return render(request, 'auth/home.html', context)


@login_required(login_url='login')
def transfer_view(request):
    user = request.user
    context = {'user': user}

    if request.method == 'POST':
        user_pin_code = request.POST['code_pin']
        withdrawed_amount = decimal.Decimal(request.POST['amount'])
        received_amount = withdrawed_amount

        if user_pin_code != user.code_pin:
            return JsonResponse({'result': False, 'errors': {'code_pin': [{'message': 'Your pin code is incorrect'}]}}, safe=False, status=400)
        receiver = Account.objects.get(
            username=request.POST['receiver']) or None

        if receiver is None:
            return JsonResponse({'result': False, 'errors': {'receiver': [{'message': 'Unkwown receiver'}]}}, safe=False, status=400)
        # Everything is good we can make the transaction between the too user
        user.balance -= withdrawed_amount
        receiver.balance += received_amount
        user.save(update_fields=['balance'])
        receiver.save(update_fields=['balance'])
        new_transaction = Transaction.objects.create(
            sender=user, receiver=receiver, amount_sent=withdrawed_amount, amount_received=received_amount)
        if new_transaction:
            return JsonResponse({'result': True, 'url': '/home'}, safe=False, status=201)

        return JsonResponse({'result': False, 'errors': 'server internal error'}, safe=False, status=500)

    return render(request, 'auth/transaction.html',  context)


@login_required(login_url='login')
def recharge_withdraw_view(request, action):
    user = request.user
    min_amount = 50
    max_amount = 10000
    context = {
        'user': user,
        'currency': 'XAF',
        'max_amount': max_amount,
        'min_amount': min_amount
    }

    if request.method == 'POST':
        user_pin_code = request.POST['pin_code']
        amount = decimal.Decimal(request.POST['amount'])
        action = request.POST['action'] or None

        if user_pin_code != user.code_pin:
            return JsonResponse({'result': False, 'errors': {'code_pin': [{'message': 'Your pin code is incorrect'}]}}, safe=False, status=400)
        is_withrawed = False
        message = ''
        if action == 'withdraw':
            user.balance -= amount
            message = 'Your withdrawal end successfully'
            if user.balance <= 0:
                user.balance = 0.00

        elif action == 'recharge':
            is_withrawed = True
            user.balance += amount
            message = 'Your account has been credited successfully'

        user.save(update_fields=['balance'])
        new_transaction = SelfTransaction.objects.create(
            orderer=user, amount=amount, withdrawed=is_withrawed)
        if new_transaction:
            return JsonResponse({'result': True, 'message': message, 'url': '/home'}, safe=False, status=201)

        return JsonResponse({'result': False, 'errors': 'server internal error'}, safe=False, status=500)

    return render(request, f'auth/{action}.html',  context)
