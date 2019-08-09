CREATE TABLE `hk_stock` (
  `secid` varchar(100) DEFAULT NULL COMMENT '唯一id',
  `market` varchar(50) DEFAULT NULL COMMENT '市场代码',
  `stock_code` varchar(50) DEFAULT NULL COMMENT '股票代码',
  `stock_name` varchar(100) DEFAULT NULL COMMENT '股票名称',
  UNIQUE KEY `secid` (`secid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='港股股票列表';