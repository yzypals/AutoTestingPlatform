# 创建数据库
CREATE DATABASE testplatform  DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

# 初始化导航
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('1','测试管理','0','','icon-person','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('2','测试任务管理','1','/pages/testTaskManager.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('3','反馈问题管理','1','/pages/prombleManager.html','icon-set','3');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('20','项目管理','0','','icon-sys-set','20');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('21','UI项目配置','20','/pages/UIProjectSetting.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('22','API项目配置','20','/pages/APIProjectSetting.html','icon-set','2');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('23','测试项目配置','20','/pages/TestProjectSetting.html','icon-set','3');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('40','系统配置','0','','icon-sys-set','40');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('41','环境配置','40','/pages/envSetting.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('42','浏览器配置','40','/pages/browserSetting.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('43','数据库配置','40','/pages/databaseSetting.html','icon-set','2');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('44','操作配置','40','/pages/operationSetting.html','icon-set','3');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('45','函数配置','40','/pages/functionSetting.html','icon-set','4');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('46','断言配置','40','/pages/assertionTypeSetting.html','icon-set','5');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('47','全局变量配置','40','/pages/globalVarSetting.html','icon-set','6');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('60','页面元素管理','0','','icon-sys-set','60');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('61','页面元素管理','60','/pages/pageElementManager.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('80','测试用例管理','0','','icon-sys-set','80');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('81','UI测试用例管理','80','/pages/UICaseManager.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('82','API测试用例管理','80','/pages/APICaseManager.html','icon-set','2');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('100','测试计划管理','0','','icon-sys-set','100');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('101','UI测试计划','100','/pages/UITestPlanManager.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('102','API测试计划','100','/pages/APITestPlanManager.html','icon-set','2');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('120','运行计划管理','0','','icon-sys-set','120');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('121','运行计划','120','/pages/runningPlanManager.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('140','测试报告','0','','icon-sys-set','140');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('141','UI测试报告','140','/pages/UITestReport.html','icon-set','1');
insert into `website_navigation` (`id`, `menu_name`, `parent_id`, `url`, `icon`, `order`) values('142','API测试报告','140','/pages/APITestReport.html','icon-set','2');

# 环境配置
insert into `website_env_setting` (`id`, `env`, `order`) values('1','测试环境','1');
insert into `website_env_setting` (`id`, `env`, `order`) values('2','开发环境','2');

# 初始化浏览器配置
insert into `website_browser_setting` (`id`, `browser`, `order`) values('1','谷歌','1');
insert into `website_browser_setting` (`id`, `browser`, `order`) values('2','IE','2');
insert into `website_browser_setting` (`id`, `browser`, `order`) values('3','火狐','3');

# 初始化接口断言配置(未经过json格式化)
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('1','接口请求操作','包含成员','[\n{\"模式\":\"\\\"success\\\"\",\n\"消息\":\"fail#返回结果不中包含英文双引号包含的success\"\n},\n{\n\"模式\":\"status:1\",\n\"消息\":\"fail#返回结果不中包含status:1\"}\n]','1');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('2','接口请求操作','不包含成员','[\n{\"模式\":\"\\\"success\\\"\",\"消息\":\"fail#返回结果包含英文双引号包含的success\"\n},\n{\"模式\":\"status:1\",\"消息\":\"fail#返回结果包含status:1\"}\n]','2');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('3','接口请求操作','包含字符串','[\n{\n\"模式\":\"\\\"success\\\":true\",\n\"消息\":\"fail#success不为True\"\n},\n{\n\"模式\":\"\\\"success\\\":false\",\n\"消息\":\"fail#success不为false\"\n}\n]','3');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('4','接口请求操作','不包含字符串','[\n{\n\"模式\":\"\\\"success\\\":true\",\n\"消息\":\"fail#success为True\"\n},\n{\n\"模式\":\"\\\"success\\\":false\",\n\"消息\":\"fail#success为false\"\n}\n]','4');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('5','接口请求操作','键值相等','[\n{\"模式\":{\"key1\":true},\"消息\":\"fail#key1的值不为true\"\n},{\"模式\":{\"key2\":{\"key3\":\"value\"}},\"消息\":\"fail#key3的值不为value\"\n}\n]','5');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('6','接口请求操作','匹配正则表达式','[\n{\"模式\":\"regex1\",\"消息\":\"fail#不符合断言时返回的消息\"\n},{\"模式\":\"regex2\",\"消息\":\"fail#不符合断言时返回的消息\"\n},{\"模式\":\"regexN\",\"消息\":\"fail#不符合断言时返回的消息\"\n}\n]','6');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('7','接口请求操作','不匹配正则表达式','[\n{\n\"模式\":\"regex1\",\n\"消息\":\"fail#不符合断言时返回的消息\"},{\n\"模式\":\"regex2\",\n\"消息\":\"fail#不符合断言时返回的消息\"\n},\n{\n\"模式\":\"regexN\",\n\"消息\":\"fail#不符合断言时返回的消息\"}\n]','7');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('8','接口请求操作','完全匹配字典','[\n{\"模式\":{\n\"key1\":\"str\",\n\"key2\":1\n},\n\"消息\":\"fail#返回内容不完全匹配字典时抛出的消息\"}\n]','8');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('9','接口请求操作','完全匹配列表','[\n{\n\"模式\":[\n1,\n2,\n3,\n\"str\"\n],\"消息\":\"fail#返回内容不完全匹配列表时抛出的消息\"\n}\n]','9');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('10','接口请求操作','完全匹配集合','[\n{\n\"模式\":\"{1,2,\\\"str\\\"}\",\"消息\":\"fail#返回内容不完全匹配集合时抛出的消息\"}\n]','10');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('11','接口请求操作','完全匹配元组','[\n{\n\"模式\":\"(1,2,\\\"str\\\")\",\n\"消息\":\"fail#返回内容不完全匹配元组时抛出的消息\"\n}\n]','11');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('12','接口请求操作','xpath断言','[\n{\n\"模式\":{\"xpath表达式1\":\"期望值\",\n\"xpath表达式2\":\"期望值\"\n},\n\"消息\":\"fail#不符合断言时抛出的消息\"\n},{\"模式\":{\"xpath表达式2\":\"期望值\"\n},\"消息\":\"fail#不符合断言时抛出的消息\"\n},{\"模式\":{\"xpath表达式N\":\"期望值\"\n},\"消息\":\"fail#不符合断言时抛出的消息\"\n}\n]','12');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('13','数据库操作','db列值相等','[\n{\"模式\":[\n\"获取的列值(期望值)\",\n\"期望值(获取的列值)\"\n],\"消息\":\"fail#比较值不等于期望值时抛出的消息\"\n}\n]','13');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('14','数据库操作','db列值不相等','[\n{\"模式\":[\"获取的列值\",\"期望值(获取的列值)\"],\"消息\":\"fail#比较值等于期望值时抛出的消息\"\n}\n]','14');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('15','页面操作','存在元素','xpath=//div/nav[2]/ul/li[1]/a','15');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('16','页面操作','页面标题包含','目标字符串','16');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('17','页面操作','页面标题等于','页面标题','17');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('18','页面操作','页面url包含','目标字符串','18');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('19','页面操作','页面url等于','http://10.202.95.88:8080/page/platform/home.html','19');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('20','页面操作','元素文本包含','目标字符串','20');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('21','页面操作','元素文本等于','元素文本','21');

# 初始化接口断言配置(经过json格式化)
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('1','接口请求操作','包含成员','[\n  {\n    \"模式\": \"\\\"success\\\"\",\n    \"消息\": \"fail#返回结果不中包含英文双引号包含的success\"\n  },\n  {\n    \"模式\": \"status:1\",\n    \"消息\": \"fail#返回结果不中包含status:1\"\n  }\n]','1');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('2','接口请求操作','不包含成员','[\n  {\n    \"模式\": \"\\\"success\\\"\",\n    \"消息\": \"fail#返回结果包含英文双引号包含的success\"\n  },\n  {\n    \"模式\": \"status:1\",\n    \"消息\": \"fail#返回结果包含status:1\"\n  }\n]','2');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('3','接口请求操作','包含字符串','[\n  {\n    \"模式\": \"\\\"success\\\":true\",\n    \"消息\": \"fail#success不为True\"\n  },\n  {\n    \"模式\": \"\\\"success\\\":false\",\n    \"消息\": \"fail#success不为false\"\n  }\n]','3');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('4','接口请求操作','不包含字符串','[\n  {\n    \"模式\": \"\\\"success\\\":true\",\n    \"消息\": \"fail#success为True\"\n  },\n  {\n    \"模式\": \"\\\"success\\\":false\",\n    \"消息\": \"fail#success为false\"\n  }\n]','4');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('5','接口请求操作','键值相等','[\n  {\n    \"模式\": {\n      \"key1\": true\n    },\n    \"消息\": \"fail#key1的值不为true\"\n  },\n  {\n    \"模式\": {\n      \"key2\": {\n        \"key3\": \"value\"\n      }\n    },\n    \"消息\": \"fail#key3的值不为value\"\n  }\n]','5');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('6','接口请求操作','匹配正则表达式','[\n  {\n    \"模式\": \"regex1\",\n    \"消息\": \"fail#不符合断言时返回的消息\"\n  },\n  {\n    \"模式\": \"regex2\",\n    \"消息\": \"fail#不符合断言时返回的消息\"\n  },\n  {\n    \"模式\": \"regexN\",\n    \"消息\": \"fail#不符合断言时返回的消息\"\n  }\n]','6');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('7','接口请求操作','不匹配正则表达式','[\n  {\n    \"模式\": \"regex1\",\n    \"消息\": \"fail#不符合断言时返回的消息\"\n  },\n  {\n    \"模式\": \"regex2\",\n    \"消息\": \"fail#不符合断言时返回的消息\"\n  },\n  {\n    \"模式\": \"regexN\",\n    \"消息\": \"fail#不符合断言时返回的消息\"\n  }\n]','7');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('8','接口请求操作','完全匹配字典','[\n  {\n    \"模式\": {\n      \"key1\": \"str\",\n      \"key2\": 1\n    },\n    \"消息\": \"fail#返回内容不完全匹配字典时抛出的消息\"\n  }\n]','8');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('9','接口请求操作','完全匹配列表','[\n  {\n    \"模式\": [\n      1,\n      2,\n      3,\n      \"str\"\n    ],\n    \"消息\": \"fail#返回内容不完全匹配列表时抛出的消息\"\n  }\n]','9');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('10','接口请求操作','完全匹配集合','[\n  {\n    \"模式\": \"{1,2,\\\"str\\\"}\",\n    \"消息\": \"fail#返回内容不完全匹配集合时抛出的消息\"\n  }\n]','10');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('11','接口请求操作','完全匹配元组','[\n  {\n    \"模式\": \"(1,2,\\\"str\\\")\",\n    \"消息\": \"fail#返回内容不完全匹配元组时抛出的消息\"\n  }\n]','11');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('12','接口请求操作','xpath断言','[\n  {\n    \"模式\": {\n      \"xpath表达式1\": \"期望值\",\n      \"xpath表达式2\": \"期望值\"\n    },\n    \"消息\": \"fail#不符合断言时抛出的消息\"\n  },\n  {\n    \"模式\": {\n      \"xpath表达式2\": \"期望值\"\n    },\n    \"消息\": \"fail#不符合断言时抛出的消息\"\n  },\n  {\n    \"模式\": {\n      \"xpath表达式N\": \"期望值\"\n    },\n    \"消息\": \"fail#不符合断言时抛出的消息\"\n  }\n]','12');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('13','数据库操作','db列值相等','[\n  {\n    \"模式\": [\n      \"获取的列值(期望值)\",\n      \"期望值(获取的列值)\"\n    ],\n    \"消息\": \"fail#比较值不等于期望值时抛出的消息\"\n  }\n]','13');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('14','数据库操作','db列值不相等','[\n  {\n    \"模式\": [\n      \"获取的列值\",\n      \"期望值(获取的列值)\"\n    ],\n    \"消息\": \"fail#比较值等于期望值时抛出的消息\"\n  }\n]','14');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('15','页面操作','存在元素','xpath=//div/nav[2]/ul/li[1]/a','15');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('16','页面操作','页面标题包含','目标字符串','16');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('17','页面操作','页面标题等于','页面标题','17');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('18','页面操作','页面url包含','目标字符串','18');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('19','页面操作','页面url等于','http://10.202.95.88:8080/page/platform/home.html','19');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('20','页面操作','元素文本包含','目标字符串','20');
insert into `website_assertion_type_setting` (`id`, `op_type`, `assertion_type`, `assertion_pattern`, `order`) values('21','页面操作','元素文本等于','元素文本','21');



# 初始化操作配置
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('1','数据库','select_one_record','1');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('2','数据库','update_record','2');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('3','数据库','delete_record','3');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('4','数据库','truncate_table','4');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('5','数据库','call_proc','5');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('6','数据库','insert_record','6');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('7','页面元素','输入','7');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('8','页面元素','清空','8');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('9','页面元素','点击','9');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('10','页面元素','鼠标移动到','10');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('11','页面元素','拖动滚动条至元素可见','11');
insert into `website_operation_for_object` (`id`, `object_type`, `operation`, `order`) values('12','Redis','set_key_value','12');

# 创建索引
CREATE INDEX test_task_detail_page_id ON website_test_task_detail(page_id);
CREATE INDEX test_task_overview_page_id ON website_test_task_overview(page_id);
CREATE INDEX promble_feedback_order ON website_promble_feedback(`order`);

CREATE INDEX navigation_order ON website_navigation(`order`);
CREATE INDEX navigation_oparent_id ON website_navigation(parent_id);

CREATE INDEX idx_api_planid_subnodenum_order ON website_api_case_tree_test_plan(plan_id, sub_node_num, `order`);
CREATE INDEX idx_api_parentid_projectid_order ON `website_api_case_tree`(parent_id, project_id, `order`);
CREATE INDEX idx_api_execution_num_planid_runresult ON `website_api_test_report_for_case`(execution_num, plan_id, `run_result`);
CREATE INDEX idx_api_planid_subnode_num_order ON `website_api_case_tree_test_plan`(plan_id, sub_node_num, `order`);

# 初始化函数配置
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('1','智能等待','5','1','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('2','死等待','5','2','所有项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('3','切换至窗口ByName','目标窗口的窗口名称','3','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('4','切换至窗口ByPageTitle','目标窗口的当前页面标题','4','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('5','切换至窗口ByUrl','目标窗口的当前访问的URL','5','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('6','关闭当前窗口','','6','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('7','跳转到URL','/page/platform/home.html','7','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('8','浏览器前进','','8','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('9','浏览器后退','','9','UI项目');
insert into `website_function_setting` (`id`, `function_name`, `param_style`, `order`, `project_type`) values('10','拖动垂直滚动条','顶部  or  底部','10','UI项目');

# 注意：这里的5，意为5秒


# 创建触发器

# 删除环境配置时，如果UI、API项目配置表|数据库配置表引用了该项目，则不让删除（全局变量配置表也引用了环境配置，但是这里不做校验）
DROP TRIGGER IF EXISTS trigger_on_env_setting_delete;
DELIMITER //
CREATE TRIGGER trigger_on_env_setting_delete 
BEFORE DELETE ON `website_env_setting`
FOR EACH ROW
BEGIN
   IF old.id IN (SELECT environment_id FROM `website_ui_project_setting`)
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[UI项目配置]引用' ;  
   ELSEIF old.id IN (SELECT environment_id FROM `website_api_project_setting`)
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[API项目配置]引用';
   ELSEIF old.id IN (SELECT environment_id FROM `website_database_setting`)
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[数据库配置]引用';
   END IF;   
END;
//
DELIMITER ;



# 删除UI项目配置时，如果数据库配置表|全局变量配置表|运行计划表引用了该项目，则不让删除，否则所选项目表中对应的记录
DROP TRIGGER IF EXISTS trigger_on_ui_project_setting_delete;
DELIMITER //
CREATE TRIGGER trigger_on_ui_project_setting_delete 
BEFORE DELETE ON `website_ui_project_setting`
FOR EACH ROW
BEGIN
   IF old.id IN (SELECT project_id FROM `website_database_setting` WHERE project_type='UI项目')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[数据库配置]引用' ;  
   ELSEIF old.id IN (SELECT project_id FROM `website_global_variable_setting` WHERE project_type='UI项目')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[全局变量配置]引用';
   ELSEIF old.id IN (SELECT project_id FROM `website_running_plan` WHERE project_type='UI项目')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[运行计划]引用';
   ELSE
       DELETE FROM `website_project_chosen` WHERE tree_type IN ('UICaseTree', 'PlanUICaseTree') AND project_id = old.id;
   END IF;   
   
END;
//
DELIMITER ;

# 删除API项目配置时，如果数据库配置表|全局变量配置表|运行计划表引用了该项目，则不让删除，否则所选项目表中对应的记录
DROP TRIGGER IF EXISTS trigger_on_api_project_setting_delete;
DELIMITER //
CREATE TRIGGER trigger_on_api_project_setting_delete 
BEFORE DELETE ON `website_api_project_setting`
FOR EACH ROW
BEGIN
   IF old.id IN (SELECT project_id FROM `website_database_setting` WHERE project_type='API项目')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[数据库配置]引用' ;  
   ELSEIF old.id IN (SELECT project_id FROM `website_global_variable_setting` WHERE project_type='API项目')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[全局变量配置]引用';
   ELSEIF old.id IN (SELECT project_id FROM `website_running_plan` WHERE project_type='API项目')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[运行计划]引用';
   ELSE
       DELETE FROM `website_project_chosen` WHERE tree_type IN ('APICaseTree', 'PlanAPICaseTree') AND project_id = old.id;
   END IF;   
   
END;
//
DELIMITER ;

# 删除测试项目配置时，级联删除所选项目表
DROP TRIGGER IF EXISTS trigger_on_api_project_setting_delete;
DELIMITER //
CREATE TRIGGER trigger_on_api_project_setting_delete 
BEFORE DELETE ON `website_api_project_setting`
FOR EACH ROW
BEGIN
   DELETE FROM `website_project_chosen` WHERE tree_type = 'SprintTree' AND project_id = old.id;   
END;
//
DELIMITER ;

# 删除数据库配置时，如果用例详情表即用例步骤引用了该数据库配置，则不让删除
DROP TRIGGER IF EXISTS trigger_on_database_setting_delete;
DELIMITER //
CREATE TRIGGER trigger_on_database_setting_delete 
BEFORE DELETE ON `website_database_setting`
FOR EACH ROW
BEGIN
   IF old.id IN (SELECT object_id FROM `website_ui_test_case_step` WHERE object_type='数据库')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[UI测试用例管理-用例详情]引用' ; 	  
   ELSEIF old.id IN (SELECT object_id FROM `website_api_test_case_step` WHERE step_type='操作数据库')
      THEN
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[API测试用例管理-用例详情]引用' ; 
   END IF;
END;
//
DELIMITER ;



# 删除函数配置时，如果用例详情表即用例步骤引用了该函数，则不让删除
DROP TRIGGER IF EXISTS trigger_on_function_setting_delete;
DELIMITER //
CREATE TRIGGER trigger_on_function_setting_delete 
BEFORE DELETE ON `website_function_setting`
FOR EACH ROW
BEGIN
   IF old.id IN (SELECT object_id FROM `website_ui_test_case_step` WHERE object_type='系统函数')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[UI测试用例管理-用例详情]引用' ; 
   ELSEIF old.id IN (SELECT object_id FROM `website_api_test_case_step` WHERE step_type='操作数据库')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[API测试用例管理-用例详情]引用' ; 
   END IF;
END;
//
DELIMITER ;


# 删除页面元素，如果用例详情表即用例步骤引用了该页面元素，则不让删除
DROP TRIGGER IF EXISTS trigger_on_page_element_delete;
DELIMITER //
CREATE TRIGGER trigger_on_page_element_delete 
BEFORE DELETE ON `website_page_element`
FOR EACH ROW
BEGIN
   IF old.id IN (SELECT object_id FROM `website_ui_test_case_step` WHERE object_type='页面元素')
      THEN  
          SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[UI测试用例管理-用例详情]引用' ;  
   END IF;
END;
//
DELIMITER ;

# 修改测试用例即用例树节点，如果测试用例计划关联表引用了该用例，则修改计划关联表中对应的用例名称
DROP TRIGGER IF EXISTS trigger_on_ui_case_tree_update;
DELIMITER //
CREATE TRIGGER trigger_on_ui_case_tree_update 
AFTER UPDATE ON `website_ui_case_tree`
FOR EACH ROW
BEGIN
    UPDATE `website_ui_case_tree_test_plan` SET node_name=new.text WHERE node_id=old.id;  
END;
//
DELIMITER ;


DROP TRIGGER IF EXISTS trigger_on_api_case_tree_update;
DELIMITER //
CREATE TRIGGER trigger_on_api_case_tree_update 
AFTER UPDATE ON `website_api_case_tree`
FOR EACH ROW
BEGIN
    UPDATE `website_api_case_tree_test_plan` SET node_name=new.text WHERE node_id=old.id;  
END;
//
DELIMITER ;


# 删除API|UI测试计划，如果运行计划表即引用了该测试计划，则不让删除;
# 删除API|UI测试计划，一并删除和它相关联的用例
DROP TRIGGER IF EXISTS trigger_on_ui_test_plan_delete;
DELIMITER //
CREATE TRIGGER trigger_on_ui_test_plan_delete 
BEFORE DELETE ON `website_ui_test_plan`
FOR EACH ROW
BEGIN
   IF (SELECT id FROM `website_running_plan` WHERE FIND_IN_SET(old.id, plan_id))
   THEN 
       SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[运行计划管理-运行计划]引用' ; 
   ELSE
       DELETE FROM `website_ui_case_tree_test_plan` WHERE plan_id = old.id;
   END IF;
   
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS trigger_on_api_test_plan_delete;
DELIMITER //
CREATE TRIGGER trigger_on_api_test_plan_delete 
BEFORE DELETE ON `website_api_test_plan`
FOR EACH ROW
BEGIN
   IF (SELECT id FROM `website_running_plan` WHERE FIND_IN_SET(old.id, plan_id))
   THEN 
       SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = '该记录已被[运行计划管理-运行计划]引用' ; 
   ELSE
       DELETE FROM `website_api_case_tree_test_plan` WHERE plan_id = old.id;
   END IF;
   
END;
//
DELIMITER ;

# 删除测试报告-测试概况记录，级联删除与报告关联的测试用例及测试用例对应的测试步骤
DROP TRIGGER IF EXISTS trigger_on_website_ui_test_report_for_summary_delete;
DELIMITER //
CREATE TRIGGER trigger_on_website_ui_test_report_for_summary_delete 
BEFORE DELETE ON `website_ui_test_report_for_summary`
FOR EACH ROW
BEGIN
   DELETE FROM `website_ui_test_report_for_case_step` WHERE execution_num = old.execution_num;
   DELETE FROM `website_ui_test_report_for_case` WHERE execution_num = old.execution_num;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS trigger_on_website_api_test_report_for_summary_delete;
DELIMITER //
CREATE TRIGGER trigger_on_website_api_test_report_for_summary_delete 
BEFORE DELETE ON `website_api_test_report_for_summary`
FOR EACH ROW
BEGIN
   DELETE FROM `website_api_test_report_for_case_step` WHERE execution_num = old.execution_num;
   DELETE FROM `website_api_test_report_for_case` WHERE execution_num = old.execution_num;
END;
//
DELIMITER ;

# 删除测试报告-测试用例明细，级联删除与测试用例关联的测试步骤
DROP TRIGGER IF EXISTS trigger_on_website_ui_test_report_for_case_delete;
DELIMITER //
CREATE TRIGGER trigger_on_website_ui_test_report_for_case_delete 
BEFORE DELETE ON `website_ui_test_report_for_case`
FOR EACH ROW
BEGIN
   DELETE FROM `website_ui_test_report_for_case_step` WHERE execution_num = old.execution_num AND case_id=old.case_id;
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS trigger_on_website_api_test_report_for_case_delete;
DELIMITER //
CREATE TRIGGER trigger_on_website_api_test_report_for_case_delete 
BEFORE DELETE ON `website_api_test_report_for_case`
FOR EACH ROW
BEGIN
   DELETE FROM `website_api_test_report_for_case_step` WHERE execution_num = old.execution_num AND case_id=old.case_id;
END;
//
DELIMITER ;

#注意：更新、删除浏览器配置，不影响UI测试计划表已创建的计划
#注意：更新、删除操作配置|断言配置，不影响用例详情表已填写步骤
#注意：更新、删除操作配置|断言配置，不影响用例详情表已填写步骤
#注意：更新计划名称，不会修改运行计划表已新增计划的测试计划名称

# 往用例详执行明细表插入数据时，更新对应用例步骤执行明细表的run_id
DROP TRIGGER IF EXISTS trigger_on_api_test_report_for_case_insert;
DELIMITER //
CREATE TRIGGER trigger_on_api_test_report_for_case_insert 
AFTER INSERT ON `website_api_test_report_for_case`
FOR EACH ROW
BEGIN
UPDATE `website_api_test_report_for_case_step` SET run_id = new.id WHERE case_id = new.case_id AND run_id = 0; 
END;
//
DELIMITER ;


DROP TRIGGER IF EXISTS trigger_on_ui_test_report_for_case_insert;
DELIMITER //
CREATE TRIGGER trigger_on_ui_test_report_for_case_insert 
AFTER INSERT ON `website_ui_test_report_for_case`
FOR EACH ROW
BEGIN
UPDATE `website_ui_test_report_for_case_step` SET run_id = new.id WHERE case_id = new.case_id AND run_id = 0; 
END;
//
DELIMITER ;




