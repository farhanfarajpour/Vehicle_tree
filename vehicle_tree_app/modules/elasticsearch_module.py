from injector import Module, singleton, provider
from elasticsearch import Elasticsearch
from redis import Redis
from django.conf import settings


class ElasticModule(Module):
    @singleton
    @provider
    def provide_elasticsearch(self) -> Elasticsearch:
        return Elasticsearch(settings.ELASTICSEARCH_HOST['default']['hosts'])

def configure_elastic(binder):
    binder.bind(Elasticsearch, to=Elasticsearch, scope=singleton)

