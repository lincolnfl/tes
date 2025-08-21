import requests
import json
import time
from connection import create_connection

counter = 0
while True:
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
    else:
        print("Database connection is not available.")
    response_API = requests.get('https://data.traffic.hereapi.com/v7/flow?in=circle:3.575953,98.621565;r=1000&locationReferencing=olr&apiKey=xZRysV5GhtBQn8FNB_ddUzuiWJd6YYNsQUuIJE9D498')

    if response_API.status_code == 200:
        results = response_API.json()

        # Access the "location" field in each result
        if "results" in results:
            print("Time:", results["sourceUpdated"])
            for result in results["results"]:
                locations = result["location"]
                description = locations["description"]
                length = locations["length"]
                olr = locations["olr"]
                currentFlow = result["currentFlow"]
                speed = currentFlow["speed"]
                speedUncapped = currentFlow["speedUncapped"]
                freeFlow = currentFlow["freeFlow"]
                jamFactor = currentFlow["jamFactor"]
                confidence = currentFlow["confidence"]
                traversability = currentFlow["traversability"]
                road = locations["description"]
                # cursorPostgres
                # cursorPostgres.execute("INSERT INTO traffic_location (description, length, olr) VALUES (%s, %s, %s)", (description, length, olr))
                cursor.execute("INSERT INTO traffic_flow (speed, speedUncapped, freeFlow, jamFactor, confidence, traversability, road) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (speed, speedUncapped, freeFlow, jamFactor, confidence, traversability, road))
                
        else:
            print("No 'results' key found in the API response.")
    else:
        print(f"Error: {response_API.status_code}")
    connection.commit()
    counter = counter + 1
    print(counter)
else:
    print("Database connection is not available.")
