"""
author songjie
"""
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup

from app.spider.mv_list import MvList
from config import settings
from tool.db import DBConfig
from tool.function import curlData, debug, getUserAgent, getCookie

lock = threading.RLock()


class MvContentThread(object):
    def __init__(self):
        self.table_columns = (
            ("id", "int"),
            ("parent_id", "int"),
            ("url", "text")
        )
        self.cookie = dict()
        self.cookie_get_num = 0
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        """
        :return:
        """
        data = self.get_list()
        thread_pool = ThreadPoolExecutor(max_workers=15)
        task_list = list()
        self.get_cookie()
        for item in data:
            task = thread_pool.submit(self.handle_data, item)
            task_list.append(task)
        for i in as_completed(task_list):
            result = i.result()

    @classmethod
    def get_list(cls):
        """
        :return:
        """
        mv_list = MvList()
        return mv_list.get_mv_list()

    def handle_data(self, item):
        """
        :param item:
        :return:
        """
        page_resource = self.get_data(item)
        result = self.__handle_data(page_resource, item)
        if result == 0:
            debug("数据存储出错 --> {name}".format(name=item['title']))
        else:
            debug("数据存储成功 --> {name}".format(name=item['title']))
        return {"code": 0}

    def get_data(self, item):
        """
        :param item:
        :return:
        """
        url = item['url']
        page_resource = curlData(url, cookie=self.cookie, open_virtual_ip=True)
        return page_resource

    def get_cookie(self):
        url = settings.DOMAIN
        self.cookie_get_num = self.cookie_get_num + 1
        self.cookie = getCookie(url, open_virtual_ip=True)

    def __handle_data(self, page_resource, item):
        """
        :param page_resource:
        :param item:
        :return:
        """
        bs = BeautifulSoup(page_resource, "html.parser")
        insert_arr = dict()
        insert_arr['url'] = self.__get_url(bs, page_resource, item)
        insert_arr['parent_id'] = item['id']
        code = self.__save_data(insert_arr)
        return {"code": code}

    def __save_data(self, insert_arr):
        sql = self.db.getInsertSql(insert_arr, "content", table_columns=self.table_columns)
        lock.acquire()
        result = self.db.insert(sql, is_close_db=False)
        return result

    def __get_url(self, bs, page_resource, item):
        """
        :param bs:
        :param page_resource:
        :param item:
        :return:
        """
        url = bs.find("tbody", attrs={"id": "servidores_online"})
        url_str = ""
        try:
            token = re.findall('window.laravel_token = "([\w\W]*?)";', str(page_resource))[0]
        except Exception as e:
            debug("电影播放链接 _token 获取出错，出错信息：{error}".format(error=e))
            return url_str
        try:
            url = url.find_all("tr")
            for k, v in enumerate(url):
                if k < 1:
                    continue
                data = v.find("div", attrs={"class": "embedplayer"}).attrs['data-player']
                post = {
                    "data": data,
                    "tipo": "videohost",
                    "_token": token
                }
                url_str = self.__get_url_curl(post, referer=item['url'])
                break
        except Exception as e:
            url_str = ""
            debug("电影播放链接获取出错，出错信息：{error}".format(error=e))
        return url_str

    def __get_url_curl(self, post, referer):
        """
        :param post:
        :param referer:
        :return:
        """
        headers = {
            "user-agent": getUserAgent(),
            "origin": "https://www.pelisplay.tv",
            "referer": referer
        }
        url = "https://www.pelisplay.tv/entradas/procesar_player"
        data = curlData(url, value=post, cookie=self.cookie, header=headers)
        try:
            data = json.loads(data)
        except Exception as e:
            lock.acquire()
            self.get_cookie()
            lock.release()
            if self.cookie_get_num < 3:
                return self.__get_url_curl(post, referer=referer)
            else:
                data = {"estado": 500}
                debug("播放链接获取出错，错误信息：{error}".format(error=e))
        if data['estado'] == 200:
            data = data['data']
        else:
            data = ""
        self.cookie_get_num = 0
        return data
