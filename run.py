'''
Created on 14 Mar 2018

@author: Slaporter
'''
import os
from app import app

def run_my_bike():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_my_bike()