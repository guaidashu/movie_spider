"""
author songjie
"""
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tool.db import DBConfig
from tool.function import curlData, debug, getUserAgent

lock = threading.RLock()


class MvImg(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle_data()

    def handle_data(self):
        data = self.get_img_list()
        thread_pool = ThreadPoolExecutor(max_workers=15)
        task_list = list()
        for item in data:
            task = thread_pool.submit(self.__handle_data, item)
            task_list.append(task)
            # break
        for i in as_completed(task_list):
            result = i.result()

    def __handle_data(self, item):
        url = "https://www.pelisplay.tv" + item['img_src']
        header = {
            # "Referer": "https://www.pelisplay.tv/",
            "User-Agent": getUserAgent(),
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
        }
        data = curlData(url, header=header)
        with open("static/images/{id}.jpg".format(id=item['id']), "wb") as f:
            try:
                data = data.encode("utf-8")
            except Exception as e:
                debug(e)
            f.write(data)
            self.__update_data(item)
            f.close()
        return {"code": 0}

    def __update_data(self, item):
        update_arr = {
            "table": "list",
            "set": {
                "img_status": 1
            },
            "condition": ['id={id}'.format(id=item['id'])]
        }
        lock.acquire()
        result = self.db.update(update_arr, is_close_db=False)
        lock.release()
        return result

    def get_img_list(self):
        select_arr = {
            "table": "list",
            "columns": ["id", "img_src"],
            "condition": ['img_status=0']
        }
        data = self.db.select(select_arr, is_close_db=False)
        return data
