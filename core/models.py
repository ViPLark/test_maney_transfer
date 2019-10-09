from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    inn = models.IntegerField(db_index=True, help_text='ИНН')
    amount = models.DecimalField(max_digits=8, decimal_places=2, help_text='Счёт')

    @property
    def amount_display(self):
        return f'{self.amount} ₽'
