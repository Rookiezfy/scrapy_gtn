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
from twisted.enterprise import adbapi
import scrapy_gtn.conf.config as config
import logging as log

# 异步机制将数据写入到mysql数据库中
class HkStockPipeline(object):
    def __init__(self):
        dbparms = dict(
            host=config.get_db_host(),
            db=config.get_db_dbname(),
            port=config.get_db_port(),
            user=config.get_db_username(),
            passwd=config.get_db_passwd(),
            charset=config.get_db_charset(),
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparms)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
    def do_insert(self,cursor,item):
        sql = 'replace into hk_stock(secid,code,name,market) VALUES (%s,%s,%s,%s)'
        lis = (item['secid'], item['code'], item['name'], item['market'])
        cursor.execute(sql, lis)

    def handle_error(self, failure):
        log.error(failure)