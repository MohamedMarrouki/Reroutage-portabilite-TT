from django import forms

class DateInput(forms.DateInput):
    input_type='date'
    

class FiltreForm(forms.Form):
    call_day=forms.DateField(widget=DateInput)
    origin=forms.ChoiceField(label='Select an option', choices=[
        ('national', 'National'),
        ('international', 'International'),
    ])
    trunk=forms.ChoiceField(label='Select an option', choices=[
        ('ALL', 'ALL'),
        ('INORDI', 'Ooredoo In'),
        ('OUTODOO', 'Ooredoo Out'),
        ('INORGI', 'Orange In'),
        ('OUTORGO', 'Orange Out'),
    ])
    