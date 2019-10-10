from django.urls import path

from .views import display_form

app_name = 'core'

urlpatterns = [
    path('', display_form, name='transfer_form'),
]
