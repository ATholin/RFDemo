def get(servers):
	## opens server file, puts all servers in array
	with open("discovery.dat","r") as discoverylist:
		for line in discoverylist:
			line = line.strip()
			if not str(line[0]) == "#":
				servers.append(line)
	discoverylist.closed
	
def printServers(servers):
	## Easier to read which servers are in list, counts them one by one
	## 1: (server ip 1)
	## 2: (server ip 2)
	print ("Servers in list:")
	count = 0
	for server in servers:
		count = count + 1
		print(str(count) + ": " + server)