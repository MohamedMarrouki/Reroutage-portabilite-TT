from django import forms

class DateInput(forms.DateInput):
    input_type='date'
    

class FiltreForm(forms.Form):
    call_day=forms.DateField(widget=DateInput)
    origin=forms.ChoiceField(label='Select an option', choices=[
        ('national', 'National'),
        ('international', 'International'),
    ])
    