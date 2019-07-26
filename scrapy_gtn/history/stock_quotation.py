import sys
import pandas as pd
import tushare as ts
import scrapy_gtn.history.stock_basic as stock_basic
import scrapy_gtn.conf.config as config
import logging as log
import datetime
import time

log.basicConfig(level=log.INFO,format=config.get_log_format(),datefmt=config.get_log_datefmt(),
                handlers={log.FileHandler(filename=config.get_log_dir() + 'stock_d_w_m.log', mode='a', encoding='utf-8')})

# 获取所有沪深股票的日、周、月以及分时数据


# 沪深股票信息 写入stock_basic.csv
stock_file_path = stock_basic.get_stock_basic()
stocks = pd.read_csv(stock_file_path)
if(len(stocks) == 0):
    print('获取股票数据失败')
    sys.exit(0)

# 上一次采集数据截止日期,执行前需要确认，便于增量执行
# 若全量执行，设置为空串 ''
last_end_date = ''

# 本次采集开始日期
start_date = ''
if len(last_end_date) != 0: #增量执行，计算本次执行的开始日期
    start_date = (datetime.datetime.strptime(last_end_date,'%Y%m%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')
    print(start_date)
else: #全量执行(tushare目前最早的数据式19950323)
    start_date = '19950101'

# 循环获取各个频率数据
ts.set_token(config.get_token())
stock_code_arr = stocks['ts_code']

# 指定字段输出顺序
cols = ['ts_code','trade_date','open','high','low','close','pre_close','change','pct_chg','vol','amount']

for freq in ['D','W','M']:
    res = pd.DataFrame()
    for ts_code in stock_code_arr:
        log.info('获取---' + str(ts_code) + '---' + freq + '---数据开始')
        df = ts.pro_bar(freq=freq, ts_code=str(ts_code),start_date=start_date)
        res = res.append(df, ignore_index=True)
        log.info('获取---' + str(ts_code) + '---' + freq + '---数据结束')
        time.sleep(0.5) #接口限制 一分钟只能访问120次
    res = res[cols]
    res.to_csv(config.get_data_dir() + 'stock_'+freq+'.csv', index=False,sep=',')

# 分时数据，接口限制一分钟只能取访问5次
# for freq in ['1MIN','5MIN','15MIN','30MIN','60MIN']:
#     res = pd.DataFrame()
#     for ts_code in stock_code_arr:
#         log.info('获取---' + str(ts_code) + '---' + freq + '---数据开始')
#         df = ts.pro_bar(freq=freq, ts_code=str(ts_code),start_date=start_date)