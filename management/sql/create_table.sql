CREATE TABLE `test_results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_group_name` varchar(256) NOT NULL,
  `result_status` varchar(4) NOT NULL,
  `number_of_passed_tests` int(11) NOT NULL,
  `number_of_failed_tests` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `created_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`result_status`,`test_group_name`,`created_date`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
