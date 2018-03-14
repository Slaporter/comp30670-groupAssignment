'''
Created on 14 Mar 2018

@author: Slaporter
'''
import requests
import json




api_key = '9057d925a716282b0a6b224cc84b50a713c22a7e'
api_url="https://api.jcdecaux.com/vls/v1/stations"
response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey="+api_key)

# Print the status code of the response.
print(response)
print(response.json())
