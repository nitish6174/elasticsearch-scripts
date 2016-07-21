import os
from colorprint import *

fields_to_delete = {
	"index_name_1" : {
		"doc_type_1" : [ "key_1" , "key_2" ],
		"doc_type_2" : [ "key_3" ]
	},
	"index_name_2" : {
		"doc_type_3" : [ "key_4" ]
	}
}

for index in fields_to_delete:
	for doc_type in fields_to_delete[index]:
		res = es_fetchall_of_type(index,doc_type)
		doc_ids = [ x["_id"] for x in res ]
		for doc_id in doc_ids:
			for field in fields_to_delete[index][doc_type]:
				cmd = "curl -XPOST \'localhost:9200/"+index+"/"+doc_type+"/"+doc_id+"/_update\' -d \'{ \"script\" : \"ctx._source.remove(\\\""+field+"\\\")\" }\'"
				cprint("\n"+cmd,"yellow")
				os.system(cmd)
