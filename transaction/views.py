from authentication.models import Account
from .models import Transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import decimal
from .utils import get_type_of_transaction

def welcome_view(request):
    context = {}
    return render(request, 'auth/index.html', context)



class HomeView(TemplateView,LoginRequiredMixin):
    template_name = 'auth/home.html'
    login_url = 'login'

   
    def get(self, request):
        user = self.request.user
        transactions = Transaction.objects.filter(Q(orderer=user) | Q(receiver=user)
                                                )
        # to get index for the table
        transactions = [[i+1, t, get_type_of_transaction(user, t.orderer, t.receiver, t.amount_sent, t.amount_received)] for i, t in enumerate(transactions)]
        context = {'transactions': transactions, 'currency' :'XAF'}
        return render(request, self.template_name,  context)
    


@login_required(login_url='login')
def transfer_view(request):
    user = request.user
    min_amount = 5
    max_amount = user.balance
    users = Account.objects.exclude(username=user.username)

    context = {
        'user': user,
        'currency': 'XAF',
        'max_amount': max_amount,
        'min_amount': min_amount,
        'users': users,
    }
    message = None
    if request.method == 'POST':
        user_pin_code = request.POST['pin_code']
        sent_amount = decimal.Decimal(request.POST['amount'])
        received_amount = sent_amount

        if user_pin_code != user.code_pin:
            message = 'Your pin code is incorrect'
            return JsonResponse({'result': False, 'errors': {'code_pin': [{'message': message}]}}, safe=False, status=400)
        receiver = Account.objects.get(
            username=request.POST['receiver']) or None

        if receiver is None:
            message = 'Unkwown receiver'
            return JsonResponse({'result': False, 'errors': {'receiver': [{'message': message}]}}, safe=False, status=400)
        # Everything is good we can make the transaction between the too user
        user.balance -= sent_amount
        if user.balance <= 0:
            user.balance = 0.00
        receiver.balance += received_amount
        user.save(update_fields=['balance'])
        receiver.save(update_fields=['balance'])
        new_transaction = Transaction.objects.create(
            orderer=user, receiver=receiver, amount_sent=sent_amount, amount_received=received_amount)
        if new_transaction:
            message = 'Transaction has been completed'
            return JsonResponse({'result': True,'message':message, 'url': '/home'}, safe=False, status=201)

        return JsonResponse({'result': False, 'errors': 'server internal error'}, safe=False, status=500)

    return render(request, 'auth/transfer.html',  context)


@login_required(login_url='login')
def recharge_withdraw_view(request, action):
    user = request.user
    min_amount = 5
    max_amount = 10000
    context = {
        'user': user,
        'currency': 'XAF',
        'max_amount': max_amount,
        'min_amount': min_amount
    }
    message =  None
    if request.method == 'POST':
        user_pin_code = request.POST['pin_code']
        amount = decimal.Decimal(request.POST['amount'])
        action = request.POST['action'] or None

        if user_pin_code != user.code_pin:
            message = 'Your pin code is incorrect'
            return JsonResponse({'result': False, 'errors': {'code_pin': [{'message': message}]}}, safe=False, status=400)
        message = ''
        sent_amount = 0
        received_amount = 0
        if action == 'withdraw':
            user.balance -= amount
            message = 'Your withdrawal has been complete successfully'
            sent_amount = amount
            if user.balance <= 0:
                user.balance = 0.00

        elif action == 'recharge':
            user.balance += amount
            received_amount = amount
            message = 'Your Deposit has been complete successfully'

        user.save(update_fields=['balance'])
        new_transaction = Transaction.objects.create(
            orderer=user, receiver=user, amount_sent=sent_amount, amount_received=received_amount)
       
        if new_transaction:
            return JsonResponse({'result': True, 'message': message, 'url': '/home'}, safe=False, status=201)

        return JsonResponse({'result': False, 'errors': 'server internal error'}, safe=False, status=500)

    return render(request, f'auth/{action}.html',  context)

class HistoryView(HomeView):
    template_name  = 'auth/history.html'