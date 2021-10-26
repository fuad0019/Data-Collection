from elasticsearch import Elasticsearch
elastic = Elasticsearch(hosts=["192.168.136.34"])

results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {"match_all":{}}})

print(results)

