# Elasticsearch scripts
Python scripts for:
  - Taking backup and keeping version control of Elasticsearch data
  - Exporting mySQL data to elasticsearch
  - Remove fields/keys from documents
  - Functions for common tasks/queries (get all documents of a type, flatten hits array to get source etc)  

## Dependencies & modules used
  * Use python 3 to run these scripts
  * **Python elasticsearch client** : Install using ```sudo pip install elasticsearch``` or ```sudo apt-get install python-elasticsearch```
  * Other python modules (generally pre-installed) : *collections* , *json*
  
## Scripts in this project

### migrate.py
  To take backup in the form of snapshot versions, restore a snapshot version and migrate data to another machine.  
  1. Uses repository system (somewhat like git). Each repository can take backup of multiple indices.  
  2. You need to make a folder per repository on your machine to store the backup files (stored as snapshots).  
  3. Path to this folder needs to be given while running the program to export/import the data.  
  4. Use the export option in the program to make a snapshot of indices (snapshot version will auto-increment).  
  5. Once data is exported as snapshots, the import option of script can be used to restore a snapshot.  
  6. Similarly, to copy your elasticsearch data to another server, copy the backup folder (in which you exported the snapshots) to that server and run the program on the server with import option.  

### remove_fields.py
  To remove fields/keys from elasticsearch documents.  
  *Note* : Input needs to be given in the python file itself.
  1. Open the file and supply the index name, document type and field/key name to the variable ```fields_to_delete```. (A sample has been provided to show the format)
  2. Multiple indices, document types and fields can be given at once in the provided JSON format.
  
### export_mysql_to_es.py
  To export mysql database to elasticsearch.  
  *Note* : Settings need to be done in the python file itself:
  1. Set the variables for mySQL credentials, source database name and target index name.
  2. To export only some tables of the mySQL database instead of all:
    - Comment the line ```table_list = allTables()```
    - Uncomment the line ```table_list = ['tableName1','tableName2']``` and provide the required table names here
  3. Use variable ```reset``` to control if the target index in elasticsearch is to be newly created or not.
  4. If there are date/time fields in your mySQL data, you may need to set mappings for the elasticsearch index.  
    In this case, set the variable ```set_mapping``` to ```True``` and write the required mappings in ```setMapping()``` function. (A sample has been provided)
  5. If error occurs while exporting data due to datatype issues:
    - Fields with date/time type: Try setting ```convert_date``` to True
    - Fields with non-ascii values: Try setting ```convert_unicode``` to True

### es_process.py
  Module containing functions for common elasticsearch tasks/queries.  
  - **es_fetchall_of_type(***db_index,doc_type, only_id=False, fields=[]***)**  
    Fetches all documents of specified doc_type. If ```only_id``` is True, document source is not fetched.  Provide list of source fields to fetch in ```fetch``` parameter.  
    Returns array of hits found. Each array object will contain document id and source.
  - **getSource(***res***)**  
    Takes an array of hits (each object in this list contains source in key value form) and returns an array of all source objects i.e. extracts sources from each item in hits array.
  - **show(***obj***)**  
    Takes a JSON object and prints it in an indented manner.
  - **es_recreate_index(***db_index***)**  
    Deletes provided index name (if exists) and creates new index with the given name.
  - **es_search(***db_index,db_query, filter_source=False, size=1000, filter_path=['hits.hits._id', 'hits.hits._source', 'hits.total'], source=True, fields=[]***)**  
    Performs search for provided query.  
    Returns the ```hits``` object if ```filter_source``` parameter is False, otherwise returns an array containing source of each matched document.  
    Default search size has been set to 1000 to avoid the necessity of providing size argument to get more than 10 results (default size value in elasticsearch API and client is 10).  
    Use ```filter_path``` parameter to set the paths returned.  
    Set ```source``` parameter to False if you don't want to fetch document sources.  
    Provide a list of fields in ```fields``` parameter to return only specific source fields.
  - Other functions included (es_refresh_index,es_insert,es_delete,es_update,es_get) simply call the elasticsearch client functions.  
    [API documentation of python elasticsearch client](http://elasticsearch-py.readthedocs.io/en/master/api.html)