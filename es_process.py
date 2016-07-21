import json
from elasticsearch import Elasticsearch
es = Elasticsearch()


def es_recreate_index(db_index):
	es.indices.delete(index=db_index, ignore=[400,404])
	es.indices.create(index=db_index, ignore=400)

def es_refresh_index(db_index):
	es.indices.refresh(index=db_index)

def es_insert(db_index,doc_type, body, refresh=True):
	res = es.index(index=db_index, doc_type=doc_type, body=body, refresh=refresh)
	if "_id" in res:
		return res["_id"]
	else:
		return False

def es_delete(db_index,doc_type, doc_id, refresh=True):
	res = es.delete(index=db_index, doc_type=doc_type, id=doc_id, refresh=refresh)

def es_update(db_index,doc_type, doc_id, body, update_type="doc", refresh=True):
	if update_type=="doc":
		doc = { "doc" : body }
	elif update_type=="script":
		doc = { "script" : body }
	es.update(index=db_index, doc_type=doc_type, id=doc_id, body=doc,refresh=refresh)
		
def es_get(db_index,doc_type, doc_id):
	res = es.get(index=db_index, doc_type=doc_type, id=doc_id, filter_path=['_id', '_source'])
	return res

def es_search(db_index,db_query, filter_source=False, size=1000, filter_path=['hits.hits._id', 'hits.hits._source', 'hits.total'], source=True, fields=[]):
	if source==False:
		res = es.search(index=db_index, body=db_query, filter_path=filter_path, size=size, _source=False)
	elif fields==[]:
		res = es.search(index=db_index, body=db_query, filter_path=filter_path, size=size, _source=True)
	else:
		res = es.search(index=db_index, body=db_query, filter_path=filter_path, size=size, _source=fields)
	if filter_source==False:
		return res['hits']
	else:
		return getSource(res['hits'])

def es_fetchall_of_type(db_index,doc_type, only_id=False, fields=[]):
	if only_id==True:
		q = { "filter" : { "type" : { "value" : doc_type } } }
		res = es_search(db_index,q,filter_path=['hits.total', 'hits.hits._id'])
	else:
		if fields==[]:
			q = { "filter" : { "type" : { "value" : doc_type } } }
		else:
			q = { "_source" : fields, "filter" : { "type" : { "value" : doc_type } } }
		res = es_search(q,filter_path=['hits.total', 'hits.hits._id', 'hits.hits._source'])
	if res["total"]>0:
		return res["hits"]
	else:
		return []


def getSource(res):
	ans = []
	if "hits" in res:
		res = res["hits"]
		for item in res:
			ans.append(item["_source"])
	return ans


def show(obj):
	print(json.dumps(obj, indent=2, sort_keys=True))