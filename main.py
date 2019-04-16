"""
author songjie
"""
import base64

from app.spider.mv_category import MvCategory
from app.spider.mv_content import MvContent
from app.spider.mv_list import MvList
from test.testYield import TestYield
from tool.function import debug


if __name__ == "__main__":
    # mv_category = MvList()
    # mv_category.run()
    mv_content = MvContent()
    mv_content.run()
    # test = TestYield()
    # for i in test.fun():
    #     debug(i)
    # rel = "eyJpdiI6Iks0TW1ieXkrdHY5MVU2UFhYbG91U0E9PSIsInZhbHVlIjoiQ1RGMzFqaTlVV3V5TzN0TzBjZzltVG0zMmw1b1QxXC85Wk5zMGdLRk1lN3VkXC95dGxkYzdNR3ZYWllqTFJkK2o4ZzNsMUZSZmpsUFZ0MmtHeEl4XC9NTEp6Z0tGUVUwQmhyWnMzOVpzS3RBbDBFXC83bThlQ3YxWE9SQ1JoNDdzTXB0MTQxcmRLXC9CK0xNY21xNXJpNHJiUzM1Z2daUjNUK0wyOUE0MXA4a25KZDU0aTFMdVZQVmNReDBMKzFTd1dGaDZRbjhtS1Z2UHpEc3JIMTRPZ0pqckQxcjVyVFJhS0JFbFZGK1wvUWZ6M2dQdz0iLCJtYWMiOiI0OTdiZDJhZmQzOGQ5NzNiYWJhMDNhNDA4ZTRmNTgwZGFiMTY3MjMzOWU2NzVhYmExZWVlYzVhYWM0NzFjZjAxIn0="
    # url = "eyJpdiI6IlM3Q3pxd1hRcTJaYXBseUxuU2RiS0E9PSIsInZhbHVlIjoiWFRkTldJN0phUk1DMDZQV2xuRkoxdz09IiwibWFjIjoiMGNiYmJjYmMxYzlhY2Y0YTk5Mzg3YmU2ZmVlNTFmYWEwNDE3YjBlMzA3ZGNkNzNmOTA0MjQ0YzBlNTIwOGE4ZCJ9"
    # data = base64.b64decode(rel).decode("utf-8")
    # debug(data)
