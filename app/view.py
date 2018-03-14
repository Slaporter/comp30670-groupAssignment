'''
Created on 14 Mar 2018

@author: Slaporter
'''
from flask import render_template
from app import app


@app.route('/')
def index():
    returnDict = {}
    returnDict['title']='Home'
    return render_template("index.html",**returnDict)
    