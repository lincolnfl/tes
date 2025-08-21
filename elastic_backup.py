import requests
import json
import time

logstash_url = "http://logstash:5044/"  # Use the Logstash container name

while True:
    try:
        response = requests.get("https://data.traffic.hereapi.com/v7/flow?in=circle:3.575953,98.621565;r=1000&locationReferencing=olr&apiKey=xZRysV5GhtBQn8FNB_ddUzuiWJd6YYNsQUuIJE9D498")
        if response.status_code == 200:
            traffic_data = response.json()
            
            # Prepare the data to be sent to Logstash
            data = {
                "message": json.dumps(traffic_data)
            }

            # Send data to Logstash
            post_response = requests.post(logstash_url, json=data)

            if post_response.status_code == 200:
                print("Data sent to Logstash successfully.")
            else:
                print("Failed to send data to Logstash.")

        else:
            print("Failed to fetch data from the API.")

        # Sleep for 60 seconds (1 minute) before the next iteration
        time.sleep(60)

    except Exception as e:
        print(f"An error occurred: {str(e)}")