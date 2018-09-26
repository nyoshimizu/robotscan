## Robotscan

Roboscan is a simple scanner for robots.txt. Written for Python3, uses Requests, and multithreaded for faster processing. Working but early version.

## Usage

./robotscan.py [options]

## Options

-h List options

-i Input file containing list of hosts. Required.

-o Output file; if provided, robots allowed and disallowed listings will be saved in filename_allowed.txt and filename_disallowed.txt. If not provided, they will be printed to stdout after the scan is over.

-p Comma separated list of ports to make for requests. Default is port 80. Note that Requests will follow redirects for HTTPS or for other reasons.

-t Number of threads to use. Default is 16 threads. If this is increased, it seems that Requests will have trouble keeping up and some connections are dropped. The scan will end with a listing of numbers of successful connections, connections which time out, etc. which can be used to gauge an appropriate number of threads.

-a Agent name to use when making HTTP requests. Default value is "Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0."

