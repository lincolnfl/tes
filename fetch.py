import requests
import json
import time
from connection import create_connection
from connection2 import connection_postgres
import psycopg2

# Define a list of API keys
api_keys = ['key1', 'key2', 'key3']  # Add your API keys here

# Helper function to get data with retry
def get_data_with_retry(api_keys):
    for api_key in api_keys:
        try:
            response_API = requests.get(f'https://data.traffic.hereapi.com/v7/flow?in=circle:3.575953,98.621565;r=1000&locationReferencing=olr&apiKey={api_key}')

            if response_API.status_code == 200:
                return response_API.json()
            else:
                print(f"Request failed with API key {api_key}, status code: {response_API.status_code}")
        except Exception as e:
            print(f"Exception occurred with API key {api_key}: {str(e)}")

    print("All API keys exhausted. Unable to retrieve data.")
    return None

while True:
    connection = create_connection()
    connection2 = connection_postgres()
    if connection and connection2 is not None:
        cursor = connection.cursor()
        cursorPostgres = connection2.cursor()
    
    # Call the function to get data with retry
    results = get_data_with_retry(api_keys)

    if results is not None:
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
            
            cursorPostgres.execute("INSERT INTO traffic_location (description, length, olr) VALUES (%s, %s, %s)", (description, length, olr))
            cursor.execute("INSERT INTO traffic_flow (speed, speedUncapped, freeFlow, jamFactor, confidence, traversability, road) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (speed, speedUncapped, freeFlow, jamFactor, confidence, traversability, road))
    else:
        print("No data retrieved.")

    connection.commit()
    connection2.commit()
    time.sleep(1)
    # connection.close()

