# -*- coding: utf-8 -*-
import sys
import os
# 临时修改环境变量 为当前目录上两级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(root_dir)
import scrapy
import json
from ..items import USStockItem
import scrapy_gtn.conf.config as config
import logging as log

log.basicConfig(level=log.WARNING,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=root_dir + '/us_stocks.log', mode='a', encoding='utf-8'),
                          log.StreamHandler(sys.stderr)})

# 美股列表 数据来源：雪球 https://xueqiu.com/hq#exchange=US&firstName=3&secondName=3_0
class UsStocksSpider(scrapy.Spider):
    name = 'us_stocks'

    def start_requests(self):
        start_url = 'https://xueqiu.com/service/v5/stock/screener/quote/list'
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Content-Type': 'application/json; charset=utf-8'
        }

        pages = 100
        for page in range(1,pages):
            log.info('正在爬取第'+str(page)+'页'+'美股股票列表...')
            yield scrapy.FormRequest(callback=self.parse,dont_filter=True,url=start_url,method='GET',headers=headers,
                                     formdata={'page': str(page), 'size': '90', 'market': 'US', 'type': 'us','order_by':'percent'})

    def parse(self, response):
        response_str = str(response.text).replace("\n", "").replace("\r", "")
        if(str(json.loads(response_str)['error_code']) == '0'):
            data = json.loads(response_str)['data']['list']
            if (data != None and len(data) > 0 ):
                for one in data:
                    item = USStockItem()
                    item['symbol'] = one['symbol']
                    item['market'] = 'us'
                    item['stock_name'] = one['name']
                    yield item
