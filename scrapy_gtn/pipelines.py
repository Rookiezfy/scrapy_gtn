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
import datetime

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
        if isinstance(item, items.StockItem):
            sql = 'insert into hk_hs_stock_list(secid,market,stock_code,stock_name) VALUES (%s,%s,%s,%s) on duplicate key update market = %s,stock_code = %s, stock_name = %s'
            lis = (item['secid'], item['market'], item['stock_code'], item['stock_name'],item['market'], item['stock_code'], item['stock_name'])
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

            sql = 'insert into ' + table_name + '(stock_code,' \
                                                'trade_date,' \
                                                'open_px,' \
                                                'high_px,' \
                                                'low_px,' \
                                                'close_px,' \
                                                'business_amount,' \
                                                'business_balance,' \
                                                'secid,' \
                                                'market) VALUES ' \
                                                '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                  ' on duplicate key update open_px = %s,' \
                                                'high_px = %s,' \
                                                'low_px = %s,' \
                                                'close_px = %s,' \
                                                'business_amount = %s,' \
                                                'business_balance = %s,' \
                                                'secid = %s,' \
                                                'market = %s,' \
                                                'last_upd_time = %s'
            lis = (item['stock_code'], item['trade_date'],item['open_px'], item['high_px'], item['low_px'], item['close_px'], item['business_amount'],
                   item['business_balance'],item['secid'],item['market'],
                   item['open_px'], item['high_px'], item['low_px'], item['close_px'], item['business_amount'],
                   item['business_balance'],item['secid'],item['market'],datetime.datetime.now())
            cursor.execute(sql, lis)

    def handle_error(self, failure):
        log.error(failure)