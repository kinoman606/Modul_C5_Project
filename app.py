from extensions import APIException, ExchangeCurrency
from config import TOKEN, currencies
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> ' \
'<имя валюты, в которой надо узнать цену первой валюты> ' \
'<количество первой валюты> \n Для ознакомления со списком поддерживаемых валют введите /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for currency in currencies.keys():
        text = '\n'.join((text, currency, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Вы ввели некорректные параметры')
        base, quote, amount = values
        price = ExchangeCurrency.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {price}'
        bot.send_message(message.chat.id, text)

bot.polling()