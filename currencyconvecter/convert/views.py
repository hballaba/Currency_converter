from django.shortcuts import render
import requests
from xml.dom import minidom
from  django.views.generic import View

from .forms import CurrencyForm

def get_currency_dictionary_with_date(url):
    response = requests.get(url)

    dom = minidom.parseString(response.text)
    dom.normalize()

    response_date = dom.firstChild.getAttribute("Date")
    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = child.firstChild.data
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value
    return currency_dict, response_date


class Main(View):
    def get(self, request):
        return render(request, 'convert/index.html')


class Currency(View):
    def get(self, request):
        url = 'https://cbr.ru/scripts/XML_daily.asp'
        currency_dict, response_date = get_currency_dictionary_with_date(url)
        return render(request, 'convert/currency.html', {'response': currency_dict, 'date': response_date})


class Converter(View):


    def post(self, request):
        url = 'https://cbr.ru/scripts/XML_daily.asp'
        form = CurrencyForm(request.POST)
        if form.is_valid():
            char_code_to = form.cleaned_data['currency_to']
            char_code_from = form.cleaned_data['currency_from']
            amount = form.cleaned_data['amount']

            currency_dict, response_date = get_currency_dictionary_with_date(url)
            currency_value_to = float(currency_dict[char_code_to].replace(',', '.'))
            currency_value_from = float(currency_dict[char_code_from].replace(',', '.'))

            currency_converted = round(currency_value_from / currency_value_to * amount, 2)

            return render(request, 'convert/convert.html', {'form': form, 'currency_converted': currency_converted})

    def get(self, request):
        url = 'https://cbr.ru/scripts/XML_daily.asp'
        currency_dict, response_date = get_currency_dictionary_with_date(url)
        char_codes = currency_dict.keys()
        form = CurrencyForm()

        return render(request, 'convert/convert.html', {'char_codes': char_codes, 'form': form})
