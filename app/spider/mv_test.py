"""
author songjie
"""
from tool.db import DBConfig


class MvTest(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        pass

    def get_category(self):
        pass
