from injector import Injector
from vehicle_tree_app.modules.minio_module import MinIOModule
from vehicle_tree_app.modules.redis_module import RedisModule
from vehicle_tree_app.modules.kavenegar_module import KavenegarModule
import os

BaseInjector = Injector(
    [
        MinIOModule,
        RedisModule,
        KavenegarModule(os.getenv('KAVENEGAR_KEY'))

    ]
)
