from injector import inject
from vehicle_tree_app.services.redis.redis import RedisService
from vehicle_tree_app.services.minio.minio import MinIOSDK
from vehicle_tree_app.services.sms.tasks import KavenegarAPI


class BaseRepo:

    @inject
    def __init__(self, minio_sdk: MinIOSDK, redis: RedisService,KavenegarAPI:KavenegarAPI):
        self.service_minio = minio_sdk
        self.Redis = redis
        self.KavenegarAPI = KavenegarAPI

