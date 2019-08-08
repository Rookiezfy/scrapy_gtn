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
import scrapy_gtn.items as items

# 异步机制将数据写入到mysql数据库中
class HkStockPipeline(object):
    def __init__(self):
        dbparms = dict(
            host=config.get_db_host(),
            db=config.get_db_dbname(),
            port=config.get_db_port(),
            user=config.get_db_username(),
            password=config.get_db_passwd(),
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
        # 港股股票列表
        if isinstance(item, items.HkStockItem):
            sql = 'insert into hk_stock(secid,code,name,market) VALUES (%s,%s,%s,%s) on duplicate key update code = %s,name = %s, market = %s'
            lis = (item['secid'], item['code'], item['name'], item['market'],item['code'], item['name'], item['market'])
            cursor.execute(sql, lis)

        # 港股行情
        if isinstance(item, items.HkQuotItem):
            table_name = ''
            # 日k
            if(item['freq'] == '101'):
                table_name = 'hk_stock_daily'
            # 周k
            if(item['freq'] == '102'):
                table_name = 'hk_stock_weekly'
            # 月k
            if(item['freq'] == '103'):
                table_name = 'hk_stock_monthly'

            sql = 'insert into ' + table_name + '(ts_code,trade_date,open,high,low,close,vol,amount,secid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                  ' on duplicate key update open = %s,high = %s,low = %s,close = %s,vol = %s, amount = %s, secid = %s'
            lis = (item['ts_code'], item['trade_date'],item['open'], item['high'], item['low'], item['close'], item['vol'], item['amount'],item['secid'],
                   item['open'], item['high'], item['low'], item['close'], item['vol'], item['amount'],item['secid'])
            cursor.execute(sql, lis)

    def handle_error(self, failure):
        log.error(failure)