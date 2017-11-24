import requests
import json
import urllib3
import get_servers
import pandas
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

lines = []
servers = []

get_servers.get(servers)
get_servers.printServers(servers)

## Takes every health status, outputs on screen
for server in servers:
	print("\n"+10*"-"+"\n")
	print ("Calling server:")
	print (server)
	
	system = requests.get('https://' + server.rstrip() + '/redfish/v1/Systems/System.Embedded.1',verify=False,auth=('root','calvin'))
	storage = requests.get('https://' + server.rstrip() + '/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/RAID.Integrated.1-1',verify=False,auth=('root','calvin'))
	
	# Convert to json
	systemData = system.json()
	storageData = storage.json()
	
	# Takes every key in json
	# if that key is "Status", print the health
	# if that key is a dictionary, go through the dictionary and print health if key is "Status"
	for key in systemData:
		if (key == "Status"):
			print (key+": {}".format(systemData[u'Status'][u'Health']))
		if isinstance(systemData[key], dict):
			for statusKey in systemData[key]:
				if (statusKey == "Status"):
					print (key+": {}".format(systemData[u'Status'][u'Health']))