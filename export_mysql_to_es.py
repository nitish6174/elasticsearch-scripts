import os
import MySQLdb
from elasticsearch import Elasticsearch
import datetime
import json
import collections
from es_process import *
from colorprint import *

### MySql variables
db_hostname = "localhost"
db_username = "root"
db_password = "pass"
db_database = "myapp"
### Name of target index in elasticsearch
db_index = "myapp"

def main():

	### Export some tables or all tables of the database
	table_list = ['tableName1','tableName2']
	# table_list = allTables()

	### Set reset True to recreate index if present
	generateDB(table_list,reset=True)

	### Display count of inserted documents for each table to verify
	countDocuments(table_list)



def generateDB(table_list,reset=False):
	if reset==True:
		es_recreate_index(db_index)
		# setMapping()
	for table in table_list:
		exportTable(table)
	es_refresh_index(index=db_index)
	cprint("Database exported","green")


def exportTable(table_name):
	query = "SELECT * FROM "+table_name
	data = run(query)
	# data = convertDate(data)
	print("Exporting MySQL table - "+table_name+" : "+str(len(data))+" rows")
	for row in data:
		es_insert(db_index, table_name, row, False)


def allTables():
	table_list = []
	query = "SHOW TABLES"
	res = run(query)
	for row in res:
		for key in row:
			table_list.append(row[key])
	return table_list

### Use this to set some fields as date-time type
def setMapping():
	map_body = {
		"doc_type_name": {
			"properties": {
				"field1": {
					"type":   "date",
					"format": "yyyy-MM-dd"
				},
				"field2": {
					"type":   "date",
					"format": "yyyy-MM-dd"
				}
			}
		}
	}
	es.indices.put_mapping(index=db_index, doc_type="doc_type_name", body=map_body)

### Converts all strings to unicode. May be useful in case of some errors.
def convert(data):
	if isinstance(data, basestring):
		return unicode(data)
	elif isinstance(data, collections.Mapping):
		return dict(map(convert, data.iteritems()))
	elif isinstance(data, collections.Iterable):
		return type(data)(map(convert, data))
	else:
		return data

### Converts date-time type values to strings
def convertDate(data):
	for row in data:
		for key in row:
			if isinstance(row[key],datetime.date) or isinstance(row[key],datetime.timedelta):
				row[key] = str(row[key])
	return data


def tableData(table_name):
	query = "SELECT * FROM "+table_name
	cursor.execute(query)
	data = cursor.fetchall()
	columns = cursor.description
	return {'table':table_name,'columns':columns,'data':data}

### Check how many documents with doc_type same as a table name are indexed
def countDocuments(table_list):
	cprint("Showing count of inserted documents for each table:","purple")
	for table_name in table_list:
		search_query = { "filter" : { "type" : { "value" : table_name } } }
		res = es.search(index=db_index, body=search_query, filter_path=['hits.hits._type','hits.hits._source','hits.total'])
		print(table_name+":"+str(res['hits']['total'])+" documents")


def run(query):
	cursor.execute(query)
	return cursor.fetchall()


def show(res):
	print(json.dumps(res, indent=2, sort_keys=True))



db = MySQLdb.connect(db_hostname,db_username,db_password,db_database)
cursor = db.cursor(MySQLdb.cursors.DictCursor)
es = Elasticsearch()
main()
db.close()