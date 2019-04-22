"""
author songjie
"""
from flask import Blueprint

help_spider = Blueprint("help_spider", __name__, url_prefix="/help_spider")

from app.web.help_spider import get_image
