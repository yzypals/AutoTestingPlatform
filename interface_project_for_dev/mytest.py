#-*- encoding:utf-8 -*-

__author__ = 'laifuyu'
# import xml.etree.ElementTree as ET
# import re

# /node
# 查找结果：报错，不能使用绝对路径
# ./node2
# 查找结果：找不到元素
# ./Body
# 查找结果：找不到元素
# ./ns1:Body/selectByPrimaryKeyResponse
# 查找结果：找不到元素
# ./ns1:Body/ns2:selectByPrimaryKeyResponse/return
# 查找结果：找不到元素
# ./ns1:Body/ns2:selectByPrimaryKeyResponse/xmlns:return[1]/copeWith
# 查找结果：找不到元素

# 查找结果：根元素，即Envelope元素
# ns1:Body
# 查找结果：所有名称空间为ns1的Body元素
# ./ns1:Body
# 查找结果：等同ns1:Body
# ./ns1:Body/ns2:selectByPrimaryKeyResponse
# 查找结果：所有名称空间为ns1的Body元素下的所有名为selectByPrimaryKeyResponse的子元素
# ./ns1:Body/ns2:selectByPrimaryKeyResponse[2]
# 查找结果：所有名称空间为ns1的Body元素下，名称空间为ns2的第2个名为selectByPrimaryKeyResponse的子元素
# ./ns1:Body/ns2:selectByPrimaryKeyResponse/xmlns:return
# 查找结果：所有名称空间为ns1的Body元素下，所有名称空间为ns2,名称为selectByPrimaryKeyResponse的子元素下，所有名称空间定义为 http://www.overide_first_defaul_xmlns.com的return元素
# ./ns1:Body/ns2:selectByPrimaryKeyResponse/xmlns:return[1]/xmlns:copeWith
# 查找结果：所有名称空间为ns1的Body元素下，所有名称空间为ns2,名称为selectByPrimaryKeyResponse的子元素下，第一个名称空间定义为http://www.overide_first_defaul_xmlns.com的return元素下，
# 名称空间定义为http://www.overide_first_defaul_xmlns.com的copyWith元素
# .//xmlns:copeWith
# 查找结果：所有名称空间定义为http://www.overide_first_defaul_xmlns.com的copeWith元素
# .//xmlns:copeWith[2]
# 查找结果：同一个元素节点下，名称空间定义为http://www.overide_first_defaul_xmlns.com的第二个copeWith元素(例中为 <copeWith>5.00</copeWith>' ，注意：这里的数字是针对兄弟节点的，不再赘述)
# 注意：[]里面不支持last()这种谓词，数字可以
# .//xmlns:return//xmlns:copeWith"
# 查找结果：所有名称空间定义为http://www.overide_first_defaul_xmlns.com的return元素下，所有名称空间定义为http://www.overide_first_defaul_xmlns.com的copeWith元素
# xpath = ".//xmlns:return//xmlns:copeWith"
#
#
# response_to_check = '<soap:Envelope xmlns="http://www.examp.com"  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" >' \
#                     '    <node2>' \
#                     '        <id>goods1</id>' \
#                     '    </node2>    ' \
#                     '    <ns1:Body xmlns:ns1="http://service.rpt.data.platform.ddt.sf.com/">' \
#                         '    <ns2:selectByPrimaryKeyResponse  xmlns:ns2="http://service.rpt.data.platform.ddt.sf2.com/"  xmlns="http://www.overide_first_defaul_xmlns.com">  '\
#                         '        <return>' \
#                         '                <copeWith>1.00</copeWith>' \
#                         '                <discount>0.99</discount>' \
#                         '                <id>144</id>' \
#                         '                <invoice>2</invoice>' \
#                         '                <invoiceType></invoiceType>' \
#                         '                <orderCode>DDT201704071952057186</orderCode>' \
#                         '                <orderDate>2017-04-07 19:52:06.0</orderDate>' \
#                         '                <paid>0.01</paid>' \
#                         '                <payType>pc</payType>' \
#                         '                <productName>快递包</productName>' \
#                         '                <state>0</state>' \
#                         '                <userId>2</userId>' \
#                         '        </return>' \
#                         '        <return>' \
#                         '             <copeWith>2.00</copeWith>' \
#                         '             <discount>0.99</discount>' \
#                         '             <id>143</id>' \
#                         '             <invoice>2</invoice>' \
#                         '             <invoiceType></invoiceType>' \
#                         '             <orderCode>DDT201704071951065731</orderCode>' \
#                         '             <orderDate>2017-04-07 19:51:07.0</orderDate> ' \
#                         '             <paid>0.01</paid>' \
#                         '             <payType>pc</payType>' \
#                         '             <productName>快递包</productName>' \
#                         '             <state>0</state>' \
#                         '             <userId>2</userId>' \
#                         '        </return>' \
#                         '        <return>                ' \
#                         '            <copeWith>3.00</copeWith>' \
#                         '            <discount>0.99</discount>' \
#                         '            <id>142</id>' \
#                         '            <invoice>2</invoice>' \
#                         '            <invoiceType></invoiceType>' \
#                         '            <orderCode>DDT201704071945408575</orderCode>' \
#                         '            <orderDate>2017-04-07 19:45:40.0</orderDate>' \
#                         '            <paid>0.01</paid>' \
#                         '            <payType>pc</payType>' \
#                         '            <productName>快递包</productName>' \
#                         '            <state>0</state>' \
#                         '            <userId>2</userId>' \
#                         '       </return>            ' \
#                         '       <return attr="re">' \
#                         '            <copeWith>4.00</copeWith>' \
#                         '            <copeWith>5.00</copeWith>' \
#                         '            <discount>0.99</discount>' \
#                         '            <id>141</id>' \
#                         '            <invoice>1</invoice>' \
#                         '            <invoiceType>增值税普通发票</invoiceType>' \
#                         '            <orderCode>DDT201704071845403738</orderCode>' \
#                         '            <orderDate>2017-04-07 18:45:41.0</orderDate>' \
#                         '            <paid>0.01</paid>' \
#                         '            <productName>快递包</productName>' \
#                         '            <state>0</state>' \
#                         '            <userId attr="testattr">2</userId>' \
#                         '      </return>' \
#                         '    </ns2:selectByPrimaryKeyResponse>' \
#                         '</ns1:Body>' \
#                         '<ns1:Body xmlns:ns1="http://service.rpt.data.platform.ddt.sf.com/">' \
#                         '    <ns2:selectByPrimaryKeyResponse  xmlns:ns2="http://service.rpt.data.platform.ddt.sf2.com/"> '\
#                         '    </ns2:selectByPrimaryKeyResponse>' \
#                         '    <ns2:selectByPrimaryKeyResponse  xmlns:ns2="http://service.rpt.data.platform.ddt.sf2.com/"> '\
#                         '    </ns2:selectByPrimaryKeyResponse>' \
#                         '</ns1:Body>' \
#                     '</soap:Envelope>'
#
# # 对比试验
# # .//xmlns:return//xmlns:copeWith
# # 查找结果：所有名称空间定义为http://www.examp.com的return元素下，所有名称空间定义为http://www.examp.com的copeWith元素
#
# xpath = ".//xmlns:return//xmlns:copeWith"
#
#
# response_to_check = '<soap:Envelope xmlns="http://www.examp.com"  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" >' \
#                     '    <node2>' \
#                     '        <id>goods1</id>' \
#                     '    </node2>    ' \
#                     '    <ns1:Body xmlns:ns1="http://service.rpt.data.platform.ddt.sf.com/">' \
#                         '    <ns2:selectByPrimaryKeyResponse  xmlns:ns2="http://service.rpt.data.platform.ddt.sf2.com/">  '\
#                         '        <return>' \
#                         '                <copeWith>1.00</copeWith>' \
#                         '                <discount>0.99</discount>' \
#                         '                <id>144</id>' \
#                         '                <invoice>2</invoice>' \
#                         '                <invoiceType></invoiceType>' \
#                         '                <orderCode>DDT201704071952057186</orderCode>' \
#                         '                <orderDate>2017-04-07 19:52:06.0</orderDate>' \
#                         '                <paid>0.01</paid>' \
#                         '                <payType>pc</payType>' \
#                         '                <productName>快递包</productName>' \
#                         '                <state>0</state>' \
#                         '                <userId>2</userId>' \
#                         '        </return>' \
#                         '        <return>' \
#                         '             <copeWith>2.00</copeWith>' \
#                         '             <discount>0.99</discount>' \
#                         '             <id>143</id>' \
#                         '             <invoice>2</invoice>' \
#                         '             <invoiceType></invoiceType>' \
#                         '             <orderCode>DDT201704071951065731</orderCode>' \
#                         '             <orderDate>2017-04-07 19:51:07.0</orderDate> ' \
#                         '             <paid>0.01</paid>' \
#                         '             <payType>pc</payType>' \
#                         '             <productName>快递包</productName>' \
#                         '             <state>0</state>' \
#                         '             <userId>2</userId>' \
#                         '        </return>' \
#                         '        <return>                ' \
#                         '            <copeWith>3.00</copeWith>' \
#                         '            <discount>0.99</discount>' \
#                         '            <id>142</id>' \
#                         '            <invoice>2</invoice>' \
#                         '            <invoiceType></invoiceType>' \
#                         '            <orderCode>DDT201704071945408575</orderCode>' \
#                         '            <orderDate>2017-04-07 19:45:40.0</orderDate>' \
#                         '            <paid>0.01</paid>' \
#                         '            <payType>pc</payType>' \
#                         '            <productName>快递包</productName>' \
#                         '            <state>0</state>' \
#                         '            <userId>2</userId>' \
#                         '       </return>            ' \
#                         '       <return attr="re">' \
#                         '            <copeWith>4.00</copeWith>' \
#                         '            <copeWith>5.00</copeWith>' \
#                         '            <discount>0.99</discount>' \
#                         '            <id>141</id>' \
#                         '            <invoice>1</invoice>' \
#                         '            <invoiceType>增值税普通发票</invoiceType>' \
#                         '            <orderCode>DDT201704071845403738</orderCode>' \
#                         '            <orderDate>2017-04-07 18:45:41.0</orderDate>' \
#                         '            <paid>0.01</paid>' \
#                         '            <productName>快递包</productName>' \
#                         '            <state>0</state>' \
#                         '            <userId attr="testattr">2</userId>' \
#                         '      </return>' \
#                         '    </ns2:selectByPrimaryKeyResponse>' \
#                         '</ns1:Body>' \
#                         '<ns1:Body xmlns:ns1="http://service.rpt.data.platform.ddt.sf.com/">' \
#                         '    <ns2:selectByPrimaryKeyResponse  xmlns:ns2="http://service.rpt.data.platform.ddt.sf2.com/"> '\
#                         '    </ns2:selectByPrimaryKeyResponse>' \
#                         '    <ns2:selectByPrimaryKeyResponse  xmlns:ns2="http://service.rpt.data.platform.ddt.sf2.com/"> '\
#                         '    </ns2:selectByPrimaryKeyResponse>' \
#                         '</ns1:Body>' \
#                     '</soap:Envelope>'
# # ./string
# # 查找结果：找不到元素
# # ./xmlns:string
#
# # 查找结果，根元素下，所有名称空间定义为 xmlns的string元素
# xpath = "./xmlns:string"
#
# response_to_check =''\
#     '<ArrayOfString xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
#     '   xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://WebXml.com.cn/">' \
#     '   <string>阿尔及利亚,3320</string>' \
#     '   <string>阿根廷,3522</string>' \
#     '   <string>阿曼,3170</string>' \
#     '   <string>阿塞拜疆,3176</string>' \
#     '   <string>埃及,3317</string>' \
#     '   <string>埃塞俄比亚,3314</string>' \
#     '   <string>爱尔兰,3246</string>' \
#     '   <string>奥地利,3237</string>' \
#     '   <string>澳大利亚,368</string>' \
#     '   <string>巴基斯坦,3169</string>' \
#     '   <string>巴西,3580</string>' \
#     '   <string>保加利亚,3232</string>' \
#     '   <string>比利时,3243</string>' \
#     '</ArrayOfString>'
#
# # 对比试验
# # ./string
# # 查找结果，根元素下，所有名称空间定义为 http://WebXml.com.cn/的string元素
# xpath = "./string"
#
# response_to_check =''\
#     '<ArrayOfString xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
#     '   xmlns:xsd="http://www.w3.org/2001/XMLSchema">' \
#     '   <string>阿尔及利亚,3320</string>' \
#     '   <string>阿根廷,3522</string>' \
#     '   <string>阿曼,3170</string>' \
#     '   <string>阿塞拜疆,3176</string>' \
#     '   <string>埃及,3317</string>' \
#     '   <string>埃塞俄比亚,3314</string>' \
#     '   <string>爱尔兰,3246</string>' \
#     '   <string>奥地利,3237</string>' \
#     '   <string>澳大利亚,368</string>' \
#     '   <string>巴基斯坦,3169</string>' \
#     '   <string>巴西,3580</string>' \
#     '   <string>保加利亚,3232</string>' \
#     '   <string>比利时,3243</string>' \
#     '</ArrayOfString>'
#
# xpath = ".//return"
#
# response_to_check ='<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:findByAccountCompanyResponse xmlns:ns2="http://service.rpt.ddtm.platform.ddt.sf.com/"><return>dataviewer</return></ns2:findByAccountCompanyResponse></soap:Body></soap:Envelope>'
#
# root = ET.fromstring(response_to_check)
# print(root)
#
# if xpath == '.':
#     text_of_element = root.text
# else:
#     xmlnsnamespace_dic = {}  # 存放名称空间定义
#     print('正在获取xmlns定义')
#     match_result_list =re.findall('xmlns[^:]?=(.+?)[ |\>|\\\>]', response_to_check, re.MULTILINE)
#     if match_result_list:
#         xmlns = match_result_list[len(match_result_list) - 1]
#         xmlns = xmlns.strip(' ')
#         xmlns = '{' + xmlns + '}'
#         print('xmlns定义为：%s' % xmlns)
#         xmlnsnamespace_dic['xmlns'] = xmlns
#
#     print('正在获取"xmlns:xxx名称空间定义')
#     match_result_list = re.findall('xmlns:(.+?)=(.+?)[ |>]', response_to_check)
#     for ns in match_result_list:
#         xmlnsnamespace_dic[ns[0]] = '{' + ns[1] + '}'
#
#     print("最后获取的prefix:uri为：%s" % xmlnsnamespace_dic)
#
#     print('正在转换元素结点前缀')
#
#     for dic_key in xmlnsnamespace_dic.keys():
#         namespace = dic_key + ':'
#         if namespace in xpath:
#             uri = xmlnsnamespace_dic[dic_key]
#             xpath = xpath.replace(namespace, uri)
#             xpath = xpath.replace('"','')
#
#     print('转换后用于查找元素的xpath：%s' % xpath)
#     try:
#         elements_list = root.findall(xpath)
#     except Exception as e:
#         print('查找元素出错：%s' % e)
#
#     print('查找到的元素为：%s' % elements_list)
#
#     for element in elements_list:
#         text_of_element = element.text
#         print(text_of_element)


import redis

if __name__ == '__main__':
    pass
    r = redis.StrictRedis(host='10.202.40.105', port=8080, db='0', password='admin.123')

     # host='localhost', port=6379,
     #             db=0, password=None, socket_timeout=None,
     #             socket_connect_timeout=None,
     #             socket_keepalive=None, socket_keepalive_options=None,
     #             connection_pool=None, unix_socket_path=None,
     #             encoding='utf-8', encoding_errors='strict',
     #             charset=None, errors=None,
     #             decode_responses=False, retry_on_timeout=False,
     #             ssl=False, ssl_keyfile=None, ssl_certfile=None,
     #             ssl_cert_reqs=None, ssl_ca_certs=None,
     #             max_connections=None):

    # result = r.set('name', 'shouke')  # 存储键-值
    # print('result of set: %s' % result)
    #
    # r.set('hobby', 'music')
    #
    name = r.get('req:cache:code:reset:pwd:18110000014:1061493')  # 获取键“name”对应的值
    print('name: %s' % name)
    #
    keys = r.keys(pattern="req:cache:code:reset:pwd:18110000014*")  # 获取所有键
    print('keys: %s' % keys)
    name = r.get(keys[0])
    print(name)

    #
    # dbsize = r.dbsize() # redis数据库包的记录数(key的数量)
    # print('dbsize: %s' % dbsize)
    #
    # result = r.delete('hobby')  # 根据指定的键，删除指定键-值
    # print('result of delete: %s' % result)
    #
    # result = r.save()  # 执行“检查点”操作，将数据写回磁盘。保存时阻塞
    # print('result of save: %s' % result)
    #
    # hobby = r.get('hobby')
    # print('hobby: %s' % hobby)
    #
    # name = r['name']   # 获取键“name”对应的值
    # print('name: %s' % name)
    #
    # result = r.flushdb()   # 清空数据当前库中的所有数据
    # print('result of flushdb: %s' % result)
    #
    # print('dbsize: %s' % r.dbsize())
