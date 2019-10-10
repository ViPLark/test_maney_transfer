import math
from decimal import Decimal
from logging import getLogger

from django.db import transaction

from .config import money_sign

logger = getLogger(__name__)


def calc_amount_per_user(amount, user_count):
    amount_per_user = Decimal.from_float(
        math.floor(amount * 100 / user_count) / 100
    )
    return amount_per_user


def make_money_transfer(user_from, users_to, amount):
    logger.info('Осуществляем перевод денежных средств...')
    user_count = len(users_to)
    amount_per_user = calc_amount_per_user(amount, user_count)
    if amount_per_user == 0:
        logger.info('Холостой перевод')
        return

    with transaction.atomic():
        for user_to in users_to:
            user_to.amount += amount_per_user
            user_to.save(update_fields=('amount',))
            logger.info(f'Пользователю {user_to} планируется перевести {amount_per_user} {money_sign}')
        total_amount = amount_per_user * user_count
        user_from.amount -= total_amount
        user_from.save(update_fields=('amount',))
        logger.info(f'Перевод успешно завешрён. Пользователь {user_from} перевёл {total_amount} {money_sign}')
