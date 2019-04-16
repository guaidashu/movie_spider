"""
author songjie
"""
from app.spider.thread.mv_list_thread import MvListThread
from tool.db import DBConfig


class MvList(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    @classmethod
    def run(cls):
        """
        start get movie list
        :return:
        """
        mv_list_thread = MvListThread()
        mv_list_thread.run()

    def get_mv_list(self):
        """
        :return:
        """
        select_arr = {
            "table": "list"
        }
        mv_list = self.db.select(select_arr, is_close_db=False)
        return mv_list
