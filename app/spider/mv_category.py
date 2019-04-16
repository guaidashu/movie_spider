"""
author songjie
"""
from bs4 import BeautifulSoup

from config import settings
from tool.db import DBConfig
from tool.function import curlData, debug


class MvCategory(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()

    def get_category(self):
        """
        :return:
        """
        select_arr = {
            "table": "type"
        }
        category = self.db.select(select_arr, is_close_db=False)
        if not category:
            return []
        return category

    def get(self):
        """
        :return:
        """
        # page_resource = self.get_data()
        with open("tmp/index_page.txt", "rb") as f:
            page_resource = f.read().decode("utf-8")
            f.close()
        bs = BeautifulSoup(page_resource, "html.parser")
        category_list = self.__get_category_list(bs)
        for item in category_list:
            self.handle_data(item)

    def handle_data(self, item):
        """
        :param item:
        :return:
        """
        insert_arr = dict()
        insert_arr['status'] = 0
        insert_arr['url'] = self.__get_category_url(item)
        insert_arr['img_src'] = self.__get_category_img_src(item)
        insert_arr['icon_img_src'] = self.__get_category_icon_img_src(item)
        insert_arr['name'] = self.__get_category_name(item)
        insert_arr['description'] = self.__get_category_description(item)
        if self.__save_date(insert_arr):
            debug("类型存储成功")
        else:
            debug("类型存储失败")

    def __save_date(self, insert_arr):
        """
        :param insert_arr:
        :return:
        """
        table_columns = (
            ("id", "int"),
            ("img_src", "varchar"),
            ("icon_img_src", "varchar"),
            ("url", "varchar"),
            ("name", "varchar"),
            ("description", "text")
        )
        sql = self.db.getInsertSql(insert_arr, table="type", table_columns=table_columns)
        result = self.db.insert(sql, is_close_db=False)
        if result == 0:
            return False
        return True

    @classmethod
    def get_data(cls):
        """
        :return:
        """
        url = settings.DOMAIN
        data = curlData(url, open_virtual_ip=True)
        return data

    @classmethod
    def __get_category_list(cls, bs):
        """
        :param bs:
        :return:
        """
        category_list = bs.find_all("ul", attrs={"class": "owl-carousel"})
        try:
            category_list = category_list[0].find_all("li", attrs={"class": "item"})
        except Exception as e:
            category_list = list()
            debug("类型列表获取失败，错误信息：{error}".format(error=e))
        return category_list

    @classmethod
    def __get_category_url(cls, item):
        """
        :param item:
        :return:
        """
        category_url = item.find("a")
        try:
            category_url = category_url.attrs['href']
        except Exception as e:
            category_url = ""
            debug("分类url链接获取失败，错误信息：{error}".format(error=e))
        return category_url

    @classmethod
    def __get_category_img_src(cls, item):
        """
        :param item:
        :return:
        """
        category_img_src = item.find("img")
        try:
            category_img_src = category_img_src.attrs['src']
        except Exception as e:
            category_img_src = ""
            debug("图片地址获取失败，错误信息：{error}".format(error=e))
        return category_img_src

    @classmethod
    def __get_category_icon_img_src(cls, item):
        """
        get icon img src
        :param item:
        :return:
        """
        category_icon_img_src = item.find("img")
        try:
            category_icon_img_src = category_icon_img_src.attrs['src']
        except Exception as e:
            category_icon_img_src = ""
            debug("icon图片地址获取失败，错误信息：{error}".format(error=e))
        return category_icon_img_src

    @classmethod
    def __get_category_name(cls, item):
        """
        get category name
        :param item:
        :return:
        """
        category_name = item.find("div", attrs={"class": "category-name"})
        try:
            category_name = category_name.get_text().strip()
        except Exception as e:
            category_name = ""
            debug("类型名获取失败，错误信息：{error}".format(error=e))
        return category_name

    @classmethod
    def __get_category_description(cls, item):
        """
        :param item:
        :return:
        """
        category_description = item.find("div", attrs={"class": "category-description"})
        try:
            category_description = category_description.get_text().strip()
        except Exception as e:
            category_description = ""
            debug("类型描述获取失败，错误信息：{error}".format(error=e))
        return category_description
