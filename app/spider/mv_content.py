"""
author songjie
"""
from app.spider.thread.mv_content_thread import MvContentThread
from tool.db import DBConfig


class MvContent(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    @classmethod
    def run(cls):
        """
        :return:
        """
        mv_content_thread = MvContentThread()
        mv_content_thread.run()
