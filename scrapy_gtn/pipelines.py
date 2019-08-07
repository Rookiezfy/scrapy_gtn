# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import os
import sys
# 临时修改环境变量 为当前目录上级目录
root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(root_dir)
import scrapy_gtn.conf.config as config

class HkStockPipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host=config.get_db_host(),
            port=config.get_db_port(),
            user=config.get_db_username(),
            passwd=config.get_db_passwd(),
            db=config.get_db_dbname(),
            charset=config.get_db_charset()
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        sql = 'replace into hk_stock(secid,code,name,market) VALUES (%s,%s,%s,%s)'
        lis = (item['secid'], item['code'], item['name'], item['market'])
        self.cur.execute(sql, lis)
        self.client.commit()
        return item
