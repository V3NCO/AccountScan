from piccolo.engine.postgres import PostgresEngine
from piccolo.conf.apps import AppRegistry
from accscan.config import settings

DB = PostgresEngine(config={'dsn': settings.database_url})

APP_REGISTRY = AppRegistry(apps=['accscan.piccolo_app'])
