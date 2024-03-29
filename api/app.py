from multiprocessing import Process
import threading

# COLOR SENSOR

from TCS34725 import ColourSensor
import time, sys, smbus

address = 0x29

CS = ColourSensor(address)
CS.set_a_time(atime=24) # set ATIME to 24ms, max count 10240
CS.set_wait_time(wtime=43.2,wlong=0)               # set WTIME to 43.2ms
CS.set_gain(4)                                     # set gain to 4x

# set interrupt and persistance levels
CS.set_interrupt_levels(lowTL = 56, highTL = 8000, persLevel = 3)

CS.set_enables(pon=1, aen=1, wen=1, aien=0)        # turn on PON, AEN and WEN


# FLASK

from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)


# DHT-11 SENSORS

import Adafruit_DHT
DHT_SENSOR_ROOM = Adafruit_DHT.DHT11
DHT_SENSOR_STREET = Adafruit_DHT.DHT11
DHT_PIN_ROOM = 4
DHT_PIN_STREET = 17

# BMP-180 SENSOR

import Adafruit_BMP.BMP085 as BMP085
bmp180Sensor = BMP085.BMP085()


# API WEATHER DATA

city_ru = 'Пенза'
city_en = 'Penza'
API_key_weather = "3ba9c0e9246cf9ee76413878ea521077"

api_weather_data = {'q': city_en, 'units': 'metric', 'APPID': API_key_weather, 'lang': 'ru'}



def get_now_data():
    # weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather", params=api_weather_data).json()

    lightColor, presBMP, altBMP, humidity_room, humidity_street, humidity_room, temperature_room, temperature_street = 0, 0, 0, 0, 0, 0, 0, 0

    # tempBMP = round(bmp180Sensor.read_temperature(), 1)
    presBMP = round(bmp180Sensor.read_pressure()/100*0.7501, 1)
    altBMP =  round(bmp180Sensor.read_altitude(),1)

    humidity_room, temperature_room = Adafruit_DHT.read(DHT_SENSOR_ROOM, DHT_PIN_ROOM)
    time.sleep(0.25)
    humidity_street, temperature_street = Adafruit_DHT.read(DHT_SENSOR_STREET, DHT_PIN_STREET)

    try:
        lightColor = round(CS.read_CRGB()[0] / 3600 * 100)
    except:
        pass

    if lightColor > 100: lightColor = 100

    if temperature_room is not None and temperature_street is not None and humidity_room is not None and humidity_street is not None and presBMP is not None and altBMP is not None:
        return {'city': city_ru, 'lightColor': lightColor, 'tempStreet': temperature_street, 'tempRoom': temperature_room, 'tempStreetReal': temperature_street - 5, 'humidity_room': humidity_room, 'humidity_street': humidity_street, 'pressure': presBMP, 'alt': altBMP}
    else:
        return {}

def get_forecast_data_chart(days):
    try:
        result_forecast = []

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

        result_data_chart = [[], []]

        for i in range(start_index, days):
            result_forecast.append(result_list[i][0]['dt_txt'][:10])
            for i in result_list[i]:
                result_data_chart[0].append(i['dt_txt'][11:16])
                result_data_chart[1].append('{0:+3.0f}'.format(i['main']['temp']))

        return result_data_chart
    except:
        pass

def get_forecast_data(days):
    try:
        result_forecast = []

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
        if(days != 1): start_index = 1

        for i in range(start_index, days):
            temp_forecast = []
            temp_forecast.append(result_list[i][0]['dt_txt'][:10])
            for i in result_list[i]:
                temp_forecast.append(i['dt_txt'][11:16] + ' ' + '{0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0]['description'])
            result_forecast.append(temp_forecast)
        return result_forecast
    except:
        pass


@app.route("/now")
def now():
    return jsonify(get_now_data())

@app.route("/forecast/<int:days>")
def forecast(days):
    return jsonify(get_forecast_data(days))

@app.route("/forecast_chart/<int:days>")
def forecast_chart(days):
    return jsonify(get_forecast_data_chart(days))


if __name__ == "__main__":
    app.run(debug=True)



CS.clear_interrupt()
del(CS)