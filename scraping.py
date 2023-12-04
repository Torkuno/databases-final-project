import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import mysql.connector


# MongoDB connection details
mongo_url = "mongodb://localhost:27017/"  # Replace with your MongoDB connection string
db_name = "ProjectDB"  # Replace with your database name
collection_name = "events"  # Replace with your collection name

# Initialize MongoDB client
client = MongoClient(mongo_url)
db = client['ProjectDB']
collection = db['events']



# MySQL connection details
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "Miskinho_77"  # Replace with personal MySQL password
mysql_db = "projectdb"

# Establishing a connection to the MySQL database
conn = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_db
)


cursor = conn.cursor()
# URL of the website you want to scrape
url = 'https://www.fourvenues.com/en/discotecas-madrid/events?date=2023-12'

# Make an HTTP GET request to the website
response = requests.get(url)

# Initialize an empty list to store events
events = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract event details
    for event_div in soup.find_all("div", class_="relative flex transition-all duration-300 hover:shadow-lg shadow-white cursor-pointer bg-gray-100 dark:bg-gray-800 hover:bg-white/70 hover:dark:bg-gray-700/70 rounded-lg overflow-hidden mt-3 cursor-pointer"):
        # Extracting event name, date, time, and location
        event_name = event_div.find("p", class_="mt-1 sm:mt-3 font-semibold text-xl sm:text-2xl text-black dark:text-white sm:w-full sm:text-clip").get_text(strip=True)
        date_div = event_div.find("div", class_="subtitle badge rounded text-xs sm:text-sm bg-secondary text-white p-1 sm:px-2")
        event_date = " ".join(date_div.stripped_strings)
        time_div = event_div.find("div", class_="subtitle text-xs sm:text-sm")
        event_time = time_div.get_text(strip=True)
        location_div = event_div.find("div", class_="mt-1 badge rounded text-xs sm:text-sm bg-blue-200/30 dark:bg-blue-700/30 text-blue-600 dark:text-blue-100/50 p-1 px-2 whitespace-nowrap")
        event_location = location_div.get_text(strip=True).replace("\uf3c5", "")  # Removing icon character
        image_div = soup.find('div', style=lambda value: value and 'background-image' in value)
        image_url = None
        if image_div:
            style = image_div['style']
            # Extract the URL from the style string
            start = style.find("url('") + 5
            end = style.find("')", start)
            image_url = style[start:end]
        # Insert data into MySQL
        query = "INSERT INTO events (name, date, start_time, end_time, location, image_url) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (event_name, event_date, event_time[:5], event_time[5:], event_location, image_url)
        cursor.execute(query, values)
        #Adding event details to the list
        events.append({
            "name": event_name,
            "date": event_date,
            "start_time": event_time[:5],
            "end_time": event_time[5:],
            "location": event_location,
            "image": image_url
        })
    conn.commit()
    # Insert events into MongoDB

    if events:
        collection.insert_many(events)
        print("Events inserted into MongoDB")
    else:
        print("No events to insert")


else:
    print("Failed to retrieve the website")

cursor.close()
conn.close()