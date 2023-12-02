import requests
from bs4 import BeautifulSoup
import json

# URL of the website we wish to scrape
url = 'https://www.fourvenues.com/en/discotecas-madrid/events?date=2023-12'

# HTTP GET request to the website
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

        # Adding event details to the list
        events.append({
            "name": event_name,
            "date": event_date,
            "start_time": event_time[:5],
            "end_time": event_time[5:],
            "location": event_location,
            "image": image_url
        })

    # Save the events to a JSON file
    with open('events.json', 'w') as file:
        json.dump(events, file, indent=4)

else:
    print("Failed to retrieve the website")
