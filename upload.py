from boxsdk import Client, JWTAuth
from boxsdk import OAuth2
import os
from pathlib import Path
import json
import requests
import urllib
import urllib2
from urllib import urlopen
import re
import schedule
import time
import datetime

def pull():
	# initialize paths for config file
	private_path = Path(__file__).resolve().parent
	config_path = private_path / "config.json"
	key_path = private_path/"private.pem"
	print('keypath = ' + str(key_path))
	print('config = ' + str(config_path))
	print('private = ' + str(private_path))

	with config_path.open() as f:
	    config = json.load(f)

	# initialize client variables from config tokens
	client_id = config["clientID"]
	client_secret = config["clientSecret"]
	enterprise_id = config["enterpriseID"]

	# initialize a new client
	auth = JWTAuth(client_id=client_id,
			client_secret=client_secret,
			enterprise_id=enterprise_id,
			jwt_key_id='0l74oi4p',
			rsa_private_key_file_sys_path="private.pem")

	access_token = auth.authenticate_instance()
	client = Client(auth)

	me = client.user(user_id='me').get()

	folderId = config["folderId"]						# id of box folder to sync with

	# returns a list of all items inside box folder
	itemsToSync = client.folder(folder_id=folderId).get_items(limit=100, offset=0)

	# create a list of file names to parse and id number to identify and pull data
	nameList = []
	idList = []

	# counter variables
	i = 0
	while i < len(itemsToSync):
		s = str(itemsToSync[i])
		name = str(re.search('\(([^)]+)', s).group(1))
		idNum = re.findall(r'\d{12}', s)							# finds string of 12 digits as file id number

		# only searches for .png types
		# saves name and id number to separate lists
		if name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
			idList.append(idNum)
			nameList.append(name)
		else:
			pass
		i += 1

	j = 0
	destinationPath = config["destinationPath"]						# path files will be saved to
	timelogPath = config["timelogPath"]
	now = datetime.datetime.now()									# get current timestamp
	strNow = now.strftime("%Y-%m-%d %H:%M:%S")
	while j < len(nameList):
		print nameList[j]
		print idList[j]
		completeName = os.path.join(destinationPath, nameList[j])	# concatenates destination with name of file
		idNum = ''.join(idList[j])									# parses id number to be pulled from box folder
		filecontent = client.file(file_id=idNum).content()			# saves file content as variable
		newfile = open(completeName,'w')						
		newfile.write(filecontent)
		newfile.close()
		j += 1
	with open(timelogPath,"a") as f:								# logs sync date and time in timelog.txt
		f.write("Last box sync at " + strNow + "\n")

schedule.every(5).seconds.do(pull)

while 1:
    schedule.run_pending()
    time.sleep(1)
