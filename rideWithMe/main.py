'''
Created on 14 Mar 2018

@author: Slaporter
'''
import requests
import json

api_key = '9057d925a716282b0a6b224cc84b50a713c22a7e'
api_url="https://api.jcdecaux.com/vls/v1/stations"
response = requests.get("https://api.jcdecaux.com/vls/v1/stations?&apiKey="+api_key)

# Print the status code of the response.
print(response.status_code)


headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_key)}
def get_account_info():

    api_url_base = '{0}account'.format(api_url)

    response = requests.get(api_url_base, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
account_info = get_account_info()

if account_info is not None:
    print("Here's your info: ")
    for k, v in account_info['account'].items():
        print('{0}:{1}'.format(k, v))

else:
    print('[!] Request Failed')