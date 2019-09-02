# -*- coding: utf-8 -*-
import sys
import os
# 临时修改环境变量 为当前目录上两级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(root_dir)
import scrapy
import pymysql
import logging as log
import scrapy_gtn.conf.config as config
import json
from ..items import QuotItem
import datetime
import time

log.basicConfig(level=log.WARNING,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=root_dir + '/us_quotation.log', mode='a', encoding='utf-8'),
                          log.StreamHandler(sys.stderr)})

# 从雪球爬取美股行情数据
class UsQuotationSpider(scrapy.Spider):
    name = 'us_quotation'

    def start_requests(self):
        start_url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8'
        }
        # 查询所有美股股票列表
        connection = pymysql.connect(
            host=config.get_db_host(),
            db=config.get_db_dbname(),
            port=config.get_db_port(),
            user=config.get_db_username(),
            password=config.get_db_passwd(),
            charset=config.get_db_charset())
        cursor = connection.cursor()
        cursor.execute('select symbol,market,stock_name from us_stock_list limit 2')
        hs_stocks = cursor.fetchall()

        # k线频度及对应接口参数
        # 1分钟'1m',5分钟'5m', 15分钟'15m', 30分钟'30m', 60分钟'60m', 日'day', 周'week', 月'month'
        freqs = ['1m','5m', '15m', '30m', '60m', 'day', 'week', 'month']

        for freq in freqs:
            for hs_stock in hs_stocks:
                log.info('正在爬取美股[' + hs_stock[0] + hs_stock[2] + ']频度' + freq + '数据...')
                meta = {'symbol': hs_stock[0],
                        'market': hs_stock[1],
                        'stock_name': hs_stock[2],
                        'klt': freq}
                params = {'symbol': 'XNET',
                          'begin': str(int(round(time.time() * 1000))),
                          'period': freq,
                          'type': 'normal',
                          'count':'-432',
                          'indicator':'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
                          }
                yield scrapy.Request(callback=self.parse, dont_filter=True, url=start_url, method='GET',
                                         headers=headers,
                                         meta=meta, formdata=params)

    def parse(self, response):
        log.info(str(response.text))
        # market = response.meta['market']
        # stock_code = response.meta['stock_code']
        # stock_name = response.meta['stock_name']
        # secid = response.meta['secid']
        # freq = response.meta['klt']
        #
        # text = str(response.text).replace("\n", "").replace("\r", "")
        # response_str = text[1:len(text)-1]
        #
        # data = []
        # try:
        #     data = json.loads(response_str)['data']
        # except:
        #     log.error(secid+ '爬取'+stock_code+stock_name+freq+'频度数据出错...')
        #
        # if (data != None and len(data) > 0):
        #     cur_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
        #
        #     # 分钟线和日线 取当天的数据
        #     # 周线和月线 取倒数第二条数据 防止日k 周k出现多余数据
        #     recently = []
        #     if (freq in ['wk', 'mk']):
        #         data.pop()
        #         recently.append(data[len(data)-1])
        #
        #     else:
        #         for one in data:
        #             if (str(one).split(',')[0].find(cur_date) >= 0):
        #                 recently.append(one)
        #
        #     for one in recently:
        #         item = QuotItem()
        #         item['secid'] = secid
        #         item['market'] = market
        #         item['stock_code'] = stock_code
        #         item['stock_name'] = stock_name
        #         if (freq in ['m5k', 'm15k', 'm30k', 'm60k']): #分钟数据，处理交易时间字段
        #             item['trade_time'] = str(one).split(',')[0]
        #             item['trade_date'] = (str(one).split(',')[0])[0:10]
        #         else:
        #             item['trade_time'] = ''
        #             item['trade_date'] = str(one).split(',')[0]
        #         item['open_px'] = str(one).split(',')[1]
        #         item['high_px'] = str(one).split(',')[3]
        #         item['low_px'] = str(one).split(',')[4]
        #         item['close_px'] = str(one).split(',')[2]
        #         item['business_amount'] = str(one).split(',')[5]
        #         item['business_balance'] = str(one).split(',')[6]
        #         item['freq'] = freq
        #         yield item