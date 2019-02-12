# #!/usr/bin/env python
# #-*-encoding:utf-8-*-
#
__author__ = 'shouke'

from common.globalvar import  test_platform_db
from common.log import logger

# 同步测试步骤表中的页面元素所在页面路径
def sync_page_name_of_element_for_case_steps():
    temp_var = ''
    def find_node_fullpath(node_id):
        nonlocal  temp_var
        query = "SELECT parent_id, text FROM `website_page_tree` WHERE id = %s"
        data = (node_id, )
        result = test_platform_db.select_one_record(query, data)

        if result[0] and result[1]:
            parent_id, text = result[1]
            temp_var = find_node_fullpath(parent_id) + '->' + text
            return temp_var
        elif result[0] and not result[1]:
            return temp_var
        else:
            logger.error('查询出错，退出程序')
            exit()

    try:
        logger.info('正在查询与测试步骤关联的页面元素ID')
        query = "SELECT object_id FROM `website_ui_test_case_step` WHERE object_type = '页面元素' GROUP BY object_id"
        data = ''
        result = test_platform_db.select_many_record(query, data)
        if result[0] and result[1]:
            records = result[1]
            for record in records:
                element_id = int(record[0])

                logger.info('正在查找页面元素所在页面ID')
                query = "SELECT page_id  FROM `website_page_element` WHERE id = %s"
                data = (element_id,)
                result = test_platform_db.select_one_record(query, data)

                if result[0] and result[1]:
                    page_id = int(result[1][0])

                    logger.info('正在查找页面(id：%s)的父页面信息' % page_id)
                    query = "SELECT text, parent_id FROM `website_page_tree` WHERE id = %s"
                    data = (page_id,)
                    result = test_platform_db.select_one_record(query, data)

                    if result and result[1]:
                        text, parent_id = result[1]
                        page_node_path = (find_node_fullpath(parent_id) + text).lstrip('->')

                        logger.info('同步测试步骤表中的页面元素所在页面路径')
                        query = "UPDATE website_ui_test_case_step SET page_name='%s' WHERE object_id = %s AND object_type = '页面元素'"
                        data = (page_node_path, element_id)
                        result = test_platform_db.execute_update(query, data)
                        if not result[0]:
                            logger.error('同步测试步骤表中的页面元素(id:%s)所在页面路径失败：%s' % (element_id, result[1]))
                        else:
                            logger.info('同步测试步骤表中的页面元素(id:%s)所在页面路径成功：%s' % (element_id, result[1]))
                    elif result[0] and not result[1]:
                        logger.warn('未找到页面(id：%s)的父页面信息' % page_id)
                        continue
                    else:
                        logger.error('正在查找页面(id：%s)的父页面信息失败：%s，退出程序' % (page_id, result[1]))
                        exit()
                    temp_var = ''
                elif result[0] and not result[1]:
                    logger.warn('没有找到查找页面元素（ID:%s）所在的页面id' % element_id)
                    continue
                else:
                    logger.error('找到查找页面元素（ID:%s）所在的页面id失败：%s，退出程序' % result[1])
                    exit()
        elif result[0] and not result[1]:
            logger.warn('没找到与测试步骤关联的页面元素ID')
            exit()
        else:
            logger.error('查询与测试步骤关联的页面元素ID失败：%s，退出程序' % result[1])
            exit()
    except Exception as e:
        logger.error( '同步测试步骤表中的页面元素所在页面路径失败：%s' % e)


## 同步测试步骤表中的用例所在页面及用例名称
def sync_page_name_of_case_for_case_steps():
    temp_var = ''
    def find_case_fullpath(node_id):
        nonlocal  temp_var
        query = "SELECT parent_id, text FROM `website_ui_case_tree` WHERE id = %s"
        data = (node_id, )
        result = test_platform_db.select_one_record(query, data)

        if result[0] and result[1]:
            parent_id, text = result[1]
            temp_var = find_case_fullpath(parent_id) + '->' + text
            return temp_var
        elif result[0] and not result[1]:
            return temp_var
        else:
            logger.error('查询用例路径出错，退出程序')
            exit()

    try:
        logger.info('正在查询测试步骤操作的用例对象id')
        query = "SELECT object_id FROM `website_ui_test_case_step` WHERE object_type = '用例' GROUP BY object_id"
        data = ''
        result = test_platform_db.select_many_record(query, data)
        if result[0] and result[1]:
            records = result[1]
            for record in records:
                object_id = int(record[0])
                logger.info('正在查找用例(ID：%s)所在父级页面信息' % object_id)
                query = "SELECT text, parent_id FROM `website_ui_case_tree` WHERE id = %s"
                data = (object_id,)
                result = test_platform_db.select_one_record(query, data)

                if result and result[1]:
                    text, parent_id = result[1]
                    page_node_path = (find_case_fullpath(parent_id) + '').lstrip('->')

                    logger.info('正在同步测试步骤表中用例(ID：%s)所在页面信息,用例名称' % object_id)
                    query = "UPDATE website_ui_test_case_step SET page_name='%s', object='%s' WHERE object_id = %s AND object_type = '用例'"
                    data = (page_node_path, text, object_id)
                    result = test_platform_db.execute_update(query, data)
                    if not result[0]:
                        logger.error('正在同步测试步骤表中用例(ID：%s)所在页面信息及用例名称失败：%s' % (object_id, result[1]))
                    else:
                        logger.info('正在同步测试步骤表中用例(ID：%s)所在页面信息及用例名称成功' % object_id)
                elif result[0] and not result[1]:
                    logger.warn('未找到用例(ID：%s)所在父级路径信息' % object_id)
                    continue
                else:
                    logger.error('查找用例(ID：%s)所在父级路径信息出错：%s,退出程序' % (object_id, result[1]))
                    exit()
                temp_var = ''
        elif result[0] and not result[1]:
            logger.warn('没找到测试步骤操作的用例对象id')
            exit()
        else:
            logger.error('正在查询测试步骤操作的用例对象id失败：%s，退出程序' % result[1])
            exit()
    except Exception as e:
        logger.error( '同步测试步骤表中的用例所在页面及用例名称失败：%s' % e)

if __name__ == '__main__':
    logger.warn('---------------------------start----------------------------------')
    sync_page_name_of_element_for_case_steps()
    sync_page_name_of_case_for_case_steps()
    logger.warn('---------------------------end----------------------------------\n\n\n')