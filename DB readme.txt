CREATE TABLE `myorder` (
  `order_id` varchar(50) COLLATE utf8_bin NOT NULL,
  `start_time` int COLLATE utf8_bin NOT NULL,
  `end_time` int COLLATE utf8_bin NOT NULL,
  `start_longitude` double COLLATE utf8_bin NOT NULL,
  `start_latitude` double COLLATE utf8_bin NOT NULL,
  `end_longitude` double COLLATE utf8_bin NOT NULL,
  `end_latitude` double COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `订单id` (`order_id`) USING BTREE,
  KEY `上车时间` (`start_time`) USING BTREE,
  KEY `上车地点` (`start_longitude`,`start_latitude`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE `position` (
  `driver_id` varchar(50) NOT NULL,
  `order_id` varchar(50) NOT NULL,
  `time_stamp` int NOT NULL,
  `longitude` double NOT NULL,
  `latitude` double NOT NULL,
  PRIMARY KEY (`time_stamp`,`order_id`) USING BTREE,
  KEY `订单id` (`order_id`) USING BTREE,
  KEY `司机id` (`driver_id`) USING BTREE,
  KEY `时间` (`time_stamp`) USING BTREE,
  KEY `位置` (`longitude`,`latitude`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



load data infile “F:\\wamp\\tmp\\position" into table position fields terminated by ',';
load data infile “F:\\wamp\\tmp\\myorder" ignore into table myorder fields terminated by ',';
