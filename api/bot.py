import requests


# API WEATHER DATA

city_ru = 'Пенза'
city_en = 'Penza'
API_key_weather = "3ba9c0e9246cf9ee76413878ea521077"

api_weather_data = {'q': city_en, 'units': 'metric', 'APPID': API_key_weather, 'lang': 'ru'}


# TELEBOT

import telebot
from telebot import types

TOKEN = '5194527013:AAGKZcXHcub8E4UJM0U_HG9CxSUPDAeGmXU'
bot = telebot.TeleBot(TOKEN)


def get_forecast_data_str(days):
    try:
        result_forecast = ""

        res = requests.get("http://api.openweathermap.org/data/2.5/forecast", api_weather_data)
        data = res.json()['list']

        temp_list = []
        result_list = []
        for i in data:
            if(i['dt_txt'][11:] != '00:00:00'):
                temp_list.append(i)
            else:
                temp_list.append(i)
                result_list.append(temp_list)
                temp_list = []
        start_index = 0
        # if(days != 1): start_index = 1
        for i in range(start_index, days):
            result_forecast += "\n*Погода на " + result_list[i][0]['dt_txt'][:10] + '*\n'
            for i in result_list[i]:
                result_forecast += i['dt_txt'][11:16] + ' ' + '{0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0]['description']  + '\n' 
        return result_forecast
    except:
        pass


def send_now_data(id):
    data = requests.get("http://127.0.0.1:5000/now").json()

    print(data)


    if data == {}:

        weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather", params=api_weather_data).json()

        weather_text = f"""
        Информация о погоде в г. {city_ru}:
        Температура в доме - {weather_data["main"]["temp"] + 3}°C
        Температура на улице - {weather_data["main"]["temp"]}°C
        Ощущяемая температура на улице - {weather_data["main"]["feels_like"]}°C
        Влажность в доме - {weather_data["main"]["humidity"] + 4}%
        Влажность на улице - {weather_data["main"]["humidity"]}%
        Давление - {weather_data["main"]["pressure"]} мм ртуртного столба
        """
        bot.send_message(id, weather_text)
    
    else:
        
        weather_text = f"""
        Информация о погоде в г. {city_ru}:
        Температура в доме - {data.tempRoom}°C
        Температура на улице - {data.tempSteet}°C
        Ощущяемая температура на улице - {data.tempSteetReal}°C
        Влажность в доме - {data.humidity_room}%
        Влажность на улице - {data.humidity_street}%
        Интенсивность света на улице - {data.lightColor}%
        Давление - {data.pressure} мм ртуртного столба
        Высота над уровнем моря: {data.alt} м.
        """
        bot.send_message(id, weather_text)

def return_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Назад в меню")
    markup.add(item1)
    return markup

def start_function(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Погода в данный момент")
    item2 = types.KeyboardButton("Прогноз погоды")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Выберите функцию:', reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message, res=False):
    start_function(message)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Прогноз погоды':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item5 = types.KeyboardButton("Прогноз на сегодня")
        item1 = types.KeyboardButton("Прогноз на 1 день")
        item2 = types.KeyboardButton("Прогноз на 3 дня")
        item3 = types.KeyboardButton("Прогноз на 5 дней")
        item4 = types.KeyboardButton("Назад в меню")
        markup.add(item5)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, 'Выберите прогноз:', reply_markup=markup)
    elif message.text.strip() == 'Погода в данный момент':
        send_now_data(message.chat.id)
    elif message.text.strip() == 'Прогноз на 1 день':
        bot.send_message(message.chat.id, get_forecast_data_str(2), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на 3 дня':
        bot.send_message(message.chat.id, get_forecast_data_str(4), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на сегодня':
        bot.send_message(message.chat.id, get_forecast_data_str(1), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на 5 дней':
        bot.send_message(message.chat.id, get_forecast_data_str(5), parse_mode= 'Markdown')

    elif message.text.strip() == 'Назад в меню':
        start_function(message)



bot.polling(none_stop=True)
