from elasticsearch import Elasticsearch
import InpediaSearchService.constants as constants

es = Elasticsearch()


def query_es(query):
    res = es.search(index=constants.INDEX_NAME,
                    body={"query": {"fuzzy": {"title": {"value": query, "prefix_length": 1, "max_expansions": 100}}}})
    return res['hits']
