#!/usr/bin/python3

import sys
import getopt
import requests
from multiprocessing.dummy import Pool as ThreadPool


hostslist = []  # List of hostnames.
robotsDis = []  # List of robots.txt disallowed URLs.
robotsAllw = []  # List of robots.txt allowed URLs.


def getrobotstxt(hostname):

    global robotsAllw, robotsDis

    global hostsConnN
    global hostsConnErrorN, hostsConnTimeOutN, hostsReadTimeOutN
    global hostsNoRobotsN, hostsInvalidURL

    global agent

    for port in portslist:
        print("[*] Requesting robots.txt: {}".format(hostname))

        if agent == "":
            agent = "Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101" \
                    " Firefox/56.0"

        URL = "http://" + hostname + ":" + port + "/robots.txt"

        try:
            r = requests.get(URL,
                             timeout=10,
                             allow_redirects=True,
                             verify=False,
                             headers={'User-Agent': agent}
                             )
        except requests.exceptions.ConnectionError:
            hostsConnErrorN += 1
            return -1
        except requests.exceptions.ConnectTimeout:
            hostsConnTimeOutN += 1
            return -1
        except requests.exceptions.InvalidURL:
            hostsInvalidURL += 1
            return -1
        except requests.exceptions.ReadTimeout:
            hostsReadTimeOutN += 1
            return -1

        code = r.status_code
        text = r.text

        # If 200 status code, parse robots.txt and create list as URLs.
        if int(code) == 200:
            hostsConnN += 1
            textstring = text.splitlines()

            for line in textstring:
                if line[:9] == "Disallow:":
                    robotsDis += [hostname + line[10:]]
                if line[:6] == "Allow:":
                    robotsAllw += [hostname + line[7:]]
        else:
            hostsNoRobotsN += 1


opts, args = getopt.getopt(sys.argv[1:], "o:p:i:t:a:h")

ports = "80"
tN = 16
ifile = ""
agent = ""
for opt, arg in opts:
    # input filename of hosts or IPs
    if opt == "-o":
        ofile = arg
    if opt == "-p":
        ports = arg
    if opt == "-i":
        ifile = arg
    if opt == "-t":
        tN = int(arg)
    if opt == "-a":
        agent = arg
    if opt == "-h":
        print("Usage: %s -i input file of hosts <-o output file base "
              "-p list of ports -t number of threads> -a user-agent"
              % sys.argv[0])

if ifile == "":
    print("[!] Argument for input files required. Exiting...")
    sys.exit()

with open(ifile) as f:
    hostfile = f.read().splitlines()

hostsN = len(hostfile)  # Number of hosts provided.
hostsConnN = 0  # Number of hosts which make connections.
hostsConnErrorN = 0  # Number of hosts with connection errors (hostname not found).
hostsConnTimeOutN = 0  # Number of hosts with connect timeout.
hostsReadTimeOutN = 0  # Number of hosts with read timeout.
hostsNoRobotsN = 0  # Number of hosts which have no robots.txt.
hostsInvalidURL = 0  # Number of hosts with invalid URL.
countN = 0
gotURLs = []

# Parse and validate list of ports.
portslist = ports.split(",")
if all([port.isdigit() for port in portslist]):
    pass
else:
    raise ValueError("[!] Invalid port numbers in argument.")


# Retrieve robots.txt data.
pool = ThreadPool(tN)
polresult = pool.map(getrobotstxt, hostfile)
pool.close()
pool.join()

robotsDis.sort()
robotsAllw.sort()
gotURLs.sort()
hostfile.sort()

# Write output file if desired.
if 'ofile' in locals():
    with open(ofile + "_disallowed.txt", "w") as outfile:
        for entry in robotsDis:
            outfile.write(entry+"\n")
    with open(ofile + "_allowed.txt", "w") as outfile:
        for entry in robotsAllw:
            outfile.write(entry+"\n")
else:
    print("======================================")
    print("Robots.txt disallowed:")
    for URL in hostfile:
        print(URL)
    # for robot in robotsDis:
    #    print(robotsDis)
    print("--------------------------------------")
    # print("Robots.txt allowed:")
    # for robot in robotsAllw:
    #    print(robotsAllw)
    print("Got URLs:")
    for URL in gotURLs:
        print(URL)

print("==========================================")
print("Total hosts provided: {}.".format(hostsN))
print("Total hosts connected: {}.".format(hostsConnN))
print("Total hosts connect timeout: {}.".format(hostsConnTimeOutN))
print("Total hosts read timeout: {}.".format(hostsReadTimeOutN))
print("Total hosts no robots.txt: {}.".format(hostsNoRobotsN))
print("Total hosts invalid URL: {}.".format(hostsInvalidURL))
print("CountN: {}.".format(countN))
