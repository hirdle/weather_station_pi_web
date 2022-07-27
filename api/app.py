from flask import Flask
from flask import Response
from flask import jsonify
import json

app = Flask(__name__)

import requests

import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# import Adafruit_BMP.BMP085 as BMP085
# bmp180Sensor = BMP085.BMP085()


city_ru = 'Пенза'
city_en = 'Penza'
API_key_weather = "3ba9c0e9246cf9ee76413878ea521077"

api_weather_data = {'q': city_en, 'units': 'metric', 'APPID': API_key_weather, 'lang': 'ru'}

def get_now_data():
    weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather", params=api_weather_data).json()

    tempBMP, presBMP, altBMP, humidity = 0, 0, 0, 0

    # tempBMP = round(bmp180Sensor.read_temperature(), 1)
    # presBMP = round(bmp180Sensor.read_pressure()/100*0.7501, 1)
    # altBMP =  round(bmp180Sensor.read_altitude(),1)

    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)


    if humidity is not None:
        return {'city': city_ru, 'temp': tempBMP, 'tempReal': tempBMP - 5, 'humidity': humidity, 'pressure': presBMP, 'alt': altBMP}
    else:
        return (city_ru, tempBMP, weather_data['main']['humidity'], presBMP, altBMP, tempBMP - 5)

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
        # if(days != 1): start_index = 1

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