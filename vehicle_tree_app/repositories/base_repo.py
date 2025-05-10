from injector import inject
from vehicle_tree_app.services.redis.redis import RedisService
from vehicle_tree_app.services.minio.minio import MinIOSDK
from vehicle_tree_app.services.sms.tasks import KavenegarAPI
from vehicle_tree_app.services.elastic_search.elastic_search import Elasticsearch


class BaseRepo:

    @inject
    def __init__(self, minio_sdk: MinIOSDK, elastic: Elasticsearch,redis: RedisService, KavenegarAPI: KavenegarAPI):
        self.service_minio = minio_sdk
        self.redis = redis
        self.KavenegarAPI = KavenegarAPI
        self.elastic = elastic
