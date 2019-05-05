"""
author songjie
"""
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from tool.db import DBConfig
from tool.function import debug, curlData, getUserAgent, getCookie

lock = threading.RLock()


class GetVideoSrc(object):
    def __init__(self):
        self.cookie = {}
        # self.get_cookie()
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        data = self.get_content_list()
        self.handle_data(data)

    def handle_data(self, data):
        thread_pool = ThreadPoolExecutor(max_workers=15)
        task_list = list()
        for item in data:
            if item['url'] == '':
                continue
            else:
                task = thread_pool.submit(self.__handle_data, item)
                task_list.append(task)
                # self.__handle_data(item)
        for i in as_completed(task_list):
            result = i.result()

    def __handle_data(self, item):
        update_data = dict()
        update_data['status'] = 1
        update_data['video_src'] = self.__get_video_src(item)
        debug(update_data['video_src'])
        self.__update_data(item['id'], update_data)
        return {"code": 0}

    def __get_video_src(self, item):
        header = {
            # "Referer": "http://www.wyysdsa.com/",
            "User-Agent": getUserAgent(),
            # "Cache-Control": "max-age=0",
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        # url = "http://zeus.pelisplay.tv/embed/vip.php?u=Q1A5NUZJM1VDTWlUTk8wTEFmWGNQZDhnbWRIcmt6UVU0VGIxakpXOUF4Mi9yZW51Zi9yaXZlcXFoYnlwL3picC5hYm1uem4uampqLy86ZmNnZ3U&fondo_requerido="
        # url = "https://nl.tan90.club/test/testHeader.html"
        data = curlData(url=item['url'], header=header, cookie=self.cookie)
        # with open("tmp/content_detail.txt", "rb") as f:
        #     data = f.read().decode("utf-8")
        #     f.close()
        try:
            src = re.findall("JSON\.parse\('([\w\W]*?)'\)\);", data)[0]
            src = src.replace("\\", "")
            src = json.loads(src)
            src = src[0]['file']
        except Exception as e:
            src = ""
            debug(e)
        return src

    def __update_data(self, content_id, update_data):
        update_arr = {
            "table": "content",
            "set": update_data,
            "condition": ['id={content_id}'.format(content_id=content_id)]
        }
        lock.acquire()
        result = self.db.update(update_arr, is_close_db=False)
        lock.release()
        return result

    def get_content_list(self):
        data = self.db.select({
            "table": "content",
            "columns": ['id', 'url'],
            "condition": ['status=0']
        }, is_close_db=False)
        return data

    def get_cookie(self):
        header = {
            "User-Agent": getUserAgent(),
            # "Cache-Control": "max-age=0",
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
        url = "https://www.pelisplay.tv/"
        self.cookie = getCookie(url, header=header)
        debug(self.cookie)
