#!/usr/bin/env python3

import os
import requests
import argparse
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--name", help='Git repo name')
parser.add_argument("-p", "--path", help='Path to download')
args = parser.parse_args()

api_url = 'http://localhost:5000/repoDownload?{}'

def checkArgs():
	if args.path != None and args.name != None:
		return True
	else:
		return False
	return False

# Implementare output directory

if __name__ == '__main__':

	if checkArgs():
		repo = args.name
		path = args.path
		token = os.getenv('TOKEN')
		url = api_url.format('token='+token+'&repo='+repo+'&path='+path)
		response = requests.get(url)
		zip_bytes = response.content
		zip_file = open('test.zip', 'wb')
		zip_file.write(zip_bytes)
	else:
		parser.print_help()