#!/usr/bin/env python
"""
Py-Komence is a simple client to test network speeds

There are two scripts:
komence-latency
komence-speed

Author: James Krause <james@thekrauses.me>

"""
import argparse, argcomplete, komencecore, json
from re import L

download_endpoints = {
    '1GB' : 'http://ipv4.download.thinkbroadband.com/1GB.zip',
    '512MB' : 'http://ipv4.download.thinkbroadband.com/512MB.zip',
    '200MB' : 'http://ipv4.download.thinkbroadband.com/200MB.zip',
    '100MB' : 'http://ipv4.download.thinkbroadband.com/100MB.zip',
    '50MB' : 'http://ipv4.download.thinkbroadband.com/50MB.zip',
    '20MB' : 'http://ipv4.download.thinkbroadband.com/20MB.zip',
    '10MB' : 'http://ipv4.download.thinkbroadband.com/10MB.zip',
    '5MB' : 'http://ipv4.download.thinkbroadband.com/5MB.zip'
}

parser = argparse.ArgumentParser()
argcomplete.autocomplete(parser)

parser.add_argument('--size', default='20MB', choices=['5MB','10MB','20MB','50MB','100MB','200MB','512MB','1GB'], help="Select the size of file you want to download. Default = 20MB")
parser.add_argument('--iterations', type=int, default=5, help="Choose the number of times you want to run the tests, default=")
parser.add_argument('--output', help="Enter a file name to write the outputs to.")

args = parser.parse_args()

results = []
iteration = 0
while iteration < args.iterations:
    results.append(komencecore.getDownSpeed(download_endpoints[args.size]))
    iteration += 1
    
jsondata = json.dumps(results,indent=6)
if args.output is not None:
    f = open(args.output, "w")
    f.write(jsondata)
    print ('Wrote results to' + args.output)
else:
    print(jsondata)
