"""
author songjie
"""
from app.spider.get_video_src import GetVideoSrc
from app.spider.help.clearNullData import ClearNullData
from app.spider.mv_img import MvImg

if __name__ == "__main__":
    # get_video_src = GetVideoSrc()
    # get_video_src.run()
    # mv_img = MvImg()
    # mv_img.run()
    clear_null_data = ClearNullData()
    clear_null_data.run()
