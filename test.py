import requests
import json

response_API = requests.get('https://data.traffic.hereapi.com/v7/flow?in=circle:3.575953,98.621565;r=1000&locationReferencing=olr&apiKey=xZRysV5GhtBQn8FNB_ddUzuiWJd6YYNsQUuIJE9D498')
result = response_API.json()
print(result)