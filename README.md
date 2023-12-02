<!--------------------- Table of Contents ------------------->
## Table Of Contents
- [1. Django configurations](#1.-Django-configurations)
    - [Setting up our Django Web-App](#Setting-up-our-Django-Web-App)
    - [Configure Database Settings for the Django Web-App](#Configure-Database-Settings-for-the-Django-Web-App)
        - [Configure Database Settings for MySQL database](#Configure-Database-Settings-for-MySQL-database)
    - [Propagating Data Base Configurations and Runing the App](#Propagating-Data-Base-Configurations-and-Runing-the-App)
- [2. Web-Scraping](#2.-Web-Scraping)
    - [Prerequisites](#Prerequisites)
    - [Explanation of scraping.py](#scraping-file)
        - [Setting the target url](#Setting-the-target-url)
        - [Making a request to the website](#Making-a-request-to-the-website)
        - [Initializing an Empty List for Events](#Initializing-an-Empty-List-for-Events)
        - [Checking the Request Status](#Checking-the-Request-Status)
        - [Parsing HTML Content with BeautifulSoup](#Parsing-HTML-Content-with-BeautifulSoup)
        - [Extracting Event Details](#Extracting-Event-Details)
        - [Extracting Event Information](#Extracting-Event-Information)
        - [Fidning the image](#Fidning-the-image)
        - [Adding Event Details to the List](#Adding-Event-Details-to-the-List)
        - [Saving Events to a JSON File](#Saving-Events-to-a-JSON-File)
        - [Request Failure](#Request-Failure)
- [3. Project Members](#3.-Project-Members)


<!--------------------- Django Web-App  --------------------->
# 1. Django configurations
## Setting up our Django Web-App
Creating **virtual environment** to isolates dependencies, ensuring compatibility and conflict-free development.
```
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```
configuring **virtual environment** to hoset our Django Web-App.
```
pip install wheel
pip install django
pip install mysqlclient
```
Creating a new **Django** project.
```
django-admin startproject madridevents
```

## Configure Database Settings for the Django Web-App
We decided to do the MySQL and Django migrations in separate Python files (MySQL in manage.py and MongoDB in manage_Mongo.py) this was done in order for us to integrate the MySQL Database seamlessly with Django's ORM(Object-Relational Mapping) and have more flexibility with the management and configuration of the MongoDB Database.

### Configure Database Settings for MySQL database 

[manage.py](https://github.com/Torkuno/databases-final-project/blob/main/manage.py)


## Propagating Data Base Configurations and Runing the App
Applying our database schema changes (manage.py) in order to synchronize the database with the current state of models and schemas.
```
python manage.py migrate
```

Createing a new application named 'madridevents' within our Django project
```
python manage.py startapp madridevents
```

Running the Django Web-App (http://127.0.0.1:8000/admin/)
```
python manage.py runserver
```




<!-------------------- WEB-Scraping ------------------------->
# 2. Web-Scraping
## Prerequisites
This project's execution requres **BeautifulSoup4** and **requests**. You can install them using
```
pip install beautifulsoup4 requests
```

## Explanation of [scraping.py](https://github.com/Torkuno/databases-final-project/blob/main/scraping.py)<a name = "scraping file"></a>
### Setting the target url
This line defines the target URL, which is the webpage containing the events that the script is looking for.
```
url = 'https://www.fourvenues.com/en/discotecas-madrid/events?date=2023-12'
```

### Making a request to the website
We use the `requests.get` method to make a GET request to the specified URL and store the response in the response variable.
```
response = requests.get(url)
```

### Initializing an Empty List for Events
We create an empty list called events to store the details of the scraped events.
```
events = []
```

### Checking the Request Status
The script checks if the HTTP request was successful by verifying that the status code is 200. If we do not get status code 200, the script abort the procedure.
```
if response.status_code == 200:
```

### Parsing HTML Content with BeautifulSoup
We create a BeautifulSoup object to parse the HTML content of the webpage using the `html.parser` parser.
```
soup = BeautifulSoup(response.content, 'html.parser')
```

### Extracting Event Details
The script uses a loop to iterate through HTML elements containing event details. The details include the event name, date, time, and location.
```
for event_div in soup.find_all("div", class_="relative ..."):
```

### Extracting Event Information
The script extracts specific details such as event name, date, time, location, and image reference from the HTML elements.

Some elements, like the date, time, and location, require us to find another div element before obtaining the data that we want.
```
    event_name = event_div.find("p", class_="mt-1 ...").get_text(strip=True)
    date_div = event_div.find("div", class_="subtitle badge ...")
    event_date = " ".join(date_div.stripped_strings)
    time_div = event_div.find("div", class_="subtitle ...")
    event_time = time_div.get_text(strip=True)
    location_div = event_div.find("div", class_="mt-1 ...")
    event_location = location_div.get_text(strip=True).replace("\uf3c5", "")
    image_div = soup.find('div', style=lambda value: value and 'background-image' in value)
    image_url = None
```

### Fidning the image
This block checks if an image was found, and generates a clean URL string.
```
    if image_div:
        style = image_div['style']
        start = style.find("url('") + 5
        end = style.find("')", start)
        image_url = style[start:end]
```

### Adding Event Details to the List
The script appends the extracted event details to the events list in the form of a dictionary.
```
events.append({
    "name": event_name,
    "date": event_date,
    "start_time": event_time[:5],
    "end_time": event_time[5:],
    "location": event_location,
    "image": image_url
})
```

### Saving Events to a JSON File
If the request was successful, the script saves the list of events to a JSON file named 'events.json' with an indentation of 4 spaces per level.
```
with open('events.json', 'w') as file:
    json.dump(events, file, indent=4)
```

### Request Failure
If the HTTP request was not successful, giving us a status code not equal to 200, the script prints an error message indicating that the website retrieval failed.
```
else:
    print("Failed to retrieve the website")
```


# 3. Project Members
All the collabroaors in this repositories are group members.

- [Shahaf Brenner](https://github.com/shahafbr)
- [Larbi Benamour](https://github.com/Larbibenamour)
- [Juan Diego Fernandez](https://github.com/juandifers)
- [Tomas Mesalles](https://github.com/Torkuno)
- [Sergio Verdugo](https://github.com/Svrubio7)