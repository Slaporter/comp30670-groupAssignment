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
print(response.json())

DB_NAME = 'dbbikes'

TABLES = {}
TABLES['static_data'] = (
    "CREATE TABLE `static_data` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `number` int(11) NOT NULL,"
    "  `contract_name` varchar(14) NOT NULL,"
    "  `name` varchar(16) NOT NULL,"
    "  `address` varchar(14) NOT NULL,"
    "  `lat` double NOT NULL,"
    "  `lng` double NOT NULL,"
    "  `banking` varchar(14),"
    "  `bonus` varchar(14),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['dynamic_data'] = (
    "CREATE TABLE `dynamic_data` ("
    "  `id` int(11) NOT NULL,"
    "  `status` enum('CLOSED','OPEN') NOT NULL,"
    "  `bike_stands` int(11) NOT NULL,"
    "  `available_bike_stands` int(11) NOT NULL,"
    "  `available_bikes` int(11) NOT NULL,"
    "  `last_update` datetime NOT NULL,"
    "  PRIMARY KEY (`id`)"
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



cursor.close()
cnx.close()
