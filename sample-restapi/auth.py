import requests
requests.packages.urllib3.disable_warnings()
import json
from pprint import pprint

auth_url = "https://192.168.250.4:8000/login"
url = "https://192.168.250.4:8000/"

#Authenticate
auth_payload = {
		'username': 'saltuser', 
		'password': 'password',
		'eauth': 'pam'
	  	}

auth_headers = {'Accept': 'application/json'}

response = requests.post(auth_url, data=auth_payload, verify=False, headers=auth_headers)
json_data = json.loads(response.text)

#Get token
token = json_data['return'][0]['token']
token_headers = { 'Accept': 'application/x-yaml',
		  'X-Auth-Token' : token
		}

payload = {	'client': 'local',
		'tgt':'*',
		'fun':'cmd.run',
		'arg':'echo "hi salt" >> /root/test.log'
	  }
#response = requests.post(url, headers=token_headers, data=payload, verify=False)

message = {"message":"{'item1':'item1', 'item2':'item2' }"}
response = requests.post(url+'hook/my/event', headers=token_headers, data=message, verify=False)

print response.content
