import json

from django.conf import settings
from redis import Redis
from redis import ConnectionPool as RedisConnectionPool
from redis.connection import Connection

WEBSOCKET_REDIS_BROKER_DEFAULT = {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0
}

CONNECTION_KWARGS = getattr(settings, 'WEBSOCKET_REDIS_BROKER', WEBSOCKET_REDIS_BROKER_DEFAULT)


class ConnectionPoolManager(object):
    """
    A singleton that contains and retrieves redis ``ConnectionPool``s according to the connection settings.
    """
    pools = {}

    @classmethod
    def key_for_kwargs(cls, kwargs):
        return ":".join([str(v) for v in kwargs.values()])

    @classmethod
    def connection_pool(cls, **kwargs):
        pool_key = cls.key_for_kwargs(kwargs)
        if pool_key in cls.pools:
            return cls.pools[pool_key]

        params = {
            'connection_class': Connection,
            'db': kwargs.get('DB', 0),
            'password': kwargs.get('PASSWORD', None),
            'host': kwargs.get('HOST', 'localhost'),
            'port': int(kwargs.get('PORT', 6379))
        }

        cls.pools[pool_key] = RedisConnectionPool(**params)
        return cls.pools[pool_key]


def redis_connection():
    """
    Returns a redis connection from one of our pools.
    """
    pool = ConnectionPoolManager.connection_pool(**CONNECTION_KWARGS)
    return Redis(connection_pool=pool)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)



        