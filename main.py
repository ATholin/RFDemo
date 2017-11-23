import sys

try:
    import configparser
except ImportError:
    import ConfigParser

def print_menu():
    print ("1. Do an inventory")
    print ("2. Healthcheck")
    print ("3. Deploy an SCP profile")
    print ("4. Do a firmware inventory")
    print ("5. Exit")

Config = configparser.ConfigParser()
Config.read("settings.ini")
share_ip = Config.get("SETTINGS","SHARE_IP")
filename = Config.get("SETTINGS","FILENAME")

loop=True
  
## while variable 'loop' is true, keep doing it.
while loop:
	print_menu()    ## Displays menu
	choice = int(input("Enter your choice [1-5]: "))
     
	if (choice==1):
		print ("\n" + 10 * "-" + "INVENTORY" + 10 * "-")
		exec(open("./inventory.py").read())
	elif (choice==2):
		exec(open("./healthcheck.py").read())
	elif (choice==3):
		sys.argv = [Config.get("SETTINGS","SHARE_IP"), Config.get("SETTINGS","FILENAME")]
		exec(open("./deploy.py").read())
	elif (choice==4):
		print ("Choice:", choice)
	elif (choice==5):
		## ends loop, since the 'while' will be false
		loop=False