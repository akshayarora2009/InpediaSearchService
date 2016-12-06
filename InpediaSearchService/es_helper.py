from elasticsearch import Elasticsearch
import InpediaSearchService.constants as constants

es = Elasticsearch()


def query_es(query):
    res = es.search(index=constants.INDEX_NAME,
                    body={"query":{"bool":{"should":[{"match":{"title":{"query":query,"boost":2,"fuzziness": "AUTO"}}},{"match":{"description":query}}]}}})
    hits = res['hits']['hits']
    answer = []

    for hit in hits:
        if '_index' in hit:
            del hit['_index']

        # TODO: Temporarily removing `related` products information because it is not being used
        if '_source' in hit:
            if 'related' in hit['_source']:
                del hit['_source']['related']

        answer.append(hit)

    return answer
