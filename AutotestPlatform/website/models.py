from django.db import models

# Create your models here.

# 导航栏
class Navigation(models.Model):
    id = models.IntegerField(primary_key=True) # ID
    menu_name = models.CharField(max_length=20) # 菜单名称
    parent_id = models.IntegerField()  # 父级菜单ID
    url = models.CharField(max_length=500) # 菜单URL
    icon = models.CharField(max_length=15) # 菜单图标名称
    order = models.IntegerField()  # 菜单排序


# 测试项目配置
class Test_project_setting(models.Model):
    id = models.AutoField(primary_key=True)            # ID, 主键
    project_name = models.CharField(max_length=50)      # 项目名称
    valid_flag = models.CharField(max_length=5)         # 是否启用标识（启用|禁用）
    order = models.IntegerField()                       # 顺序


# 存放不同树中选择的项目，作为默认项目
class Project_chosen(models.Model):
    id = models.AutoField(primary_key=True)
    project_id = models.IntegerField()             # 选择的项目ID
    project_name = models.CharField(max_length=50) # 选择的项目名称
    tree_type = models.CharField(max_length=20)    # 树类型

# 用于管理测试任务的开发迭代树
class Sprint_tree(models.Model):
    id  = models.AutoField(primary_key=True)
    text = models.CharField(max_length=50)        # 存放节点名称
    state = models.CharField(max_length=10)       # 存放节点状态（是否展开）
    parent_id = models.IntegerField()             # 存放父节点id
    iconCls = models.CharField(max_length=20)      # 存放节点图标名称
    attributes = models.CharField(max_length=100)  # 存放节点属性
    project = models.ForeignKey(Test_project_setting, to_field='id', on_delete=models.CASCADE) # 关联项目ID
    order = models.IntegerField()                       # 顺序

# UI自动化项目配置
class UI_project_setting(models.Model):
    id = models.AutoField(primary_key=True)            # ID, 主键
    project_name = models.CharField(max_length=50)      # 项目名称
    home_page = models.CharField(max_length=500)        # 项目主页
    environment = models.CharField(max_length=20)       # 所属环境
    environment_id = models.IntegerField()              # 所属环境ID
    valid_flag = models.CharField(max_length=5)         # 是否启用标识（启用|禁用）
    order = models.IntegerField()                       # 顺序

# API自动化项目配置
class API_project_setting(models.Model):
    id = models.AutoField(primary_key=True)            # ID, 主键
    project_name = models.CharField(max_length=50)      # 项目名称
    protocol = models.CharField(max_length=10)          # 协议 http、http
    host = models.CharField(max_length=200)             # 主机地址
    port = models.IntegerField()                        # 端口
    environment = models.CharField(max_length=20)       # 所属环境
    environment_id = models.IntegerField()              # 所属环境ID
    valid_flag = models.CharField(max_length=5)         # 是否启用标识（启用|禁用）
    order = models.IntegerField()                       # 顺序

# 用于管理页面元素的页面树
class Page_tree(models.Model):
    id  = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=50)                # 存放节点名称
    state = models.CharField(max_length=10)               # 存放节点状态（是否展开）
    parent_id = models.IntegerField()                     # 存放父节点id
    iconCls = models.CharField(max_length=20)             # 存放节点图标名称
    attributes = models.CharField(max_length=100)         # 存放节点属性
    project = models.ForeignKey(UI_project_setting, to_field='id', on_delete=models.CASCADE) # 关联项目ID
    order = models.IntegerField()    # 存放节点顺序

# 用于管理UI测试用例的用例树
class UI_case_tree(models.Model):
    id  = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=50) # 存放节点名称
    state = models.CharField(max_length=10) # 存放节点状态（是否展开）
    parent_id = models.IntegerField() # 存放父节点id
    iconCls = models.CharField(max_length=20) # 存放节点图标名称
    attributes = models.CharField(max_length=100)  # 存放节点属性
    project = models.ForeignKey(UI_project_setting, to_field='id', on_delete=models.CASCADE) # 关联项目ID
    order = models.IntegerField()    # 存放节点顺序

# 用于管理接口测试用例的用例树
class API_case_tree(models.Model):
    id  = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=50) # 存放节点名称
    state = models.CharField(max_length=10) # 存放节点状态（是否展开）
    parent_id = models.IntegerField() # 存放父节点id
    iconCls = models.CharField(max_length=20) # 存放节点图标名称
    attributes = models.CharField(max_length=100)  # 存放节点属性
    project = models.ForeignKey(API_project_setting, to_field='id', on_delete=models.CASCADE) # 关联项目ID
    order = models.IntegerField()    # 存放节点顺序


# 敏捷开发测试任务概要
class Test_task_overview(models.Model):
    id = models.BigAutoField(primary_key=True) # 任务ID
    module = models.CharField(max_length=100) # 任务所属功能模块
    progress = models.CharField(max_length=10) # 整体进度
    requirement = models.CharField(max_length=100) #需求任务
    sub_task = models.CharField(max_length=100) # 子任务
    time_for_test = models.CharField(max_length=20) # 预估转测时间
    real_time_for_test = models.CharField(max_length=20) # 实际转测时间
    if_delay = models.CharField(max_length=2) # 是否延迟转测
    developer_in_charge = models.CharField(max_length=50) # 开发负责人
    tester_in_charge = models.CharField(max_length=20) # 测试负责人
    pm_in_charge = models.CharField(max_length=10)  # 产品负责人
    mark = models.CharField(max_length=100)  # 备注
    order = models.IntegerField()
    page = models.ForeignKey(Sprint_tree, to_field='id', on_delete=models.PROTECT)


# 敏捷开发测试任务明细
class Test_task_detail(models.Model):
    id = models.BigAutoField(primary_key=True) # 任务ID
    module = models.CharField(max_length=100) # 任务所属功能模块
    requirement = models.CharField(max_length=100) #需求任务
    person_in_charge = models.CharField(max_length=20) # 测试负责人
    sub_task = models.CharField(max_length=100) # 子任务
    progress = models.CharField(max_length=10) # 任务进度
    time_took = models.CharField(max_length=10) # 预估耗时
    deadline = models.CharField(max_length=20) # 预计截止时间
    finish_time = models.CharField(max_length=20) # 实际完成时间
    if_delay = models.CharField(max_length=4)    # 是否超时
    history_progress = models.CharField(max_length=400) # 进度更新历史记录
    remark = models.CharField(max_length=200)    # 备注
    order = models.IntegerField()
    page = models.ForeignKey(Sprint_tree, to_field='id', on_delete=models.PROTECT)


# 反馈问题管理
class Promble_feedback(models.Model):
    id = models.BigAutoField(primary_key=True)              # 问题ID
    desc = models.CharField(max_length=300)               # 问题描述
    status = models.CharField(max_length=10)              # 问题状态
    issuer = models.CharField(max_length=10)              # 问题发起人
    tracer = models.CharField(max_length=10)              # 问题跟进人
    handler = models.CharField(max_length=10)             # 问题处理人
    record_time = models.CharField(max_length=20)         # 问题录入时间
    start_trace_time = models.CharField(max_length= 20)   # 开始处理时间
    solved_time = models.CharField(max_length= 20)        # 处理完成时间
    mark = models.CharField(max_length=100)               # 备注
    order = models.IntegerField()                         # 顺序

# 浏览器配置
class Env_setting(models.Model):
    id = models.AutoField(primary_key=True)          # ID, 主键
    env = models.CharField(max_length=50)             # 环境
    order = models.IntegerField()                     # 顺序

# 浏览器配置
class Browser_setting(models.Model):
    id = models.AutoField(primary_key=True)          # ID, 主键
    browser = models.CharField(max_length=20)         # 浏览器
    order = models.IntegerField()                     # 顺序


# 数据库配置
class Database_setting(models.Model):
    id = models.AutoField(primary_key=True)        # ID, 主键
    db_type = models.CharField(max_length=10)       # 数据库类型
    db_alias = models.CharField(max_length=20)      # 数据库别名，唯一
    db_name = models.CharField(max_length=20)       # 数据库名称
    db_host = models.CharField(max_length=200)       # ip,host
    db_port = models.IntegerField()                 # 端口
    db_user = models.CharField(max_length=20)       # 数据库用户名
    db_passwd = models.CharField(max_length=20)     # 数据库用户密码
    environment = models.CharField(max_length=20)   # 所属环境
    environment_id = models.IntegerField()          # 所属环境ID
    project_type = models.CharField(max_length=10)  # 项目类型 API项目，UI项目
    project_name = models.CharField(max_length=50)  # 项目名称
    project_id =  models.CharField(max_length=300)  # 关联项目ID
    order = models.IntegerField()                   # 顺序


# 不同类型对象可执行的操作
class Operation_for_object(models.Model):
    id = models.AutoField(primary_key=True)          # ID, 主键
    object_type = models.CharField(max_length=10)     # 对象类型
    operation = models.CharField(max_length=50)       # 对象具备的操作
    order = models.IntegerField()                     # 顺序

# 函数配置
class Function_setting(models.Model):
    id = models.AutoField(primary_key=True)           # ID, 主键
    function_name = models.CharField(max_length=20)    # 函数名称
    param_style = models.CharField(max_length=100)     # 参数样例
    order = models.IntegerField()                      # 顺序
    project_type = models.CharField(max_length=10)     # 项目类型

# 断言类型配置
class Assertion_type_setting(models.Model):
    id = models.AutoField(primary_key=True)                 # ID, 主键
    op_type = models.CharField(max_length=10)                # 页面操作|接口请求操作|数据库操作|系统函数调用
    assertion_type = models.CharField(max_length=50)         # 断言类型
    assertion_pattern = models.CharField(max_length=2000)    # 断言模式
    order = models.IntegerField()                            # 顺序


# 全局变量配置(供接口自动化使用)
class Global_variable_setting(models.Model):
    id = models.AutoField(primary_key=True)                # ID，主键
    name = models.CharField(max_length=50)                  # 变量名称
    value = models.CharField(max_length=3000)               # 变量值
    remark = models.CharField(max_length=3000)              # 备注
    environment = models.CharField(max_length=20)           # 所属环境
    env_id = models.CharField(max_length=500)               #关联环境ID
    project_type = models.CharField(max_length=10)          # 项目类型 API项目，UI项目, 所有项目
    project_name = models.CharField(max_length=50)          # 项目名称
    project_id = models.CharField(max_length=500)           # 关联项目ID
    order = models.IntegerField()                           # 顺序


# UI自动化页面元素
class Page_element(models.Model):
    id  = models.BigAutoField(primary_key=True)      # ID, 主键
    element_name = models.CharField(max_length=100)   # 元素名称
    selector1 = models.CharField(max_length=150)      # 元素选择器
    selector2 = models.CharField(max_length=150)
    order = models.IntegerField()                     # 顺序
    page = models.ForeignKey(Page_tree, to_field='id', on_delete=models.PROTECT)


# UI自动化测试用例步骤
class UI_test_case_step(models.Model):
    id = models.BigAutoField(primary_key=True)           # 步骤ID
    order = models.IntegerField()                        # 步序
    object_type = models.CharField(max_length=10)        # 操作对象类型
    page_name = models.CharField(max_length=1000)        # 归属页面
    object = models.CharField(max_length=50)             # 要操作的对象
    exec_operation = models.CharField(max_length=50)     # 要执行的操作
    input_params = models.CharField(max_length=500)      # 输入参数
    output_params = models.CharField(max_length=100)     # 输出参数
    assert_type  = models.CharField(max_length=20)       # 预期结果-断言类型
    assert_pattern = models.CharField(max_length=1000)   # 预期结果-断言模式
    run_times = models.IntegerField()                    # 运行次数
    try_for_failure = models.IntegerField()              # 失败重试次数
    status = models.CharField(max_length=5)              # 步骤状态 启用|禁用
    object_id = models.IntegerField()                    # 对象ID(页面元素ID, 数据库ID，函数ID)
    case = models.ForeignKey(UI_case_tree, to_field='id', on_delete=models.PROTECT) #节点ID，即用例ID


# API自动化测试用例步骤
class API_test_case_step(models.Model):
    id = models.BigAutoField(primary_key=True)          # 步骤ID
    order = models.IntegerField()                        # 步序
    step_type = models.CharField(max_length=10)          # 步骤类型
    op_object = models.CharField(max_length=5000)          # 操作对象
    object_id = models.BigIntegerField()                 # 对象ID(数据库ID,用例ID)
    exec_operation = models.CharField(max_length=50)     # 要执行的操作
    request_header = models.CharField(max_length=2000)   # 请求头
    request_method = models.CharField(max_length=10)     # 请求方法
    url_or_sql = models.CharField(max_length=2000)       # URL/SQL
    input_params = models.CharField(max_length=3000)     # 输入参数
    response_to_check = models.CharField(max_length=10)  # 检查响应
    check_rule = models.CharField(max_length=20)         # 校验规则
    check_pattern = models.CharField(max_length=3000)    # 校验模式
    output_params = models.TextField(max_length=6000)    # 输出
    protocol = models.CharField(max_length=10)           # 协议 http、https
    host = models.CharField(max_length=200)              # 主机地址
    port = models.CharField(max_length=6)                # 端口
    run_times = models.IntegerField()                    # 运行次数
    try_for_failure = models.IntegerField()              # 失败重试次数
    retry_frequency = models.IntegerField()              # 失败重试频率
    status = models.CharField(max_length=5)              # 步骤状态 启用|禁用
    case = models.ForeignKey(API_case_tree, to_field='id', on_delete=models.PROTECT) #节点ID，即用例ID

# UI自动化测试计划
class UI_test_plan(models.Model):
    id = models.AutoField(primary_key=True)           # 计划ID
    project_name = models.CharField(max_length=100)    # 关联项目的名称
    plan_name = models.CharField(max_length=50)        # 计划名称
    plan_desc = models.CharField(max_length=200)       # 计划描述
    browsers = models.CharField(max_length=20)         # 运行浏览器
    browser_id = models.CharField(max_length=100)      # 浏览器id
    valid_flag = models.CharField(max_length=5)        # 是否启用(启用|禁用)
    order = models.IntegerField()                      # 顺序
    project = models.ForeignKey(UI_project_setting,to_field='id', on_delete=models.PROTECT)      # 所属项目ID


# API自动化测试计划
class API_test_plan(models.Model):
    id = models.AutoField(primary_key=True)           # 计划ID
    project_name = models.CharField(max_length=100)    # 关联项目的名称
    plan_name = models.CharField(max_length=50)        # 计划名称
    plan_desc = models.CharField(max_length=200)       # 计划描述
    valid_flag = models.CharField(max_length=5)        # 是否启用(启用|禁用)
    order = models.IntegerField()                      # 顺序
    project = models.ForeignKey(API_project_setting, to_field='id', on_delete=models.PROTECT)      # 所属项目ID

# UI测试用例树和测试计划关联表
class UI_case_tree_test_plan(models.Model):
    id  = models.BigAutoField(primary_key=True)       # 主键ID
    plan_id = models.IntegerField()                    # 计划ID
    node_name = models.CharField(max_length=50)        # 存放节点名称
    node_path = models.CharField(max_length=1000)      # 存放节点“父级路径”
    sub_node_num = models.IntegerField()               # 存子节点数量，用于区分是否是用例
    order = models.IntegerField(default=0)             # 顺序
    node = models.ForeignKey(UI_case_tree, to_field='id', on_delete=models.PROTECT) #节点ID

# 接口测试用例树和测试计划关联表
class API_case_tree_test_plan(models.Model):
    id  = models.BigAutoField(primary_key=True)       # 主键ID
    plan_id = models.IntegerField()                    # 计划ID
    node_name = models.CharField(max_length=50)        # 存放节点名称
    node_path = models.CharField(max_length=5000)      # 存放节点“父级路径”
    sub_node_num = models.IntegerField()               # 存子节点数量，用于区分是否是用例
    order = models.IntegerField(default=0)             # 顺序
    node = models.ForeignKey(API_case_tree, to_field='id', on_delete=models.PROTECT) #节点ID

# 运行计划管理-运行计划
class Running_plan(models.Model):
    id  = models.BigAutoField(primary_key=True)        # 主键ID
    running_plan_num = models.BigIntegerField()         # 运行计划编号
    running_plan_name = models.CharField(max_length=50) # 运行计划名称
    project_type = models.CharField(max_length=10)      # 项目类型 API项目，UI项目
    project_id = models.IntegerField()                  # 项目ID(前端隐藏)
    project_name = models.CharField(max_length=50)      # 项目名称
    plan_name = models.CharField(max_length=50)         # 计划名称，如果有多个，都号分隔
    plan_id = models.CharField(max_length=500)          # 计划ID，如果有多个,逗号分隔 (前端隐藏)
    script_dirpath = models.CharField(max_length=200)   # 脚本父级目录绝对路径
    python_path = models.CharField(max_length=200)      # python路径
    valid_flag = models.CharField(max_length=5)         # 是否启用(启用|禁用)
    running_status = models.CharField(max_length=10)    # 运行状态：未执行|执行中|
    remark = models.CharField(max_length=1000)          # 备注
    order = models.IntegerField()                       # 顺序


# UI自动化测试报告-测试概况
class UI_test_report_for_summary(models.Model):
    id = models.AutoField(primary_key=True)
    execution_num = models.CharField(max_length=30)      # 执行编号
    project_id = models.IntegerField()                   # 项目ID（前端隐藏）
    plan_id = models.IntegerField()                      # 计划ID
    project_name = models.CharField(max_length=100)      # 项目名称
    plan_name = models.CharField(max_length=50)          # 计划名称
    browser = models.CharField(max_length=20)            # 浏览器
    start_time = models.CharField(max_length=30)         # 开始运行时间
    end_time = models.CharField(max_length=30)           # 结束运行时间
    time_took = models.CharField(max_length=20)          # 运行耗时
    case_total_num = models.IntegerField()               # 用例总数
    case_pass_num = models.IntegerField()                # 用例执行成功数
    case_fail_num = models.IntegerField()                # 用例执行失败数
    case_block_num = models.IntegerField()               # 用例执行阻塞数
    remark = models.CharField(max_length=3000)           # 备注，说明计划运行失败的原因

# API自动化测试报告-测试概况
class API_test_report_for_summary(models.Model):
    id = models.AutoField(primary_key=True)
    execution_num = models.CharField(max_length=30)      # 执行编号
    project_id = models.IntegerField()                   # 项目ID（前端隐藏）
    plan_id = models.IntegerField()                      # 计划ID
    project_name = models.CharField(max_length=100)      # 项目名称
    plan_name = models.CharField(max_length=50)          # 计划名称
    start_time = models.CharField(max_length=30)         # 开始运行时间
    end_time = models.CharField(max_length=30)           # 结束运行时间
    time_took = models.CharField(max_length=20)          # 运行耗时
    case_total_num = models.IntegerField()               # 用例总数
    case_pass_num = models.IntegerField()                # 用例执行成功数
    case_fail_num = models.IntegerField()                # 用例执行失败数
    case_block_num = models.IntegerField()               # 用例执行阻塞数
    remark = models.CharField(max_length=3000)           # 备注，说明计划运行失败的原因

# UI自动化测试报告-用例执行明细
class UI_test_report_for_case(models.Model):
    id = models.BigAutoField(primary_key=True)
    execution_num = models.CharField(max_length=30)      # 执行编号（和ui_test_report_for_summary.execution_num保持一致
    plan_id = models.IntegerField()                      # 计划ID（前端隐藏）
    case_id = models.IntegerField()                      # 用例ID
    case_path = models.CharField(max_length=1000)        # 计划名称
    case_name = models.CharField(max_length=100)         # 用例名称
    run_result = models.CharField(max_length=10)         # 运行结果
    run_time = models.CharField(max_length=30)           # 运行时间
    remark = models.CharField(max_length=3000)           # 失败原因、补充说明，备注
    time_took = models.CharField(max_length=20)          # 运行耗时

# API自动化测试报告-用例执行明细
class API_test_report_for_case(models.Model):
    id = models.BigAutoField(primary_key=True)
    execution_num = models.CharField(max_length=30)      # 执行编号（和api_test_report_for_summary.execution_num保持一致
    plan_id = models.IntegerField()                      # 计划ID（前端隐藏）
    case_id = models.IntegerField()                      # 用例ID
    case_path = models.CharField(max_length=1000)        # 计划名称
    case_name = models.CharField(max_length=100)         # 用例名称
    run_result = models.CharField(max_length=10)         # 运行结果
    run_time = models.CharField(max_length=30)           # 运行时间
    remark = models.CharField(max_length=3000)           # 失败原因、补充说明，备注
    time_took = models.CharField(max_length=20)          # 运行耗时

# UI自动化测试报告-用例步骤执行明细
class UI_test_report_for_case_step(models.Model):
    id = models.BigAutoField(primary_key=True)
    execution_num = models.CharField(max_length=30)      # 执行编号（ui_test_report_for_case.execution_num保持一致
    plan_id = models.IntegerField()                      # 计划ID（前端隐藏）
    case_id = models.IntegerField()                      # 用例ID（前端隐藏）
    step_id = models.IntegerField()                      # 用例步骤ID
    order = models.IntegerField()                        # 步序
    page = models.CharField(max_length=1000)             # 所属页面
    object = models.CharField(max_length=200)            # 操作对象
    exec_operation = models.CharField(max_length=10)     # 执行操作
    input_params = models.CharField(max_length=500)       # 输入参数
    output_params = models.CharField(max_length=500)      # 输出参数
    assert_type  = models.CharField(max_length=100)      # 预期结果-断言类型
    check_pattern = models.CharField(max_length=500)    # 预期结果-断言模式
    run_times = models.IntegerField()                    # 运行次数
    try_for_failure = models.IntegerField()              # 失败重试次数
    run_result = models.CharField(max_length=10)         # 运行结果
    remark = models.CharField(max_length=500)            # 原因备注
    run_time = models.CharField(max_length=30)           # 运行时间
    run_id = models.BigIntegerField()                    # 运行id，用于关联用例和用例步骤，值:UI_test_report_for_case.id

# UI自动化测试报告-用例步骤执行明细
class API_test_report_for_case_step(models.Model):
    id = models.BigAutoField(primary_key=True)          # 步骤ID
    execution_num = models.CharField(max_length=30)      # 执行编号（api_test_report_for_case.execution_num保持一致
    plan_id = models.IntegerField()                      # 计划ID（前端隐藏）
    case_id = models.IntegerField()                      # 用例ID（前端隐藏）
    step_id = models.IntegerField()                      # 用例步骤ID
    order = models.IntegerField()                        # 步序
    step_type = models.CharField(max_length=10)          # 步骤类型
    op_object = models.CharField(max_length=5000)          # 操作对象
    object_id = models.BigIntegerField()                 # 对象ID(数据库ID,用例ID)
    exec_operation = models.CharField(max_length=50)     # 要执行的操作
    protocol = models.CharField(max_length=10)           # 协议 http、https
    host = models.CharField(max_length=200)               # 主机地址
    port = models.CharField(max_length=6)                # 端口
    request_header = models.CharField(max_length=2000)   # 请求头
    request_method = models.CharField(max_length=10)     # 请求方法
    url_or_sql = models.CharField(max_length=2000)       # URL/SQL
    input_params = models.CharField(max_length=3000)     # 输入参数
    response_to_check = models.CharField(max_length=10)  # 检查响应
    check_rule = models.CharField(max_length=20)         # 校验规则
    check_pattern = models.CharField(max_length=3000)    # 校验模式
    output_params = models.TextField(max_length=7000)    # 输出
    run_result = models.CharField(max_length=10)         # 运行结果
    remark = models.CharField(max_length=3000)           # 原因备注
    run_time = models.CharField(max_length=30)           # 运行时间
    run_id = models.BigIntegerField()                    # 运行id，用于关联用例和用例步骤，值:API_test_report_for_case.id
