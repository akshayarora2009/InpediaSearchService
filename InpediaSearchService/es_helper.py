from elasticsearch import Elasticsearch
import InpediaSearchService.constants as constants

es = Elasticsearch()


def query_es(query):
    res = es.search(index=constants.INDEX_NAME, body={"query": {"match_all": {}}})
    return res['hits']
