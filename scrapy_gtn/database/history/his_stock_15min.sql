CREATE TABLE `his_stock_15min` (
  `ts_code` varchar(255) DEFAULT NULL COMMENT '股票代码',
  `trade_date` varchar(255) DEFAULT NULL COMMENT '交易日期',
  `trade_time` varchar(255) DEFAULT NULL COMMENT '交易时间',
  `open` decimal(40,2) DEFAULT NULL COMMENT '开盘价',
  `high` decimal(40,2) DEFAULT NULL COMMENT '最高价',
  `low` decimal(40,2) DEFAULT NULL COMMENT '最低价',
  `close` decimal(40,2) DEFAULT NULL COMMENT '收盘价',
  `pre_close` decimal(40,2) DEFAULT NULL COMMENT '昨收价',
  `vol` decimal(40,2) DEFAULT NULL COMMENT '成交量(手)',
  `amount` decimal(40,2) DEFAULT NULL COMMENT '成交额(千元)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='15分钟线行情(tushare)';