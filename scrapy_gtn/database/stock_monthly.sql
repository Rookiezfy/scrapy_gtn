CREATE TABLE `stock_monthly` (
  `ts_code` varchar(255) DEFAULT NULL COMMENT '股票代码',
  `trade_date` varchar(255) DEFAULT NULL COMMENT '交易日期',
  `open` decimal(40,2) DEFAULT NULL COMMENT '开盘价',
  `high` decimal(40,2) DEFAULT NULL COMMENT '最高价',
  `low` decimal(40,2) DEFAULT NULL COMMENT '最低价',
  `close` decimal(40,2) DEFAULT NULL COMMENT '收盘价',
  `pre_close` decimal(40,2) DEFAULT NULL COMMENT '昨收价',
  `change` decimal(40,2) DEFAULT NULL COMMENT '涨跌额',
  `pct_chg` decimal(40,2) DEFAULT NULL COMMENT '涨跌幅(复权)',
  `vol` decimal(40,2) DEFAULT NULL COMMENT '成交量(手)',
  `amount` decimal(40,2) DEFAULT NULL COMMENT '成交额(千元)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='月线行情';

