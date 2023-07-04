from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type='date'
    

class FiltreForm(forms.Form):
    call_day=forms.DateField(widget=DateInput)
    origin=forms.ChoiceField(label='Select an option', choices=Country.objects.values_list('Code','Pays')
    )
    trunk=forms.ChoiceField(label='Select an option', choices=[
        ('ALL', 'ALL'),
        ('INORDI', 'Ooredoo In'),
        ('OUTODOO', 'Ooredoo Out'),
        ('INORGI', 'Orange In'),
        ('OUTORGO', 'Orange Out'),
    ])
    