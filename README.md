Theme Park Information 

Theme Park Wait Times is a data feed containing the wait time of rides in different theme parks around the world. Queue Times offers an interface providing access to live waiting time data for over 80 amusement parks. 

This project aims to create an automated system to dynamically fetch the waiting time as they update to create a database of the waiting time. This data will then be visualised to show the different theme parks and different rides, and enable users to see the waiting time for that specific ride.

Part One

theme_park1.py requests the current wait times of differnt rides in differnt theme parks around the world, from the Theme Park Wait Times API. It then stores information (such as the theme park, ride name, wait time and status) in the student.park_db table.

theme_park1.py sits on the job server, running on a CRON schedule that executes it every hour.

Part Two

The Streamlit application reads from the database and displays the latest wait time of each rides in the selected theme park.
