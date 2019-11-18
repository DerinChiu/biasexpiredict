# Author: zhaolu
import time
import threading

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict  # Python < 2.7


class BiasExpireDict:
    """
    Bias Expire Dict 偏差过期字典
    An incomplete and imperfect solution for expiring dict

    The final key expiring time is between 'expire' and 'expire'+'bias'.
    Smaller bias means more accurate expire time but more resources consumption

    *** Usage of big data might be malfunctioning
    *** Usage of tiny bias might be malfunctioning

    """
    def __init__(self, expire, bias):
        """
        :param expire: expire time in seconds
        :param bias: bias time in seconds
        """
        assert expire > 0
        assert bias > 0

        self.__dict = dict()
        self.__seq = OrderedDict()

        self.expire = expire
        self.bias = bias

        self.__lock = threading.RLock()
        self.__thread = threading.Thread(target=self.__heartbeat)
        self.__thread.setDaemon(True)
        self.__thread.start()

    # def __repr__(self):
    #     import json
    #     return json.dumps(self.__dict) + json.dumps(self.__seq)

    def __contains__(self, key):
        return key in self.__dict

    def __getitem__(self, key):
        return self.__dict[key]

    def __setitem__(self, key, value):
        with self.__lock:
            self.__dict[key] = value
            self.__seq[key] = time.time()

    def __heartbeat(self):
        while 1:
            time.sleep(self.bias)

            now = time.time()
            expired = []
            with self.__lock:
                for key, reg_time in self.__seq.items():
                    if now - reg_time < self.expire:
                        break
                    expired.append(key)
                for exp in expired:
                    del self.__seq[exp], self.__dict[exp]

    def remove(self, key):
        with self.__lock:
            del self.__dict[key]
            del self.__seq[key]

    def get(self, key, default=None):
        return self.__dict.get(key, default)

    def update(self, value):
        """not write yet"""
        raise NotImplementedError

    def items(self):
        return self.__dict.items()

    def values(self):
        return self.__dict.values()

    def keys(self):
        return self.__dict.keys()
