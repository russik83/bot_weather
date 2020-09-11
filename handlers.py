import requests
from config import api_token, url
from telegram import ReplyKeyboardMarkup, KeyboardButton


def start(update, context):
    my_keyboard = ReplyKeyboardMarkup([['погода']], resize_keyboard=True)
    update.message.reply_text(f'Привет, {update.message.from_user.username} хочешь узнать погоду?!',
                                reply_markup=my_keyboard)


def get_weather(update, context):
    update.message.reply_text('Пожалуйста введите название города!')
    return WEATHER


def cancel(update, context):
    update.message.reply_text('Я вас не понимаю!')


def get_recommendation(data):
    if int(data['list'][0]['main']['temp']) < -30:
        return "Очень холодно, оденься теплее!))"
    elif int(data['list'][0]['main']['temp']) < -10:
        return "Холодно, оденься потеплее!))"
    elif int(data['list'][0]['main']['temp']) < 10:
        return "Очень холодно, оденься потеплее!))"
    elif int(data['list'][0]['main']['temp']) < 20:
        return "Сейчас прохладно, лучше оденься!))"
    elif int(data['list'][0]['main']['temp']) < 25:
        return "Сейчас тепло!"
    elif int(data['list'][0]['main']['temp']) > 40:
        return "Не холодно, хоть в шортах иди!:)"


WEATHER = 1

def weather(update, context):
    city = update.message.text
    try:
        responce = requests.get(
            url,
            params={'q': city, 'type':'like','units': 'metric', 'appid': api_token, 'lang': 'ru'}
            )
        responce.raise_for_status()
        data = responce.json()
        recommendation = get_recommendation(data)

        update.message.reply_text(
        f"Погода в: {data['list'][0]['name']} : {int(data['list'][0]['main']['temp'])}🌡️\n"
        f"Ощущается как: {int(data['list'][0]['main']['feels_like'])}🌡️\n"
        f"Минимальная температура ⬇️: {int(data['list'][0]['main']['temp_min'])}🌡️\n"
        f"Максимальная температура ⬆️: {int(data['list'][0]['main']['temp_max'])}🌡️\n"
        f"Давление: {int(data['list'][0]['main']['pressure'])}мм рт. ст.\n"
        f"Влажность: {int(data['list'][0]['main']['humidity'])}%\n"
        f"Скорость ветра: {int(data['list'][0]['wind']['speed'])} м/с\n"
        f"{(data['list'][0]['weather'][0]['description']).capitalize()}\n"
        f"{recommendation}"
        )
    except(requests.RequestException):
            update.message.reply_text('Сервис недоступен')
    except(ValueError, KeyError, IndexError):
            update.message.reply_text('Такой город ' + city + ' не найден')
    return WEATHER
