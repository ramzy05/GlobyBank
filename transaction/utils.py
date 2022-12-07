def get_type_of_transaction(user, orderer, receiver,sent_amount, received_amount):
    output = 'Transfer'
    if orderer.username ==  receiver.username :
        if sent_amount == 0 :
            output = 'Deposit'
        elif received_amount == 0:
            output = 'Witdrawal'
    else:
        if user.username == receiver.username:
            output = 'Reception'
    
    return output

