import sys
import os
# 临时修改环境变量 为当前目录上两级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(root_dir)

import pandas as pd
import tushare as ts
import scrapy_gtn.history.stock_basic as stock_basic
import scrapy_gtn.conf.config as config
import logging as log
import time
import datetime
from dateutil.parser import parse

log.basicConfig(level=log.INFO,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=root_dir + '/stock_quotation.log', mode='a', encoding='utf-8'),
                          log.StreamHandler(sys.stderr)})

# 获取所有沪深股票的日、周、月以及分时数据
# 沪深股票信息
stocks = stock_basic.get_stock_basic()
if(len(stocks) == 0):
    print('获取股票数据失败')
    sys.exit(0)

# 从参数本次采集开始日期
if(len(sys.argv) == 1):#未填写开始采集日期
    log.error('执行出错，请输入数据采集开始日期')
    sys.exit(1)
else:
    try:
        parse(sys.argv[1])
    except:
        log.error('执行出错，数据采集开始日期格式错误，请输入正确的日期yyyyMMdd')
        sys.exit(1)
start_date = sys.argv[1]

# 计算开始日期与当前日期天数差
days = (datetime.datetime.now().date() - parse(start_date).date()).days
if (days < 0):
    log.error('请输入今天之前的日期')
    sys.exit(1)

# 循环获取各个频率数据
ts.set_token(config.get_token())
stock_code_arr = stocks['ts_code']

# 指定字段输出顺序
cols1 = ['ts_code','trade_date','open','high','low','close','pre_close','change','pct_chg','vol','amount']
#接口限制一分钟只能访问120次
for freq in ['D','W','M']:
    res = pd.DataFrame()
    for ts_code in stock_code_arr:
        log.info('获取---' + str(ts_code) + '---' + freq + '---数据开始')
        df = ts.pro_bar(freq=freq, ts_code=str(ts_code),start_date=start_date)
        res = res.append(df, ignore_index=True)
        log.info('获取---' + str(ts_code) + '---' + freq + '---数据结束')
        time.sleep(0.5)
        break
    res = res[cols1]
    res.to_csv(root_dir + config.get_data_dir() + 'stock_'+freq+'.csv', index=False,sep=',')


# 指定字段输出顺序
cols2 = ['ts_code','trade_date','trade_time','open','high','low','close','pre_close','vol','amount']
# 接口限制一分钟只能取访问5次
for freq in ['1MIN','5MIN','15MIN','30MIN','60MIN']:
    res = pd.DataFrame()
    for ts_code in stock_code_arr:
        log.info('获取---' + str(ts_code) + '---' + freq + '---数据开始')
        for i in range(0,days):
            get_date = (parse(start_date).date() + datetime.timedelta(days=i)).strftime('%Y%m%d')
            log.info('---正在获取'+get_date+'日期的数据...')
            df = ts.pro_bar(freq=freq, ts_code=str(ts_code),start_date=get_date)
            res = res.append(df, ignore_index=True)
            log.info('---ok')
            time.sleep(15)
        log.info('获取---' + str(ts_code) + '---' + freq + '---数据结束')
        time.sleep(15)
        break
    res = res[cols2]
    res.to_csv(root_dir + config.get_data_dir() + 'stock_'+freq+'.csv', index=False,sep=',')