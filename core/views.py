from logging import getLogger

from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import render

from .forms import TransferForm

logger = getLogger(__name__)


def display_form(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except DatabaseError:
                message = 'Ошибка при совершении транзакции.'
                logger.exception(message)
                message += ' Попробуйте ещё раз или обратитесь в службу поддержки'
                messages.error(request, message)
            else:
                messages.success(request, 'Перевод совершён')
            form = TransferForm()
    else:
        form = TransferForm()

    context = {
        'form': form,
    }
    return render(request, template_name='core/transfer.html', context=context)
