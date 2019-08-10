CREATE TABLE `rt_stock_5min` (
  `secid` varchar(100) NOT NULL COMMENT '唯一id',
  `market` varchar(50) NOT NULL COMMENT '市场代码',
  `stock_code` varchar(50) NOT NULL COMMENT '股票代码',
  `stock_name` varchar(100) NOT NULL COMMENT '股票名称',
  `trade_date` varchar(255) NOT NULL COMMENT '交易日期',
  `trade_time` varchar(255) NOT NULL COMMENT '交易时间',
  `open_px` decimal(40,4) DEFAULT NULL COMMENT '开盘价',
  `high_px` decimal(40,4) DEFAULT NULL COMMENT '最高价',
  `low_px` decimal(40,4) DEFAULT NULL COMMENT '最低价',
  `close_px` decimal(40,4) DEFAULT NULL COMMENT '收盘价',
  `business_amount` decimal(40,4) DEFAULT NULL COMMENT '成交量',
  `business_balance` decimal(40,4) DEFAULT NULL COMMENT '成交额(元)',
  `last_upd_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`secid`,`trade_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='5分钟线行情(爬虫)';

