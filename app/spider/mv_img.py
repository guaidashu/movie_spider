"""
author songjie
"""
from tool.function import curlData


class MvImg(object):
    def __init__(self, img_url):
        self.img_url = img_url

    def run(self):
        img_data = curlData(self.img_url)
