"""
author songjie
"""
from tool.db import DBConfig
from tool.function import debug


class ClearNullData(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        debug(data)
        self.del_list(data)
        self.del_content(data)

    def del_list(self, data):
        for item in data:
            self.__del_list(item)

    def __del_list(self, item):
        delete_arr = {
            "table": "list",
            "condition": ["id={id}".format(id=item['parent_id'])]
        }
        result = self.db.delete(delete_arr, is_close_db=False)
        return result

    def del_content(self, data):
        for item in data:
            self.__del_content(item)

    def __del_content(self, item):
        delete_arr = {
            "table": "content",
            "condition": ["parent_id={id}".format(id=item['parent_id'])]
        }
        result = self.db.delete(delete_arr, is_close_db=False)
        return result

    def get_data(self):
        select_arr = {
            "table": "content",
            "limit": [0, 10],
            "condition": ["video_src=''", "and", "url=''"]
        }
        data = self.db.select(select_arr, is_close_db=False)
        return data
