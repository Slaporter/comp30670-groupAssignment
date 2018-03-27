'''
Created on 14 Mar 2018

@author: Slaporter
'''
import requests
import json
import mysql.connector
from mysql.connector import errorcode


api_key = '9057d925a716282b0a6b224cc84b50a713c22a7e'
api_url="https://api.jcdecaux.com/vls/v1/stations"
response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey="+api_key)

# Print the status code of the response.
print(response)
json_data=response.json()
print("number of stops:", len(json_data))

DB_NAME = 'dbbikes'

TABLES = {}
TABLES['static_data'] = (
    "CREATE TABLE `static_data` ("
    "  `number` int(11) NOT NULL,"
    "  `contract_name` varchar(14) NOT NULL,"
    "  `name` varchar(16) NOT NULL,"
    "  `address` varchar(14) NOT NULL,"
    "  `lat` double NOT NULL,"
    "  `lng` double NOT NULL,"
    "  `banking` varchar(14),"
    "  `bonus` varchar(14),"
    "  PRIMARY KEY (`number`)"
    ") ENGINE=InnoDB")

TABLES['dynamic_data'] = (
    "CREATE TABLE `dynamic_data` ("
    "  `number` int(11) NOT NULL,"
    "  `status` enum('CLOSED','OPEN') NOT NULL,"
    "  `bike_stands` int(11) NOT NULL,"
    "  `available_bike_stands` int(11) NOT NULL,"
    "  `available_bikes` int(11) NOT NULL,"
    "  `last_update` bigint(20) NOT NULL,"
    "  PRIMARY KEY (`number`,`last_update`)"
    ") ENGINE=InnoDB")

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

add_static_data=("INSERT INTO static_data "
                "(number, contract_name, name, address, lat, lng, banking, bonus)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

add_dynamic_data=("INSERT INTO dynamic_data "
                  "(number, status, bike_stands, available_bike_stands, available_bikes,last_update)"
                  "VALUES(%s,%s,%s,%s,%s,%s)")

cursor.execute("SELECT `number` from `static_data`")
ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT `number`, `last_update` from `dynamic_data`")
d_ids = [row for row in cursor.fetchall()]

for stop in json_data:
    if stop['number'] not in ids:
        values=(stop['number'], stop['contract_name'], stop['name'], stop['address'], stop['position']['lat'], stop['position']['lng'], stop['banking'], stop['bonus'])
        cursor.execute(add_static_data, values)
    if (stop['number'], stop['last_update']) not in d_ids:
        dvalues=(stop['number'],stop['status'],stop['bike_stands'],stop['available_bike_stands'],stop['available_bikes'],stop['last_update'])
        cursor.execute(add_dynamic_data, dvalues)

cnx.commit()
cursor.close()
cnx.close()
