from logging import getLogger

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .controller import make_money_transfer
from .utils import parse_inns

logger = getLogger(__name__)
User = get_user_model()


class TransferForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target_users = None

    user_from = forms.ModelChoiceField(User.objects.all().only('id', 'username'), label='Пользователь')
    users_to = forms.CharField(label='Список ИНН', widget=forms.Textarea)
    amount = forms.DecimalField(max_digits=8, decimal_places=2, label='Сумма')

    def clean_amount(self):
        if self.cleaned_data['amount'] <= 0:
            raise ValidationError('Введите корректную сумму больше нуля')

        user = self.cleaned_data['user_from']
        if user.amount < self.cleaned_data['amount']:
            raise ValidationError('На счету пользователя недостаточно средств')
        return self.cleaned_data['amount']

    def clean_users_to(self):
        users_to_text = self.cleaned_data['users_to']
        inns = parse_inns(users_to_text)
        if not inns:
            raise ValidationError(f'Невалидный ИНН "{users_to_text}"')
        users_to = User.objects \
            .filter(inn__in=inns) \
            .only('id', 'amount', 'inn') \
            # .exclude(pk=self.cleaned_data['user_from'].pk)  # TODO Уточнить в ТЗ
        known_inns = {u.inn for u in users_to}
        unknown_inns = inns - known_inns
        if unknown_inns:
            inns_str = '", "'.join(map(str, unknown_inns))
            raise ValidationError(f'Следующие ИНН не существуют: "{inns_str}"')
        return users_to

    def save(self, *args, **kwargs):
        make_money_transfer(
            user_from=self.cleaned_data['user_from'],
            users_to=self.cleaned_data['users_to'],
            amount=self.cleaned_data['amount'],
        )
