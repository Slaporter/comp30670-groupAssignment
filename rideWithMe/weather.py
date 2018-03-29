
import requests
import json
import mysql.connector
from mysql.connector import errorcode



api_url="http://api.openweathermap.org/data/2.5/weather?APPID=52b3fcc8ca94382baa1747a7dde59108&q=Dublin"


response = requests.get(api_url)

# Print the status code of the response.
print(response)
print(response.json())
json_data=response.json()

DB_NAME = 'dbbikes'

TABLES = {}

TABLES['weather_data1'] = (
    
    "CREATE TABLE `weather_data1` ("
    "  `id` int(11) NOT NULL,"
    "  `temp` int(11) NOT NULL,"
    "  `humidity` int(11) NOT NULL,"
    "  `clouds` int(11) NOT NULL,"
    "  `wind` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    
    ")ENGINE=InnoDB")


cnx=mysql.connector.connect(user='dbikes', password='dublinbikes', host='dbikes.c8m1rhzxgoap.us-east-2.rds.amazonaws.com', database='dbikes', )

cursor=cnx.cursor()
for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

insert_weather_data1 = ( "INSERT INTO weather_data1 "
                        "(id, temp, humidity, clouds, wind)"
                       "VALUES(%d,%d,%d,%d,%d,%d)")

cursor.execute("SELECT `id` from `weather_data1`")
ids = [row[0] for row in cursor.fetchall()]
print("fetching weather data")

for day in json_data:
        values=(day['id'], day['temp'], day['name'], day['humidity'], day['clouds'], day['wind'])
cursor.execute(add_weather_data1, values)

cnx.commit()
cursor.close()
cnx.close()

