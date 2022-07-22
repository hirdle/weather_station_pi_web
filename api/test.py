import requests
url = 'http://127.0.0.1:5000/forecast/2'
data = requests.get(url).json()
print(data)
