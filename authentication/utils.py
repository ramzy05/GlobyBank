import random


def get_random_pin():
    pin = ''
    for _ in range(4):
        pin += str(random.randint(1, 9))
    return pin
