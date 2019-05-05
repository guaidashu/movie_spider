"""
author songjie
"""
import re
import urllib.parse

from flask import Response, request

from app.web.help_spider import help_spider
from tool.function import curlData, get_image_type, debug, getUserAgent


@help_spider.route('/getImage')
def get_image():
    url = request.values.get("url")
    if url is not None:
        domain = "https://www.pelisplay.tv"
        url = urllib.parse.unquote(url)
        final_url = domain + url
        header = {
            "Referer": "https://www.pelisplay.tv/",
            "User-Agent": getUserAgent(),
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
        }
        data = curlData(final_url, header=header, open_virtual_ip=True)
        ext = re.findall("[\w\W]*?\.([\w\W]*.)", url)[0]
    else:
        ext = "jpg"
        data = ""
    # debug(data)
    return Response(data, mimetype=get_image_type(ext))
