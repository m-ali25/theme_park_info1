import numpy as np
import requests
import pandas as pd
import psycopg2 as psql
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('sql_username')
password = os.getenv('sql_password')
my_host = os.getenv('host')

url = 'https://queue-times.com/parks.json'
response = requests.get(url)
parks_data = response.json()
        
park_id = [x["id"] for park_group in parks_data for x in park_group["parks"]]

def get_ride_details(park_id):
    try:
        url_parks = f'https://queue-times.com/parks.json'
        response_parks = requests.get(url_parks)
        parks_data = response_parks.json()

        url_queue_times = f'https://queue-times.com/parks/{park_id}/queue_times.json'
        response_queue_times = requests.get(url_queue_times)
        queue_data = response_queue_times.json()
        
        park_name = None
        for park_group in parks_data:
            for park in park_group["parks"]:
                if park['id'] == park_id:
                    park_name = park["name"]
                    break
            if park_name:
                break
        
        if not park_name:
            return 'Error: Park not found'
        
        lands = queue_data.get("lands", [])
        ride_details = []
        
        for land in lands:
            land_name = land["name"]
            rides = land.get("rides", [])
            
            for ride in rides:
                name = ride.get("name")
                wait_time = ride.get("wait_time")
                ride_status = 'open' if ride.get('is_open') else 'closed'
                ride_details.append((park_name, name, ride_status, wait_time))
        
        return ride_details
    
    except:
        return 'Error'

def fetch_parks_data():
    url = 'https://queue-times.com/parks.json'
    response = requests.get(url)
    parks_data = response.json()
    return parks_data

parks_data = fetch_parks_data()

all_ride_details = []

for park_group in parks_data:
    for park in park_group["parks"]:
        park_id = park["id"]
        ride_details = get_ride_details(park_id)
        if ride_details:
            all_ride_details.extend(ride_details)

park_db = pd.DataFrame(all_ride_details,columns = ["park_name", "ride_name", "ride_status", "wait_time"])

park_db

conn = psql.connect(database = "pagila",
                    user = username,
                    host = my_host,
                    password = password,
                    port = 5432
                    )

cur = conn.cursor()

sql = """
INSERT INTO student.park_db (park_name, ride_name, ride_status, wait_time)
VALUES (%s, %s, %s, %s)
"""

cur.executemany(sql, park_db.values)

conn.commit()
conn.close()