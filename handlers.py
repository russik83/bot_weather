import requests
from datetime import datetime
from config import api_token, url
from telegram import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ConversationHandler


def start(update, context):
    my_keyboard = ReplyKeyboardMarkup([['погода сейчас', '24 часа']], resize_keyboard=True)
    update.message.reply_text(f'Привет, {update.message.from_user.username} хочешь узнать погоду?!',
                                reply_markup=my_keyboard)


def get_weather(update, context):
    update.message.reply_text('Пожалуйста введите название города!')
    return WEATHER


def get_weather_daily(update, context):
    update.message.reply_text('Пожалуйста введите название города!')
    return WEATHER_DAILY


def main_keyboard():
    return ReplyKeyboardMarkup([['погода сейчас', '24 часа']], resize_keyboard=True)


def cancel(update, context):
    update.message.reply_text('Я вас не понимаю!')
    return ConversationHandler.END


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
WEATHER_DAILY = 2

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
        f"Погода в {data['list'][0]['name']} : {int(data['list'][0]['main']['temp'])}🌡️\n"
        f"Ощущается как: {int(data['list'][0]['main']['feels_like'])}🌡️\n"
        f"Минимальная температура ⬇️: {int(data['list'][0]['main']['temp_min'])}🌡️\n"
        f"Максимальная температура ⬆️: {int(data['list'][0]['main']['temp_max'])}🌡️\n"
        f"Давление: {int(data['list'][0]['main']['pressure'])}мм рт. ст.\n"
        f"Влажность: {int(data['list'][0]['main']['humidity'])}%\n"
        f"Скорость ветра: {int(data['list'][0]['wind']['speed'])} м/с\n"
        f"{(data['list'][0]['weather'][0]['description']).capitalize()}\n"
        f"{recommendation}",
        reply_markup=main_keyboard()
        )
    except(requests.RequestException):
        update.message.reply_text('Сервис недоступен')
    except(ValueError, KeyError, IndexError):
        update.message.reply_text('Такой город ' + city + ' не найден')
    return ConversationHandler.END

def weather_daily(update, context):
    city = update.message.text
    try:
        responce = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast?&cnt=8',
            params={'q': city, 'type':'like','units': 'metric', 
                'appid': api_token, 'lang': 'ru', 'exclude': 'daily'}
            )
        responce.raise_for_status()
        data = responce.json() 
        for weather_block in data["list"]:
            weather_block["dt_txt"] = datetime.strptime(weather_block["dt_txt"], '%Y-%m-%d %H:%M:%S')
            hour = weather_block['dt_txt'].hour
            if hour == 6:
                morning = weather_block
            elif hour == 12:
                day = weather_block
            elif hour == 18:
                evening = weather_block
            elif hour == 0:
                night = weather_block
            
        morning = f"""<b>Погода утром</b>
    Темпереатура: {morning['main']['temp']}🌡️
    Ощущается как: {morning['main']['feels_like']}🌡️
    Минимальная температура: {morning['main']['temp_min']}🌡️
    Максимальная температура: {morning['main']['temp_max']}🌡️
    Давление: {morning['main']['pressure']}мм рт. ст.
    Влажность: {morning['main']['humidity']}%
    Скорость ветра: {morning['wind']['speed']}м/с
    <b><em>{(morning['weather'][0]['description']).upper()}</em></b>""" 
        day = f"""<b>Погода днём</b>
    Темпереатура {day['main']['temp']}🌡️
    Ощущается как: {day['main']['feels_like']}🌡️
    Минимальная температура: {day['main']['temp_min']}🌡️
    Максимальная температура: {day['main']['temp_max']}🌡️
    Давление: {day['main']['pressure']}мм рт. ст.
    Влажность: {day['main']['humidity']}%
    Скорость ветра: {day['wind']['speed']}м/с
    <b><em>{(day['weather'][0]['description']).upper()}</em></b>"""
        evening = f"""<b>Погода вечером</b>
    Темпереатура {evening['main']['temp']}🌡️
    Ощущается как: {evening['main']['feels_like']}🌡️
    Минимальная температура: {evening['main']['temp_min']}🌡️
    Максимальная температура: {evening['main']['temp_max']}🌡️
    Давление: {evening['main']['pressure']}мм рт. ст.
    Влажность: {evening['main']['humidity']}%
    Скорость ветра: {evening['wind']['speed']}м/с
    <b><em>{(evening['weather'][0]['description']).upper()}</em></b>"""
        night = f"""<b>Погода ночью</b>
    Темпереатура {night['main']['temp']}🌡️
    Ощущается как: {night['main']['feels_like']}🌡️
    Минимальная температура: {night['main']['temp_min']}🌡️
    Максимальная температура: {night['main']['temp_max']}🌡️
    Давление: {night['main']['pressure']}мм рт. ст.
    Влажность: {night['main']['humidity']}%
    Скорость ветра: {night['wind']['speed']}м/с
    <b><em>{(night['weather'][0]['description']).upper()}</em></b>"""

        update.message.reply_text(
            f"Прогноз погоды на 24 часа: \n{morning}\n{day}\n{evening}\n{night}", 
            reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
        )

    
    except(requests.RequestException):
        update.message.reply_text('Сервис недоступен')
    except(ValueError, KeyError, IndexError):
        update.message.reply_text('Такой город ' + city + ' не найден')
        raise
    return ConversationHandler.END
