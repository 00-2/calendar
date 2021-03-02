import requests
response = requests.get('http://127.0.0.1:8000/getCalendarData?{"seconds":3800,"creator":mihacsta@gmail.com}'.encode('utf-8'))
print(response.json())