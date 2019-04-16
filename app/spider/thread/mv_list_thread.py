"""
author songjie
"""
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup

from app.spider.common import GenerateUrl
from app.spider.mv_category import MvCategory
from tool.db import DBConfig
from tool.function import debug, curlData

lock = threading.RLock()


class MvListThread(object):
    def __init__(self):
        self.db = DBConfig()
        self.table_columns = (
            ("id", "int"),
            ("img_src", "varchar"),
            ("origin_src", "varchar"),
            ("url", "varchar"),
            ("description", "text"),
            ("description_poster", "text"),
            ("star", "varchar"),
            ("title", "varchar"),
            ("page_views", "int"),
            ("label", "text"),
            ("category_id", "int"),
            ("director", "varchar")
        )
        self.handle_num = 0

    def __del__(self):
        self.db.closeDB()

    def run(self):
        thread_pool = ThreadPoolExecutor(max_workers=10)
        task_list = list()
        category = self.get_category()
        for item in category:
            task_list.append(thread_pool.submit(self.handle_data, item))
        debug("本次线程数量：{length}".format(length=len(task_list)))
        for i in as_completed(task_list):
            result = i.result()
            if result['code'] == 0:
                debug("电影类型为 {category} 的数据抓取完毕".format(category=result['category']))
        debug("处理了{length}个线程".format(length=self.handle_num))

    @classmethod
    def get_category(cls):
        """
        :return:
        """
        mv_category = MvCategory()
        return mv_category.get_category()

    @classmethod
    def get_data(cls, category):
        """
        :param category:
        :return:
        """
        generate_url = GenerateUrl()
        url = generate_url.generate_url(domian=category)
        page_resource = curlData(url, open_virtual_ip=True)
        return page_resource

    def handle_data(self, category):
        """
        :param category:
        :return:
        """
        result = self.handle_data_child(category)
        while result['code'] == 0:
            category['url'] = result['url']
            result = self.handle_data_child(category)
        return {"code": 0, "category": category['name']}

    def handle_data_child(self, category):
        """
        :param category:
        :return:
        """
        code = 0
        page_resource = self.get_data(category['url'])
        # with open("tmp/mv_list_page.txt", "rb") as f:
        #     page_resource = f.read().decode("utf-8")
        #     f.close()
        bs = BeautifulSoup(page_resource, "html.parser")
        mv_list = self.__get_li_list(bs)
        for item in mv_list:
            self.__handle_data(item, category)
        lock.acquire()
        self.handle_num = self.handle_num + 1
        lock.release()
        next_url = self.__get_next_url(bs)
        if next_url == "":
            code = 1
        return {"code": code, "url": next_url}

    def __handle_data(self, item, category):
        insert_arr = dict()
        insert_arr['img_src'] = self.__get_img_src(item)
        insert_arr['origin_src'] = self.__get_origin_src(item)
        insert_arr['url'] = self.__get_url(item)
        insert_arr['category_id'] = category['id']
        insert_arr['description'] = self.__get_description(item)
        insert_arr['description_poster'] = self.__get_description_poster(item)
        insert_arr['star'] = self.__get_star(item)
        insert_arr['title'] = self.__get_title(item)
        insert_arr['page_views'] = self.__get_page_views(item)
        insert_arr['director'] = self.__get_director(item)
        insert_arr['label'] = self.__get_label(item)
        result = self.__save_data(insert_arr)
        if result == 0:
            debug("数据存储出错")
        else:
            debug("电影 {name} --> 列表存储成功".format(name=insert_arr['title']))

    def __save_data(self, insert_arr):
        """
        :param insert_arr:
        :return:
        """
        lock.acquire()
        sql = self.db.getInsertSql(insert_arr, "list", table_columns=self.table_columns)
        result = self.db.insert(sql, is_close_db=False)
        lock.release()
        return result

    @classmethod
    def __get_li_list(cls, bs):
        """
        :param bs:
        :return:
        """
        data = bs.find_all("figure")
        return data

    @classmethod
    def __get_img_src(cls, item):
        """
        :param item:
        :return:
        """
        img_src = item.find("img")
        try:
            img_src = img_src.attrs['src']
        except Exception as e:
            img_src = ""
            debug("电影封面图获取出错，出错信息：{error}".format(error=e))
        return img_src

    @classmethod
    def __get_origin_src(cls, item):
        """
        :param item:
        :return:
        """
        origin_src = item.find_all("img")
        try:
            origin_src = origin_src[1].attrs['src']
        except Exception as e:
            origin_src = ""
            debug("电影小图标获取出错，出错信息：{error}".format(error=e))
        return origin_src

    @classmethod
    def __get_url(cls, item):
        """
        :param item:
        :return:
        """
        url = item.find("a")
        try:
            url = url.attrs['href']
        except Exception as e:
            url = ""
            debug("电影详情链接地址获取出错，出错信息：{error}".format(error=e))
        return url

    @classmethod
    def __get_description(cls, item):
        """
        :param item:
        :return:
        """
        description = item.find("div", attrs={"class": "Description"})
        try:
            description = description.find("div")
            description = description.get_text().strip()
        except Exception as e:
            description = ""
            debug("电影描述获取出错，出错信息：{error}".format(error=e))
        return description

    @classmethod
    def __get_description_poster(cls, item):
        """
        :param item:
        :return:
        """
        description_poster = item.find("p", attrs={"class": "description_poster"})
        try:
            description_poster = description_poster.get_text().strip()
        except Exception as e:
            description_poster = ""
            debug("电影短述获取出错，出错信息：{error}".format(error=e))
        return description_poster

    @classmethod
    def __get_star(cls, item):
        """
        :param item:
        :return:
        """
        star = item.find("span", attrs={"class": "qualification"})
        try:
            star = star.get_text().strip()
        except Exception as e:
            star = ""
            debug("电影短述获取出错，出错信息：{error}".format(error=e))
        return star

    @classmethod
    def __get_title(cls, item):
        title = item.find("div", attrs={"class": "Title"})
        try:
            title = title.get_text().strip()
        except Exception as e:
            title = ""
            debug("电影标题获取出错，出错信息：{error}".format(error=e))
        return title

    @classmethod
    def __get_page_views(cls, item):
        """
        :param item:
        :return:
        """
        page_views = item.find("div", attrs={"class": "otros"})
        try:
            page_views = page_views.get_text().strip()
            page_views = page_views.replace(",", "")
            page_views = page_views.replace(" visitas", "")
        except Exception as e:
            page_views = 0
            debug("电影浏览量获取出错，出错信息：{error}".format(error=e))
        return page_views

    @classmethod
    def __get_director(cls, item):
        """
        :param item:
        :return:
        """
        director = item.find_all("div", attrs={"class": "otros"})
        try:
            director = director[1]
            director = director.get_text().strip()
            director = director.replace("Director: ", "")
        except Exception as e:
            director = ""
            debug("电影导演获取出错，出错信息：{error}".format(error=e))
        return director

    @classmethod
    def __get_label(cls, item):
        """
        :param item:
        :return:
        """
        label = item.find("div", attrs={"class": "tipcategorias"})
        label = label.find_all("span")
        s = ""
        try:
            for k, v in enumerate(label):
                if k == 0:
                    s = s + v.get_text().strip()
                else:
                    s = s + "," + v.get_text().strip()
        except Exception as e:
            debug("电影标签获取出错，出错信息：{error}".format(error=e))
        return s

    @classmethod
    def __get_next_url(cls, bs):
        """
        :param bs:
        :return:
        """
        next_url = bs.find_all("ul", attrs={"class": "pager"})
        try:
            next_url = next_url[0].find("a", attrs={"rel": "next"})
            next_url = next_url.attrs['href']
        except Exception as e:
            next_url = ""
            debug("下一页url获取出错，出错信息：{error}".format(error=e))
        debug(next_url)
        return next_url
