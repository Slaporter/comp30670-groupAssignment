'''
Created on 14 Mar 2018

@author: Slaporter
'''
from flask import render_template
from app import app
import mysql.connector

@app.route('/')
def index():
    con=mysql.connector.connect(user='dbikes', password='dublinbikes', host='dbikes.c8m1rhzxgoap.us-east-2.rds.amazonaws.com', database='dbikes', )
    cursor=con.cursor()
    cursor.execute("SELECT `lat`, `lng`, `name`, `status`, `available_bike_stands`, `available_bikes`, `last_update` from `current_data`")
    stops=cursor.fetchall()
    returnDict = {}
    returnDict['stops']=stops
    return render_template("index.html",**returnDict)


@app.route('/weather')
def weather():
    returnDict = {}
    return render_template("weather.html",**returnDict)


@app.route('/charts')
def charts():
    con=mysql.connector.connect(user='dbikes', password='dublinbikes', host='dbikes.c8m1rhzxgoap.us-east-2.rds.amazonaws.com', database='dbikes', )
    cursor=con.cursor()
    cursor.execute("SELECT `lat`, `lng`, `name`, `status`, `available_bike_stands`, `available_bikes`, `last_update` from `current_data`")
    infos=cursor.fetchall()
    returnDict = {}
    returnDict['infos']=infos
    return render_template("charts.html",**returnDict)

@app.route('/directions')
def directions():
    con=mysql.connector.connect(user='dbikes', password='dublinbikes', host='dbikes.c8m1rhzxgoap.us-east-2.rds.amazonaws.com', database='dbikes', )
    cursor=con.cursor()
    cursor.execute("SELECT `lat`, `lng`, `name`, `status`, `available_bike_stands`, `available_bikes`, `last_update` from `current_data`")
    infos=cursor.fetchall()
    returnDict = {}
    returnDict['infos']=infos
    return render_template("directions.html",**returnDict)
