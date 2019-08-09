# -*- coding: utf-8 -*-
# scrapy crawl hk_stock -o hk_stock.csv
import sys
import os
# 临时修改环境变量 为当前目录上两级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(root_dir)
import scrapy
import json
from ..items import HkStockItem
import scrapy_gtn.conf.config as config
import logging as log

log.basicConfig(level=log.WARNING,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=root_dir + '/hk_stock.log', mode='a', encoding='utf-8'),
                          log.StreamHandler(sys.stderr)})

class HkStockSpider(scrapy.Spider):
    name = 'hk_stock'

    def start_requests(self):
        start_url = 'http://52.push2.eastmoney.com/api/qt/clist/get/'
        headers = {
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Content-Type': 'application/javascript; charset=UTF-8'
        }
        pages = 650
        for page in range(1,pages):
            log.info('正在爬取第'+str(page)+'页港股股票数据...')
            yield scrapy.FormRequest(callback=self.parse,dont_filter=True,url=start_url,method='GET',headers=headers,
                                     formdata={'pn': str(page), 'pz': '20', 'po': '1', 'np': '1','fltt':'2','invt':'2','fs':'m:116','fields':'f12,f13,f14','fid':'f3'})


    def parse(self, response):
        response_str = str(response.text).replace("\n","").replace("\r","")
        data = json.loads(response_str)['data']
        if (data != None):
           res = data['diff']
           for one in res:
               item = HkStockItem()
               item['secid'] = str(one['f13']) + '.' + str(one['f12'])
               item['market'] = one['f13']
               item['stock_code'] = one['f12']
               item['stock_name'] = one['f14']
               yield item