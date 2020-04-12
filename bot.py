!pip install pyTelegramBotAPI

import requests

api_key_weather = '674b6d638e69f74f581eb3d5337d8667'

def get_weather(lat, lon):
    url_weather = ' http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+api_key_weather

    weather_data = requests.get(url_weather).json()

    main_weather_eng  = weather_data['weather'][0]['main']
    if main_weather_eng == 'Rain':
        main_weather = 'Дождь. '
    elif main_weather_eng == 'Snow':
        main_weather = 'Снег. '
    elif main_weather_eng == 'Clouds':
        main_weather = 'Облачно. '
    elif main_weather_eng == 'Clear':
        main_weather = 'Солнечно. '
    elif main_weather_eng == 'Thunderstorm':
        main_weather = 'Шторм. '
    else:
        main_weather = 'Погода не определена. '

    temp = round(weather_data['main']['temp'] - 273.17)
    temp_weater = 'Температура: '+str(temp)+' °C. '
    wind = round(weather_data['wind']['speed'])
    wind_weather = 'Скорость ветра: '+str(wind)+'м/с. '

    weather = main_weather+temp_weater+wind_weather
    recomend = recomendations(main_weather, temp, wind)

    return weather+recomend

def recomendations(main_weather, temp, wind):

    if main_weather == 'Дождь.' or main_weather == 'Снег.':
        a = 'непромокаемое '
    else:
        a = ''

    if temp >= 15:
        b = 'не теплое '
    elif 0 <= temp < 15:
        b = 'теплое '
    elif temp < 0:
        b = 'очень теплое '

    if wind > 15:
        c = 'непродуваемое'
    else:
        c = ''

    return 'Рекомендую надеть '+a+b+c+'.'

import time
import telebot
from telebot.types import Message

token = '920956407:AAG-bsnhecr_k6OHHH1neksLQn-GxDpGJvg'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.chat.id, 'Привет. Хотите узнать погоду? Отправь мне локацию')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Этот бот предоставляет информацию о погоде на сегодня в указанном месте. Для информации прикрепите локацию')

@bot.message_handler(content_types=['location'])
def handle_location(message):
    weather_message = get_weather(message.location.latitude, message.location.longitude)
    bot.send_message(message.chat.id, weather_message)

@bot.message_handler(func=lambda message: True)
def send_error(message: Message):
    bot.send_message(message.chat.id, 'Отправь мне локацию и я пришлю тебе погоду')


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception:
        # print(Exception.args)
        time.sleep(2)
