__author__ = 'laiyu'

from django.conf.urls import url

from . import  views
from . import common_views
from . import test_task_manager_views
from . import promble_manager_views
from . import env_setting_views
from . import browser_setting_views
from . import database_setting_views
from . import operation_setting_views
from . import function_setting_views
from . import assertion_type_setting_views
from . import global_var_setting_views
from . import project_setting_views
from . import page_element_manager_views
from . import test_case_manager_views
from . import test_plan_manager_views
from . import test_plan_case_views
from . import running_plan_manager_views
from . import test_report_views
from . import test_report_case_views
from . import test_report_case_step_views
from . import customization_interface_views



urlpatterns = [
    # 左侧导航
    url(r'^pages/nav', views.get_nav, name ='get_nav'),

    # 测试管理-测试任务管理
    url(r'^pages/testTaskManager', test_task_manager_views.test_task_manager, name='test_task_manager'),

    # 树
    url(r'^pages/nodeTree', common_views.node_tree, name='node_tree'),
    url(r'^action/updateTreeNodeName', common_views.update_tree_node_name, name='update_tree_node_name'),
    url(r'^action/appendTreeNode', common_views.append_tree_node, name='append_tree_node'),
    url(r'^action/removeTreeNode', common_views.remove_tree_node, name='remove_tree_node'),
    url(r'^action/dragTreeNode', common_views.drag_tree_node, name='drag_tree_node'),
    url(r'^action/copyTreeLeafNode', common_views.copy_tree_leaf_node, name='copy_tree_leaf_node'),

    # 获取环境，用于其它项目使用
    url(r'^action/getEnvs', common_views.get_envs, name='get_envs'),

    # 获取上次选择的项目(ID),用于展示树形结构，测试计划等
    url(r'^action/getProjectChosen', common_views.get_project_chosen, name='get_project_chosen'),

    # 存储上次选择的项目(ID),用于展示树形结构，测试计划等
    url(r'^action/storeProjectChosen', common_views.store_project_chosen, name='store_project_chosen'),

    # 根据项目类型(测试项目|UI自动化项目|接口自动化项目)，获取对应的项目
    url(r'^action/getProjects', common_views.get_projects, name='get_projects'),

    # 测试任务管理-任务概况
    url(r'^pages/testTaskOverview', test_task_manager_views.test_task_overview, name='test_task_overview'),
    url(r'^action/loadTestTasks', test_task_manager_views.load_test_tasks, name='test_tasks'),
    url(r'^action/addTestOverviewTask', test_task_manager_views.add_test_overview_task, name='add_test_overview_task'),
    url(r'^action/updateTestOverviewTask', test_task_manager_views.update_test_overview_task, name='update_test_overview_task'),
    url(r'^action/removeTask', test_task_manager_views.remove_task, name='remove_task'),

    url(r'^action/removeRow', common_views.remove_row, name='remove_row'),
    url(r'^action/moveRow', common_views.move_row, name='move_row'),

    # 测试任务管理-任务明细
    url(r'^pages/testTaskDetail', test_task_manager_views.test_task_detail, name='test_task_detail'),
    url(r'^action/addTestDetailTask', test_task_manager_views.add_test_detail_task, name='add_test_detail_task'),
    url(r'^action/updateTestDetailTask', test_task_manager_views.update_test_detail_task, name='update_test_detail_task'),

    # 测试管理-反馈问题管理
    url(r'^pages/prombleManager', promble_manager_views.promble_manager, name='promble_manager'),
    url(r'^action/loadPrombles', promble_manager_views.get_prombles, name='get_prombles'),
    url(r'^action/addPromble', promble_manager_views.add_promble, name='add_promble'),
    url(r'^action/updatePromble', promble_manager_views.update_promble, name='update_promble'),
    url(r'^action/handlePromble', promble_manager_views.handle_promble, name='handle_promble'),

    # 项目管理-UI项目配置
    url(r'^pages/UIProjectSetting', project_setting_views.ui_project_setting, name='ui_project_setting'),
    url(r'^action/loadUIProjectSettings', project_setting_views.get_ui_project_settings, name='get_ui_project_settings'),
    url(r'^action/addUIProjectSetting', project_setting_views.add_ui_project_setting, name='add_ui_project_setting'),
    url(r'^action/editUIProjectSetting', project_setting_views.edit_ui_project_setting, name='edit_ui_project_setting'),

    # 项目管理-API项目配置
    url(r'^pages/APIProjectSetting', project_setting_views.api_project_setting, name='api_project_setting'),
    url(r'^action/loadAPIProjectSettings', project_setting_views.get_api_project_settings, name='get_api_project_settings'),
    url(r'^action/addAPIProjectSetting', project_setting_views.add_api_project_setting, name='add_api_project_setting'),
    url(r'^action/editAPIProjectSetting', project_setting_views.edit_api_project_setting, name='edit_api_project_setting'),

    # 环境配置
    url(r'^pages/envSetting', env_setting_views.env_setting, name='env_setting'),
    url(r'^action/loadEnvSettings', env_setting_views.get_env_settings, name='get_env_settings'),
    url(r'^action/addEnvSetting', env_setting_views.add_env_setting, name='add_env_setting'),
    url(r'^action/editEnvSetting', env_setting_views.edit_env_setting, name='edit_env_setting'),

    # 系统配置-浏览器配置
    url(r'^pages/browserSetting', browser_setting_views.browser_setting, name='browser_setting'),
    url(r'^action/loadBrowserSettings', browser_setting_views.get_browser_settings, name='get_browser_settings'),
    url(r'^action/addBrowserSetting', browser_setting_views.add_browser_setting, name='add_browser_setting'),
    url(r'^action/editBrowserSetting', browser_setting_views.edit_browser_setting, name='edit_browser_setting'),


    # 系统配置-数据库配置
    url(r'^pages/databaseSetting', database_setting_views.database_setting, name='database_setting'),
    url(r'^action/loadDatabaseSettings', database_setting_views.get_database_settings, name='get_database_settings'),
    url(r'^action/addDatabaseSetting', database_setting_views.add_database_setting, name='add_database_setting'),
    url(r'^action/editDatabaseSetting', database_setting_views.edit_database_setting, name='edit_database_setting'),

    # 系统配置-对象可执行操作配置
    url(r'^pages/operationSetting', operation_setting_views.operation_setting, name='operation_setting'),
    url(r'^action/loadOperationSettings', operation_setting_views.get_operation_settings, name='get_operation_settings'),
    url(r'^action/addOperationSetting', operation_setting_views.add_operation_setting, name='add_operation_setting'),
    url(r'^action/editOperationSetting', operation_setting_views.edit_operation_setting, name='edit_operation_setting'),

    # 系统配置-函数配置
    url(r'^pages/functionSetting', function_setting_views.function_setting, name='function_setting'),
    url(r'^action/loadFunctionSettings', function_setting_views.get_function_settings, name='get_assertion_type_settings'),
    url(r'^action/addFunctionSetting', function_setting_views.add_function_setting, name='add_assertion_type_setting'),
    url(r'^action/editFunctionSetting', function_setting_views.edit_function_setting, name='edit_assertion_type_setting'),

    # 系统配置-断言配置
    url(r'^pages/assertionTypeSetting', assertion_type_setting_views.assertion_type_setting, name='assertion_type_setting'),
    url(r'^action/loadAssertionTypeSettings', assertion_type_setting_views.get_assertion_type_settings, name='get_assertion_type_settings'),
    url(r'^action/addAssertionTypeSetting', assertion_type_setting_views.add_assertion_type_setting, name='add_assertion_type_setting'),
    url(r'^action/editAssertionTypeSetting', assertion_type_setting_views.edit_assertion_type_setting, name='edit_assertion_type_setting'),

    # 系统配置-全局变量配置
    url(r'^pages/globalVarSetting', global_var_setting_views.global_var_setting, name='global_var_setting'),
    url(r'^action/loadGlobalVarSettings', global_var_setting_views.get_global_var_settings, name='get_global_var_settings'),
    url(r'^action/addGlobalVarSetting', global_var_setting_views.add_global_var_setting, name='add_global_var_setting'),
    url(r'^action/editGlobalVarSetting', global_var_setting_views.edit_global_var_setting, name='edit_global_var_setting'),

    # 页面元素管理
    url(r'^pages/pageElementManager', page_element_manager_views.page_element_manager, name='page_element_manager'),
    url(r'^pages/pageTreeNodePage', page_element_manager_views.page_tree_node_page, name='page_tree_node_page'),
    url(r'^action/loadPageElements', page_element_manager_views.get_page_elements, name='get_page_elements'),
    url(r'^action/addPageElement', page_element_manager_views.add_page_element, name='add_page_element'),
    url(r'^action/updatePageElement', page_element_manager_views.update_page_element, name='update_page_element'),
    url(r'^action/removePageElement', page_element_manager_views.remove_page_element, name='remove_page_element'),

    # UI测试用例管理
    url(r'^pages/UICaseManager', test_case_manager_views.ui_case_manager, name='ui_case_manager'),
    url(r'^action/UICaseTreeNodePage', test_case_manager_views.ui_case_tree_node_page, name='ui_case_tree_node_page'),
    url(r'^action/loadUICaseSteps', test_case_manager_views.get_ui_case_steps, name='load_ui_case_steps'),

    url(r'^action/getDbsForDBType', test_case_manager_views.get_dbs_for_db_obj_type, name='get_dbs_for_db_obj_type'),
    url(r'^action/getPagesForPageElements', test_case_manager_views.get_pages_for_page_elements, name='get_pages_for_page_elements'),
    url(r'^action/getPagesForCases', test_case_manager_views.get_pages_for_cases, name='get_pages_for_cases'),
    url(r'^action/getElementsForPageSelected', test_case_manager_views.get_elements_for_page_selected, name='get_elements_for_page_selected'),
    url(r'^action/getCasesForPageSelected', test_case_manager_views.get_cases_for_page_selected, name='get_cases_for_page_selected'),
    url(r'^action/getOperationsForObjectType', test_case_manager_views.get_operations_for_object_type, name='get_operations_for_object_type'),
    url(r'^action/getFuntionsForFuncType', test_case_manager_views.get_funtions_for_func_type, name='get_funtions_for_func_type'),
    url(r'^action/getAssertionsForObjectType', test_case_manager_views.get_assertions_for_op_type, name='get_assertions_for_op_type'),

    url(r'^action/addUICaseStep', test_case_manager_views.add_ui_case_step, name='add_ui_case_step'),
    url(r'^action/updateUICaseStep', test_case_manager_views.update_ui_case_step, name='update_ui_case_step'),
    url(r'^action/removeCaseStep', test_case_manager_views.remove_case_step, name='remove_case_step'),

    # 启用、禁用测试用例步骤
    url(r'^action/enableOrDisableCaseStep', test_case_manager_views.enable_or_disable_case_tep, name='enable_or_disable_case_tep'),

    #  拖拽表格中的记录行（针对测试计划用例视图表格）
    url(r'^action/dragRowOfTestCaseStep', common_views.drag_row_of_testcase_step, name='drag_row_of_testcase_step'),

    # API测试用例管理
    url(r'^pages/APICaseManager', test_case_manager_views.api_case_manager, name='api_case_manager'),
    url(r'^action/APICaseTreeNodePage', test_case_manager_views.api_case_tree_node_page, name='api_case_tree_node_page'),
    url(r'^action/loadAPICaseSteps', test_case_manager_views.get_api_case_steps, name='load_api_case_steps'),
    url(r'^action/getCasesForProject', test_case_manager_views.get_cases_for_project, name='get_cases_for_project'),

    url(r'^action/addAPICaseStep', test_case_manager_views.add_api_case_step, name='add_api_case_step'),
    url(r'^action/updateAPICaseStep', test_case_manager_views.update_api_case_step, name='update_api_case_step'),
    url(r'^action/getRedis', test_case_manager_views.get_rediss_obj, name='get_rediss_obj'),


     # UI测试计划管理
    url(r'^pages/UITestPlanManager', test_plan_manager_views.ui_test_plan_manager, name='ui_test_plan_manager'),
    url(r'^action/getUITestPlans', test_plan_manager_views.get_ui_test_plans, name='get_ui_test_plans'),

    url(r'^action/getBrowsersForUITestPlan', test_plan_manager_views.get_browsers_for_ui_test_plan, name='get_browsers_for_ui_test_plan'),

    url(r'^action/addUITestPlan', test_plan_manager_views.add_ui_test_plan, name='add_ui_test_plan'),
    url(r'^action/updateUITestPlan', test_plan_manager_views.update_ui_test_plan, name='update_ui_test_plan'),

    # API测试计划管理
    url(r'^pages/APITestPlanManager', test_plan_manager_views.api_test_plan_manager, name='api_test_plan_manager'),
    url(r'^action/getAPITestPlans', test_plan_manager_views.get_api_test_plans, name='get_api_test_plans'),
    url(r'^action/addAPITestPlan', test_plan_manager_views.add_api_test_plan, name='add_api_test_plan'),
    url(r'^action/updateAPITestPlan', test_plan_manager_views.update_api_test_plan, name='update_api_test_plan'),

    # 关联计划和测试用例
    url(r'^action/correlateTestplanAndTestcase', test_plan_manager_views.correlate_testplan_and_testcase, name='correlate_testplan_and_testcase'),
    # 获取和测试计划关联的用例树节点
    url(r'^pages/testplanCaseTreeNodes', test_plan_manager_views.get_test_plan_case_tree_nodes, name='get_test_plan_case_tree_nodes'),

    # 以datagrid的方式查看和测试计划关联的用例列表
    url(r'^pages/UITestPlanCaseView', test_plan_case_views.ui_test_plan_case_view, name='viewUITestPlanCases'),
    url(r'^pages/APITestPlanCaseView', test_plan_case_views.api_test_plan_case_view, name='viewAPITestPlanCases'),

    url(r'^action/loadTestPlanCases', test_plan_case_views.load_test_plan_cases, name='load_test_plan_cases'),
    url(r'^action/putRowTopOrBottom', test_plan_case_views.put_row_top_or_bottom, name='put_row_top_or_bottom'),
    # url(r'^action/removeTestPlanCase', test_plan_case_views.remove_testplan_case, name='remove_testplan_case'),
    # 重新调整同测试计划关联的用例顺序值
    url(r'^action/reOrderRows', test_plan_case_views.reorder_rows, name='reorder_rows'),

    #  拖拽表格中的记录行（针对测试计划用例视图表格）
    url(r'^action/dragRowOfTestPlanCaseView', common_views.drag_row_of_testplan_case_view, name='drag_row_of_testplan_case_view'),


    # 运行计划管理
    url(r'^pages/runningPlanManager', running_plan_manager_views.running_plan_manager, name='running_plan_manager'),
    url(r'^action/getRunningPlans', running_plan_manager_views.get_running_plans, name='running_plan_manager'),
    url(r'^action/addRunningPlan', running_plan_manager_views.add_running_plan, name='add_running_plan'),
    url(r'^action/updateRunningPlan', running_plan_manager_views.update_running_plan, name='update_running_plan'),
    url(r'^action/execRunningPlan', running_plan_manager_views.exec_running_plan, name='exec_running_plan'),
    url(r'^action/resetRunningPlanStatus', running_plan_manager_views.reset_running_plan_status, name='reset_running_plan_status'),



    # 根据项目类型(测试项目|UI自动化项目|接口自动化项目)，项目ID，获取获取对应的测试计划
    url(r'^action/getPlans', common_views.get_plans, name='get_plans'),

    # UI测试报告--测试概况
    url(r'^pages/UITestReport.html', test_report_views.ui_test_report, name='ui_test_report'),
    url(r'^action/loadTestReportForSummary', test_report_views.get_test_report_for_summary, name='test_report_for_summary'),

    ## 测试报告--测试概况-查看详情，即用例执行明细
    url(r'^pages/testReportCaseView', test_report_case_views.test_report_cases_view, name='ui_test_report_cases_view'),
    url(r'^action/loadTestReportCases', test_report_case_views.get_test_report_cases, name='get_test_report_cases'),

    ## UI测试报告--测试概况-查看详情-用例执行明细-查看详情，即步骤执行明细
    url(r'^pages/testReportCaseStepView', test_report_case_step_views.test_report_case_step_view, name='ui_test_report_case_step_view'),
    url(r'^action/loadTestReportCaseSteps', test_report_case_step_views.get_test_report_case_steps, name='get_test_report_case_steps'),

    # API测试报告--测试概况
    url(r'^pages/APITestReport.html', test_report_views.api_test_report, name='api_test_report'),
    url(r'^pages/postjson', views.testpost, name='index2'),

    # 定制化接口
    # 忘记密码 - 获取手机号验证码
    url(r'^action/getResetPasswordMobileVarifyCode', customization_interface_views.get_reset_password_mobile_varify_code, name='get_reset_password_mobile_varify_code'),

    # 忘记密码 - 重置手机号发送验证码次数
    url(r'^action/resetResetPwdMobileVarifyCodeNum', customization_interface_views.reset_resetpwd_mobile_varify_code_num, name='reset_resetpwd_mobile_varify_code_num'),

    # 注册 - 重置手机号验证码发送次数
    url(r'^action/resetRegisterMobileCodeSendNum', customization_interface_views.reset_register_mobile_code_send_num, name='reset_register_mobile_code_send_num'),

    # 注册 - 获取手机验证码
    url(r'^action/getRegisterMobileCode', customization_interface_views.get_register_mobile_code, name='get_register_mobile_code'),

    # 获取时间和日期
    url(r'^action/getDateAndTime', customization_interface_views.get_date_and_time, name='get_date_and_time'),
    url(r'^$', views.index, name='index')
]
