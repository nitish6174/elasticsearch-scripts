import os
import json
import subprocess
from colorprint import *

def main():

	cprint("\nMake sure Elasticsearch is running on localhost at port 9200\n", instructionC)

	cprint("1. Export data as a snapshot files", listC)
	cprint("2. Import data from snapshot files", listC)
	cprint("Enter 1/2 : ", promptC,end="")
	mode = input()
	cprint("")

	if mode=="1":

		cprint("Make folders where you want to store the backups (One folder for each backup repository)",instructionC)
		cprint("Add path to these folders at bottom of elasticsearch.yml file like this:",instructionC)
		cprint("path.repo: [\"/path/to/dir1/\",\"/path/to/dir2/\"]\n")

		cprint("Enter name of backup repository (new backup repository will be created if not found): ",promptC)
		backup_repo_name = input()
		cprint("Give the folder path where backup for this repository is to be stored (This path must be added to elasticsearch.yml file) :",promptC)
		backup_path = input()
		cprint("Enter list of index to be backed up (Separate names with space): ",promptC)
		index_list = (input()).split()
		cprint("")

		if repositoryExists(backup_repo_name)==False:
			createRepository(backup_repo_name,backup_path)
		else:
			cprint("Specified backup repository already exists",resultC)
		cprint("")

		showRepoStatus(backup_repo_name)
		snapshot_version = findSnapshotVersion(backup_repo_name)
		snapshot_version += 1

		cprint("\nContinue to create snapshot version "+str(snapshot_version)+"? (y/n) : ", promptC, end="")
		user_reply = input()
		if user_reply=='y' or user_reply=='Y':
			snapshot_name = "snapshot_"+str(snapshot_version)
			makeSnapshot(backup_repo_name,snapshot_name,index_list)
			### To delete snapshot
			### cmd = "curl -XDELETE "+snapshot_url

	elif mode=="2":

		cprint("Enter name of repository through which data is to be imported (new repository will be created if not found):", promptC)
		backup_repo_name = input()
		cprint("Make sure the path you provide below is added in the elasticsearch.yml in this way:", instructionC)
		cprint("path.repo: [\"/path/to/dir/\"]")
		cprint("Give the folder path where backup data for this repository is stored :", promptC)
		backup_path = input()
		cprint("")

		if repositoryExists(backup_repo_name)==False:
			createRepository(backup_repo_name,backup_path)
		else:
			cprint("Specified backup repository already exists",resultC)
		cprint("")

		showRepoStatus(backup_repo_name)
		snapshot_version = findSnapshotVersion(backup_repo_name)

		cprint("Continue to restore the latest snapshot version (version "+str(snapshot_version)+") ? (y/n) : ", promptC, end="")
		user_reply = input()
		if user_reply=='y' or user_reply=='Y':
			snapshot_name = "snapshot_"+str(snapshot_version)
			restoreSnapshot(backup_repo_name,snapshot_name)



def repositoryExists(backup_repo_name):
	cprint("Checking if specified backup repository exists", flagC, bold)
	cmd = "curl -GET http://localhost:9200/_snapshot/"+backup_repo_name+"?pretty"
	snapshot_response = runCommand(cmd)[1]
	if "error" in snapshot_response:
		return False
	else:
		return True


def createRepository(backup_repo_name,backup_path):
	url = "http://localhost:9200/_snapshot/"+backup_repo_name
	settings = "{ \"type\": \"fs\", \"settings\": { \"location\": \""+backup_path+"\", \"compress\": false } }"
	cmd = "curl -XPUT '"+url+"' -d '"+settings+"'"
	cprint("Creating new backup repository: \'"+backup_repo_name+"\'", flagC, bold)
	cprint("Running this command to create it:", titleC, bold)
	cprint(cmd)
	cprint("")
	os.system(cmd)
	cprint("")

def snapshotExists(backup_repo_name,snapshot_version):
	snapshot_name = "snapshot_"+str(snapshot_version)
	snapshot_url = "http://localhost:9200/_snapshot/"+backup_repo_name+"/"+snapshot_name+"?pretty"
	cmd = "curl -GET "+snapshot_url
	snapshot_response = runCommand(cmd)[1]
	if "error" in snapshot_response:
		return False
	else:
		return True


def showRepoStatus(backup_repo_name):
	cmd = "curl -GET http://localhost:9200/_snapshot/"+backup_repo_name+"?pretty"
	snapshot_response = runCommand(cmd)[0]
	cprint("Status of repository '", resultC, end="")
	cprint(backup_repo_name, end="")
	cprint("' :", resultC)
	cprint(snapshot_response)


def findSnapshotVersion(backup_repo_name):
	snapshot_version = 1
	while snapshotExists(backup_repo_name,snapshot_version)==True:
		snapshot_version += 1
	snapshot_version -= 1
	cprint( str(snapshot_version) + " snapshot(s) already exist in this repository" , resultC)
	return snapshot_version


def makeSnapshot(backup_repo_name,snapshot_name,index_list):
	url = "http://localhost:9200/_snapshot/"+backup_repo_name+"/"+snapshot_name
	body = "{ \"indices\": \""+index_list.join(",")+"\", \"ignore_unavailable\": \"true\", \"include_global_state\": false }"
	cmd = "curl -XPUT '"+url+"' -d '"+body+"'"
	cprint("Creating snapshot with the following command :", titleC, bold)
	cprint(cmd+"\n")
	os.system(cmd)
	cprint("")


def restoreSnapshot(backup_repo_name,snapshot_name):
	url = "http://localhost:9200/_snapshot/"+backup_repo_name+"/"+snapshot_name+"/_restore"
	cmd = "curl -XPOST "+url
	cprint("Restoring snapshot with the following command :", titleC, bold)
	cprint(cmd+"\n")
	os.system(cmd)
	cprint("")


def runCommand(cmd):
	p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	try:
		output_string = out.decode("utf-8")
		output_json = json.loads(output_string)
	except:
		output_string = ""
		output_json = {}
	return [output_string,output_json]




instructionC = "blue"
listC = "red"
promptC = "yellow"
flagC = "purple"
titleC = "cyan"
resultC = "green"
bold = ["bold"]

main()