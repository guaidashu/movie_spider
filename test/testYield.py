"""
author songjie
"""
from tool.function import debug


class TestYield(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @classmethod
    def fun(cls):
        for i in range(20):
            yield i
