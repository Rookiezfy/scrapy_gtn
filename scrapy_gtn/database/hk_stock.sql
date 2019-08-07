CREATE TABLE `hk_stock` (
  `secid` varchar(255) DEFAULT NULL COMMENT '股票市场代码',
  `code` varchar(255) DEFAULT NULL COMMENT '股票代码',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `market` varchar(255) DEFAULT NULL COMMENT '市场编号',
  UNIQUE KEY `secid` (`secid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='港股股票列表';