import json
import requests
from config import currencies, API


class APIException(Exception):
    pass


class ExchangeCurrency:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Вы пытаетесь конвертировать одну и ту же валюту {quote}')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту {base}')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        #начало блока для взаимодействия с ресурсом apilayer.com:
        url = f"https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"
        payload = {}
        headers = {"apikey": API}
        response = requests.request("GET", url, headers=headers, data=payload) #конец блока для взаимодействия с ресурсом apilayer.com

        price = json.loads(response.text)['result']

        return price

