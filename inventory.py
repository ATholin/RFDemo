import requests
import json
import io
import urllib3
import get_servers
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

lines = []
servers = []

get_servers.get(servers)
get_servers.printServers(servers)
	
## Exports json, appends to json files in current directory.
for server in servers:
	print()
	print ("Calling server:")
	print (server)
	system = requests.get('https://' + server.rstrip() + '/redfish/v1/Systems/System.Embedded.1',verify=False,auth=('root','calvin'))
	storage = requests.get('https://' + server.rstrip() + '/redfish/v1/Systems/System.Embedded.1/Storage/Controllers/RAID.Integrated.1-1',verify=False,auth=('root','calvin'))
	systemData = {server:[system.json()]}
	storageData = {server:[storage.json()]}
	with open("systemData.json", "a") as f:
		json.dump(systemData, f)
	with open("storageData.json", "a") as f:
		json.dump(storageData, f)