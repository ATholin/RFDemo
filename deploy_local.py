import requests
import json
import sys
import re
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)
import get_servers

from datetime import datetime

servers = []

get_servers.get(servers)
get_servers.printServers(servers)

idrac_ip = input("iDRAC IP: ")
idrac_username = input("iDRAC username: ")
idrac_password = input("iDRAC password: ")
file = sys.argv[1]
f=open(file,"r")

url = 'https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager.ImportSystemConfiguration' % idrac_ip

payload = {"ShutdownType":"Forced","ShareParameters":{"Target":"All","IPAddress":"192.168.1.121","ShareName":"share","ShareType":"CIFS","FileName":file,"UserName":"test","Password":"test"}}
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=(idrac_username,idrac_password))

d=str(response.__dict__)

try:
	z=re.search("JID_.+?,",d).group()
	
except:
	print (response)
	print ("\n- FAIL: detailed error message: {0}".format(response.__dict__['_content']))
	sys.exit()
	
job_id=re.sub("[,']","",z)

if response.status_code != 202:
	print ("\n- FAIL, status code not 202\n, code is: %s" % response.status_code)
	sys.exit()
	
else:
	print ("\n- %s successfully created for ImportSystemConfiguration method\n" % (job_id))
	
response_output=response.__dict__
job_id=response_output["headers"]["Location"]
job_id=re.search("JID_.+",job_id).group()
start_time=datetime.now()

while True:
	req = requests.get('https://%s/redfish/v1/TaskService/Tasks/%s' % (idrac_ip, job_id), auth=(idrac_username, idrac_password), verify=False)
	statusCode = req.status_code
	data = req.json()
	message_string=data[u"Messages"]
	final_message_string=str(message_string)
	current_time=(datetime.now()-start_time)
	
	if statusCode == 202 or statusCode == 200:
		print ("\n- Query job ID command passed")
		time.sleep(10)
	else:
		print ("Query job ID command failed, error code is: %s" % statusCode)
		sys.exit()
		
	if "failed" in final_message_string or "completed with errors" in final_message_string or "Not one" in final_message_string or "Unable" in final_message_string:
		print ("\n- FAIL, detailed job message is: %s" % data[u"Messages"])
		sys.exit()
		
	elif "Successfully imported" in final_message_string or "completed with errors" in final_message_string or "Successfully imported" in final_message_string:
		print ("- Job ID = "+data[u"Id"])
		print ("- Name = "+data[u"Name"])
		try:
			print ("- Message = "+message_string[0][u"Message"])
		except:
			print ("- Message = %s" % message_string[len(message_string)-1][u"Message"])
		print ("\n- %s completed in: %s" % (job_id, str(current_time)[0:7]))
		sys.exit()
	elif "No changes" in final_message_string:
		print ("- Job ID = "+data[u"Id"])
		print ("- Name = "+data[u"Name"])
		try:
			print ("- Message = "+message_string[0][u"Message"])
		except:
			print ("- Message = %s" % message_string[len(message_string)-1][u"Message"])
		print ("\n- %s completed in: %s" % (job_id, str(current_time)[0:7]))
		sys.exit()
	else:
		print ("- Job not marked completed, current status is: %s" % data[u"TaskState"])
		print ("- Message: %s\n" % message_string[0][u"Message"])
		time.sleep(1)
		continue 
		
data = req.json()
print ("Job ID = "+data[u"Id"])
print ("Name = "+data[u"Name"])
print ("Message = "+data[u"Messages"])
print ("JobStatus = "+data[u"TaskState"])