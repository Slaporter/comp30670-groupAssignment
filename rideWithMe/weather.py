
import requests
import json
import mysql.connector
from mysql.connector import errorcode
import time



api_url="http://api.openweathermap.org/data/2.5/weather?APPID=52b3fcc8ca94382baa1747a7dde59108&q=Dublin"


response = requests.get(api_url)

# Print the status code of the response.
#print(response)
print(response.json())
json_data=response.json()

DB_NAME = 'dbbikes'

TABLES = {}

TABLES['weather_data1'] = (
    
    "CREATE TABLE `weather_data1` ("
    "  `id` int(11) NOT NULL,"
    "  `temp` int(11) NOT NULL,"
    "  `main` varchar(16) NOT NULL,"    
    "  `description` varchar(16) NOT NULL,"
    "  `clouds` float(11) NOT NULL,"
    "  `humidity` float(11) NOT NULL,"
    "  `wind` float(11) NOT NULL,"
    "  `icon` varchar(16) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    
    ")ENGINE=InnoDB")

def run():
    while True:
        try:
            api_url="http://api.openweathermap.org/data/2.5/weather?APPID=52b3fcc8ca94382baa1747a7dde59108&q=Dublin"


            response = requests.get(api_url)
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
                                    "(id, temp, main, description, clouds, humidity, wind, icon)"
                                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")



            cursor.execute("SELECT `id` from `weather_data1`")
            entries = [row[0] for row in cursor.fetchall()]
            print('entries are', entries)
            info = json_data['weather'][0]
            temp = json_data['main']['temp']
            wind = json_data['wind']
            clouds = json_data['clouds']
            humidity = json_data['main']['humidity']
            id9 = info['id']
            print('id9', id9)         
            
            if id9 not in entries:
                data_weather1 = (id9, temp , info['main'], info['description'], clouds['all'], humidity, wind['speed'], info['icon']) 
                cursor.execute(insert_weather_data1, data_weather1)

            cnx.commit()
            cursor.close()
            cnx.close()

            time.sleep(5*60)


        except:
            print("Error connecting to database")
    return

run()