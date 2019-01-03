from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Integer, Search
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from . import models
import settings

connections.create_connection()
refresh=settings.ES_AUTOREFRESH

class TopStoriesIndex(DocType):

    title = Text()
    submitted_by = Text()
    description = Text()
    sentiment = Text()
    score = Integer()

    class Meta:
        index = 'topstories-index'


def bulk_indexing():
    TopStoriesIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.TopStories.objects.all().iterator()))

def search(title):
    s = Search().filter('term', title=title)
    response = s.execute()
    return response
