import requests
import json
import urllib3
import get_servers
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
	
	systemData = system.json()
	storageData = storage.json()
	
	print ("System {}:".format(systemData[u'SKU']))
	
	print ("\nMemory Summary\nHealth status: {}".format(systemData[u'MemorySummary'][u'Status'][u'Health']))
	
	print ("\nProcessor Summary\nHealth status: {}".format(systemData[u'ProcessorSummary'][u'Status'][u'Health']))
	
	print ("\nSystem\nHealth status: {}".format(systemData[u'Status'][u'Health']))