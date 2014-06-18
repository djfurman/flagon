import redis

from flagon import errors
from flagon.backends import Backend


class RedisBackend(Backend):

    def __init__(self, host, port, db):
        """
        Creates an instance of the RedisBackend.

        :rtype: RedisBackend
        """
        # https://pypi.python.org/pypi/redis/2.10.1
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self._server = redis.Redis(
            connection_pool=pool,
            charset='utf-8',
            errors='strict',
            decode_responses=False)

    def set(self, name, key, value):
        """
        Sets a value for a feature. This is a proposed name only!!!

        :param name: name of the feature.
        :rtype: bool
        """
        self._server.hset(name, key, value)

    def exists(self, name, key):
        """
        Checks if a feature exists.

        :param name: name of the feature.
        :rtype: bool
        """
        return self._server.hexists(name, key)

    def is_active(self, name, key):
        """
        Checks if a feature is on.

        :param name: name of the feature.
        :rtype: bool
        :raises: UnknownFeatureError
        """
        if not self._server.hexists(name, key):
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)
        if self._server.hget(name, key) == 'True':
            return True
        return False

    def _turn(self, name, key, value):
        """
        Turns a feature off.

        :param name: name of the feature.
        :param value: Value to turn name to.
        :raises: UnknownFeatureError
        """
        # TODO: Copy paste --- :-(
        if not self._server.hexists(name, key):
            raise errors.UnknownFeatureError('Unknown feature: %s %s' % (
                name, key))
        self._server.hset(name, key, value)

    turn_on = lambda s, name: s._turn(name, 'active', True)
    turn_off = lambda s, name: s._turn(name, 'active', False)