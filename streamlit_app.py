import streamlit as st
import pandas as pd
import numpy as np
import sqlalchemy
import psycopg2 
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine

db_username = st.secrets["DB_USERNAME"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOST"]
db_name = st.secrets["DB_NAME"]
db_port = st.secrets["DB_PORT"]

def db_connect():
    try:
        engine = create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
        
        query = '''
        SELECT t1.*
        FROM student.park_db t1
        INNER JOIN (
            SELECT park_name, ride_name, MAX(ctid) as max_ctid
            FROM student.park_db
            GROUP BY park_name, ride_name
        ) t2
        ON t1.park_name = t2.park_name
        AND t1.ride_name = t2.ride_name
        AND t1.ctid = t2.max_ctid
        '''
        
        data = pd.read_sql(query, engine)
        
        return data
    except Exception as e:
        st.error(f'Error: {e}')
        return None


park_data = db_connect()

st.title("Theme Park Infomation 🎢")

park = {
    'Thorpe Park': 'https://www.attractionsnearme.co.uk/wp-content/uploads/2023/08/Thorpe-Park-Old-logo.png',
    'Alton Towers': 'https://www.altontowers.com/media/xambm1gp/at_together.jpg',
    'Chessington World of Adventures': 'https://www.vouchercodes.co.uk/static/v10/images/merchant/horizontal-logo/chessington_ffffff_202402140858563935.png',
    'Legoland Windsor': 'https://upload.wikimedia.org/wikipedia/de/thumb/e/ec/Legoland_Windsor_Logo.svg/2560px-Legoland_Windsor_Logo.svg.png',
    'Blackpool Pleasure Beach': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtI5UT74rOtdUxhfMrI5QAmZk8x8lReIMuvQ&s'
}

if park_data is not None:
    # Filter data for the specific parks
    filtered_parks_data = park_data[park_data['park_name'].isin(park)]
    
    if not filtered_parks_data.empty:
        # Add a selectbox widget for theme park selection
        selected_park = st.selectbox('Choose a theme park:', park)
        
        # Filter data based on the selected theme park
        if selected_park:
            st.image(park[selected_park], use_column_width=True)
            selected_park_data = filtered_parks_data[filtered_parks_data['park_name'] == selected_park]
            
            # Display the filtered data
            st.write(f'Latest data for {selected_park}:')
            st.dataframe(selected_park_data[['ride_name', 'ride_status', 'wait_time']])
            
            # Add a selectbox widget for ride selection
            ride_names = selected_park_data['ride_name'].unique()
            selected_ride = st.selectbox('Choose a ride:', ride_names)
            
            # Filter data based on the selected ride
            if selected_ride:
                selected_ride_data = selected_park_data[selected_park_data['ride_name'] == selected_ride]
                
                # Display the filtered data for the selected ride
                st.write(f'Latest data for ride {selected_ride} in {selected_park}:')
                st.dataframe(selected_ride_data[['ride_name', 'ride_status', 'wait_time']])
    else:
        st.error('No data available for the selected parks.')
else:
    st.error('Failed to load data from the database.')

def get_color(wait_time):
                if wait_time < 30.0:
                    return 'green'
                elif wait_time > 50.0:
                    return 'red'
                else:
                    return 'yellow'


open_rides = selected_park_data[selected_park_data['ride_status'] == 'open']

colors = open_rides['wait_time'].apply(get_color)

fig, ax = plt.subplots()
bars = ax.bar(open_rides['ride_name'], open_rides['wait_time'], color=colors)
ax.set_xlabel('Ride Name')
ax.set_ylabel('Wait Time (minutes)')
ax.set_title(f'Wait Times for Open Rides at {selected_park}')
ax.set_xticks(range(len(open_rides['ride_name'])))
ax.set_xticklabels(open_rides['ride_name'], rotation=90, ha='right')

# Apply colors to bars
for bar, color in zip(bars, colors):
    bar.set_color(color)


st.pyplot(fig)


st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p>Powered by <a href="https://queue-times.com/" target="_blank">Queue-Times.com</a></p>
    </div>
    """,
    unsafe_allow_html=True
)



