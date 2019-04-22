"""
author songjie
"""
from app.web.help_spider import help_spider


@help_spider.route('/getImage')
def get_image():
    return "get image"
