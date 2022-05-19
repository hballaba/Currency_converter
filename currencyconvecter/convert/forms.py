from django import forms

class CurrencyForm(forms.Form):
    amount = forms.IntegerField()
    currency_from = forms.CharField(label='currency_from')
    currency_to = forms.CharField(label='currency_to')
