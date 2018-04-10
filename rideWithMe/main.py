'''
Created on 14 Mar 2018

@author: Slaporter
'''
print("preimports")
import requests
import json
print("Import pre mysql")
import mysql.connector
from mysql.connector import errorcode
import time
import datetime

print("all imports")
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

TABLES['current_data'] = (
    "CREATE TABLE `current_data` ("
    "  `number` int(11) NOT NULL,"
    "  `name` varchar(16) NOT NULL,"
    "  `lat` double NOT NULL,"
    "  `lng` double NOT NULL,"
    "  `status` enum('CLOSED','OPEN') NOT NULL,"
    "  `bike_stands` int(11) NOT NULL,"
    "  `available_bike_stands` int(11) NOT NULL,"
    "  `available_bikes` int(11) NOT NULL,"
    "  `last_update` varchar(16) NOT NULL,"
    "  PRIMARY KEY (`number`)"
    ") ENGINE=InnoDB")


def run():
    while True:
        try:
            api_key = '9057d925a716282b0a6b224cc84b50a713c22a7e'
            api_url="https://api.jcdecaux.com/vls/v1/stations"
            response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey="+api_key)
            json_data=response.json()

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
            
            print("reached")
            
            add_static_data=("INSERT INTO static_data "
                            "(number, contract_name, name, address, lat, lng, banking, bonus)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            
            add_dynamic_data=("INSERT INTO dynamic_data "
                              "(number, status, bike_stands, available_bike_stands, available_bikes,last_update)"
                              "VALUES(%s,%s,%s,%s,%s,%s)")
            
            add_current_data=("INSERT INTO current_data "
                              "(number, name, lat, lng, status, bike_stands, available_bike_stands, available_bikes, last_update)"
                              "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            
            replace_current_data=("REPLACE INTO current_data "
                                  "(number, name, lat, lng, status, bike_stands, available_bike_stands, available_bikes, last_update)"
                                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            
            
            
            print("and here")
            
            cursor.execute("SELECT `number` from `static_data`")
            ids = [row[0] for row in cursor.fetchall()]
            cursor.execute("SELECT `number`, `last_update` from `dynamic_data`")
            d_ids = [row for row in cursor.fetchall()]
            cursor.execute("SELECT `number` from `current_data`")
            c_ids = [row[0] for row in cursor.fetchall()]
            print("before for loop")
            

            
            print(json_data)
            for stop in json_data:
                s=stop['last_update']/1000
                last_update=datetime.datetime.fromtimestamp(s).strftime("%Y-%m-%d %H:%M:%S")
                print(last_update)
                if stop['number'] not in ids:
                    values=(stop['number'], stop['contract_name'], stop['name'], stop['address'], stop['position']['lat'], stop['position']['lng'], stop['banking'], stop['bonus'])
                    cursor.execute(add_static_data, values)
                if (stop['number'], stop['last_update']) not in d_ids:
                    print("in dynamic if")
                    dvalues=(stop['number'],stop['status'],stop['bike_stands'],stop['available_bike_stands'],stop['available_bikes'],stop['last_update'])
                    cursor.execute(add_dynamic_data, dvalues)
                print("out of dd")
                if stop['number'] not in c_ids:
                    print("in create")
                    cvalues=(stop['number'],stop['name'], stop['position']['lat'], stop['position']['lng'], stop['status'], stop['bike_stands'], stop['available_bike_stands'], stop['available_bikes'], last_update)
                    cursor.execute(add_current_data, cvalues)
                if stop['number'] in c_ids:
                    rvalues=(stop['number'], stop['name'], stop['position']['lat'], stop['position']['lng'], stop['status'], stop['bike_stands'], stop['available_bike_stands'], stop['available_bikes'], last_update)
                    cursor.execute(replace_current_data, rvalues)                   

            print("reached past for loop")
            cnx.commit()
            cursor.close()
            cnx.close()
            
            time.sleep(60)

        except:
            print("Error connecting to database")

    return

run()
