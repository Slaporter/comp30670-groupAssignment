'''
Created on 14 Mar 2018

@author: Slaporter
'''
from flask import render_template, request
from app import app
import sys
import mysql.connector
import string
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
import scipy
from calendar import day_abbr


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


@app.route('/prediction')
def prediction():
    returnDict={}
    path=request.url
    if "day" in path:
        day= request.args.get('day')
        time= request.args.get('time')
        stopnumber = request.args.get('stopnumber')
        temp=request.args.get('temp')
    
        clf = pickle.load(open('models/stop'+str(int(stopnumber))+'.pkl', 'rb'))
        returnDict['prediction']=int(clf.predict(pd.DataFrame({'hour':[time], 'weekday':[day], 'visibility':[90],'windspeed':[28],'temp':[temp],'humidity':[0.56]}))[0])
        returnDict['day']=day
        returnDict['time']=time
        if int(stopnumber)<20:
            returnDict['stopnumber']=int(stopnumber)-1
        else:
            returnDict['stopnumber']=int(stopnumber)-2
    con=mysql.connector.connect(user='dbikes', password='dublinbikes', host='dbikes.c8m1rhzxgoap.us-east-2.rds.amazonaws.com', database='dbikes', )
    cursor=con.cursor()
    cursor.execute("SELECT `lat`, `lng`, `name`, `number`, `status`, `available_bike_stands`, `available_bikes`, `last_update` from `current_data`")
    infos=cursor.fetchall()
    returnDict['infos']=infos
    return render_template("prediction.html",**returnDict)


    
@app.route('/directions')
def directions():
    con=mysql.connector.connect(user='dbikes', password='dublinbikes', host='dbikes.c8m1rhzxgoap.us-east-2.rds.amazonaws.com', database='dbikes', )
    cursor=con.cursor()
    cursor.execute("SELECT `lat`, `lng`, `name`, `status`, `available_bike_stands`, `available_bikes`, `last_update` from `current_data`")
    infos=cursor.fetchall()
    returnDict = {}
    returnDict['infos']=infos
    return render_template("directions.html",**returnDict)
