$.noConflict();

var daphneListenPort = 8001;

// 获取上次选择的项目(ID),用于展示树形结构，测试计划等
function getProjectChosen(treeType){
	var defer = $.Deferred();
    $.get('/action/getProjectChosen?treeType=' + treeType,
        function(data, status) {
        	var jsonData = JSON.parse(data);
            defer.resolve(jsonData);
    });
    return defer;
}


// 存储上次选择的项目(ID),用于展示树形结构，测试计划等
function storeProjectChosen(treeType, projectID, projectName){
	var defer = $.Deferred();
    $.post('/action/storeProjectChosen?treeType=' + treeType,
        {
        	treeType: treeType,
            projectID: projectID,
        	projectName: projectName
        },
        function(data, status) {
        	if (data != 'success') {
        		$.messager.alert('提示信息', '存储所选项目失败：' + data, 'error');
        		defer.resolve('error');
            } else {
            	defer.resolve('success');
            }
        }
    );
    return defer;
}

// 根据项目类型(测试项目|UI自动化项目|接口自动化项目|所有项目)，获取对应的项目
function getProjects(projectType) {
	var defer = $.Deferred();
    // 请求已有已启用项目
    $.get('/action/getProjects?projectType=' + projectType, function(data,status) {
        var jsonData = JSON.parse(data);
        defer.resolve(jsonData);
    });
    return defer;
}




// 根据项目类型(测试项目|UI自动化项目|接口自动化项目)，项目ID，获取获取对应的测试计划
function getPlans(projectType, projectID) {
    var defer = $.Deferred();
    // 请求已有已启用项目
    $.get('/action/getPlans?projectType=' + projectType + '&projectID=' + projectID, function(data,status) {
        var jsonData = JSON.parse(data);
        defer.resolve(jsonData);
    });
    return defer;
}



// 为表格新增工具栏 
function addToolbar(datagridID, datagridType) {
    if (datagridType == 'test_plan_case_view') {
        var toolbar = [{
                        text:'用例互换',
                        iconCls:'icon-add',
                        handler:exchangeTestplanCases
                    },{
                        text:'删除',
                        iconCls:'icon-remove',
                        handler:function(){
                            removeRow(datagridID);
                        }                 
                    },{
                        text:'重新排序',
                        iconCls:'icon-edit',
                        handler:function(){ 
                            reOrderRows(datagridID)
                        }
                    }];
    } else if (datagridType == 'test_report_view'){
        var toolbar = [{
                        text:'删除',
                        iconCls:'icon-remove',
                        handler:function(){
                            removeRow(datagridID);
                        }                  
                    }];        
    } else if (datagridType == 'API_test_case_step' || datagridType == 'UI_test_case_step'){
        var toolbar = [{
                        text:'新增',
                        iconCls: 'icon-add',
                        handler: insertRow
                    },{
                        text:'修改',
                        iconCls:'icon-edit',
                        handler:editRow
                    }, {
                        text:'删除',
                        iconCls:'icon-remove',
                        handler:function(){
                            removeRow(datagridID);
                        }            
                    }, {
                        text:'保存',
                        iconCls:'icon-save',
                        // disabled:true,
                        handler:saveRow            
                    }, {
                        text:'取消',
                        iconCls:'icon-cancel',
                        handler:cancelEditRow            
                    }, {
                        text:'禁用',
                        iconCls:'icon-disable',
                        handler:function(){
                            enableOrDisableCaseStep(datagridID, '禁用');
                        }                             
                    }, {
                        text:'启用',
                        iconCls:'icon-enable',
                        handler:function(){
                            enableOrDisableCaseStep(datagridID, '启用');
                        }
                    }];
    } else {
        var toolbar = [{
                        text:'新增',
                        iconCls: 'icon-add',
                        handler: insertRow
                    },{
                        text:'修改',
                        iconCls:'icon-edit',
                        handler:editRow
                    }, {
                        text:'删除',
                        iconCls:'icon-remove',
                        handler:function(){
                            removeRow(datagridID);
                        }            
                    }, {
                        text:'保存',
                        iconCls:'icon-save',
                        // disabled:true,
                        handler:saveRow            
                    }, {
                        text:'取消',
                        iconCls:'icon-cancel',
                        handler:cancelEditRow            
                    }];        
    }
    return toolbar;
}


// 针对不需要进行新增|修改记录的页面
function endEditing() {
    return true; //默认返回true
}

// 删除表格中的记录
function removeRow(datagridID, rowID, index){ 
    if (endEditing()){
        var idSelector = '#' + datagridID;
        if (index == undefined) { // 点击表格上方的删除按钮
            //获取选中行的数据  
            var rowsSelected = $(idSelector).datagrid('getSelections');
            if (rowsSelected.length < 1) {  //如果没有选中行，提示信息  
                $.messager.alert("提示信息", "请选择要删除的记录！", 'info');  
                return;  
            }

            $.messager.confirm("确认消息", "确定要删除所选记录吗？", function (isDelete) {  
                if (isDelete) { //确定删除
                    var url = '/action/removeRow';
                    var rowIDs = '';  // 存放所选记录的ID
                    for (var i = 0; i < rowsSelected.length; i++) {  
                        rowIDs += rowsSelected[i].id + ",";  
                    }

                    data = 'rowIDs=' + rowIDs + '&datagridID=' + datagridID;              
                    $.post(url, data, function(data,status) {
                        if (data == 'success') {
                            $.each(rowsSelected, function(i, row){
                                var rowIndex = $(idSelector).datagrid('getRowIndex', row);
                                $(idSelector).datagrid('deleteRow', rowIndex); 
                            });           
                            $.messager.alert('提示信息', '删除成功', 'info');
                            $(idSelector).datagrid('reload');  // 重新加载数据，防止执行其它操作时获取索引错误
                        } else {
                            $.messager.alert('错误信息', '删除失败:' + data, 'error');
                        } 
                    });                  
                }  
            });  
        } else { // 点击记录行所在的 删除 按钮
            $.messager.confirm("确认消息", "确定要删除所选记录吗？", function (isDelete) {  
                if (isDelete) { //确定删除
                    var url = '/action/removeRow'; 
                    var data = 'rowIDs=' + rowID + ',&datagridID=' + datagridID;  

                    $.post(url, data, function(data,status) {
                        if (data == 'success') {
                            $(idSelector).datagrid('deleteRow', index);
                            $(idSelector).datagrid('reload');
                            $.messager.alert('提示信息', '删除成功', 'info');
                        } else {
                          	$.messager.alert('错误信息', '删除失败:' + data, 'warnging');
                        } 
                    });                  
                }  
            });  
        }
    } 
}

// 上移|下移datagrid记录（通用操作）
function moveRow(datagridID, index, button) {
    var idSelector = '#' + datagridID;
    var data = $(idSelector).datagrid('getData');
    if ($.trim($(button).text()) == '上移') { // 需要使用trim，否则不会成功，估计前后有空格
        if (index == 0) {
            $.messager.alert('提示', '已经是第一行了', 'info');
            $(idSelector).datagrid('reload');  
            return;
        }
        
        var rowToUp = data.rows[index]; //待上移的行(当前行)
        var rowToDown = data.rows[index - 1]; // 待下移的行

        var temp_order = rowToUp.order;
        rowToUp.order = rowToDown.order;
        rowToDown.order = temp_order;
        data.rows[index] = rowToDown;
        data.rows[index - 1] = rowToUp;
        
        // 更新数据库
        updateRowOrder('{"'+rowToDown.id+'":'+rowToDown.order +',"'+rowToUp.id+'":'+rowToUp.order + '}', 
                       datagridID).then(function(result) {
            if(result == 'success') {
                if (datagridID == 'Test_task_detail'||datagridID == 'Test_task_overview'){
                    refreshRow(); //解决错位问题
                    $(idSelector).datagrid('reload');
                } else {
	                $(idSelector).datagrid('refreshRow', index);
	                $(idSelector).datagrid('refreshRow', index - 1);                 
		            if (idSelector == '#Promble_feedback') {
					    onLoadSuccess(data); // 加载按钮样式   
					} else {
					    onLoadSuccess(); // 加载按钮样式     	
				    } 
                }  
            } else {
            	$.messager.alert('提示信息', '上移失败:' + result, 'warnging');
            }
            $(idSelector).datagrid('unselectAll');
        });                       
    } else if ($.trim($(button).text()) == '下移') {
        if (data.rows.length == index +1) { // rows的长度为当前页面记录数
            $.messager.alert('提示', '已经是最后一行了', 'info');
            $(idSelector).datagrid('reload');  
            return;
        }
        var rowToDown = $(idSelector).datagrid('getData').rows[index]; // 待下移的行(当前行)  
        var rowToUp = $(idSelector).datagrid('getData').rows[index+1]; //待上移的行             

        var temp_order = rowToUp.order;
        rowToUp.order = rowToDown.order;
        rowToDown.order = temp_order;
        data.rows[index + 1] = rowToDown;
        data.rows[index] = rowToUp; 
                

        // 更新数据库
        updateRowOrder('{"'+rowToDown.id+'":'+rowToDown.order +',"'+rowToUp.id+'":'+rowToUp.order + '}', 
                       datagridID).then(function(result) {
            if(result == 'success') {
                if (datagridID == 'Test_task_detail'||datagridID == 'Test_task_overview'){
                    refreshRow(); //解决错位问题
                    $(idSelector).datagrid('reload');
                } else {
		            $(idSelector).datagrid('refreshRow', index);
		            $(idSelector).datagrid('refreshRow', index + 1);               
		            if (datagridID == 'Promble_feedback') {
					    onLoadSuccess(data); // 加载按钮样式   
					} else {
					    onLoadSuccess(); // 加载按钮样式     	
				    } 
                } 
            } else {
            	$.messager.alert('提示信息', '下移失败:' + result, 'warnging');
            }
            $(idSelector).datagrid('unselectAll');
        });
    }
}

// 上|下移操作，更新记录顺序
function updateRowOrder(orderDic, datagridID) {
	var defer = $.Deferred();
    $.post('/action/moveRow', {
                orderDic:orderDic,
                datagridID:datagridID
            },function(data, status){
                if (data == 'success') {
                    $.messager.alert('提示', '保存成功', 'info');
                    defer.resolve('success');
                } else {
                	defer.resolve('error');
                    $.messager.alert('提示', '保存失败: ' + data, 'error');
                }

            });
    return defer;
}

// 置顶、置底操作
function putRowTopOrBottom(datagridID, index, button) {
    var idSelector = '#' + datagridID;
    var data = $(idSelector).datagrid('getData');
    // 获取当前页面所在父页面(tab页)的ID
    var currentTab = window.parent.$('#tabs').tabs('getSelected');
    var planID = currentTab.panel('options').id;
    var direction = 'top'; 
    if ($.trim($(button).text()) == '置底') {
        direction = 'bottom';
    }
    rowID = data.rows[index].id;
    rowOrder = data.rows[index].order;

    $.post('/action/putRowTopOrBottom', {rowID:rowID, rowOrder:rowOrder, direction:direction, datagridID:datagridID, planID:planID}, 
        function(data, status){
            if (data == 'success') {
                $.messager.alert('提示', '保存成功', 'info');
                $(idSelector).datagrid('reload');
            } else if (data == 'AlreadyTop') {
                $.messager.alert('提示', '已经是最顶端了', 'info');
            } else if (data == 'AlreadyBottom'){
                $.messager.alert('提示', '已经是最底端了', 'info');
            } else {
                $.messager.alert('错误', '保存失败: ' + data, 'error');
            }
        }
    );
}

// 重新排序表格中的记录
function reOrderRows(datagridID) {
    var idSelector = '#' + datagridID;
    // 获取当前页面所在父页面(tab页)的ID
    var currentTab = window.parent.$('#tabs').tabs('getSelected');
    var planID = currentTab.panel('options').id;
   
    $.post('/action/reOrderRows', {datagridID:datagridID, planID:planID}, 
        function(data, status){
            if (data == 'success') {
                $.messager.alert('提示', '重新排序成功', 'info');
                $(idSelector).datagrid('reload');
            } else {
                $.messager.alert('错误', '重新排序失败: ' + data, 'error');
            }
        }
    );
}

function onDropForTestPlanCaseView(targetRow, sourceRow, point, datagridID) {
    var targetRowID = targetRow.id;
    var targetRowOrder = targetRow.order;

    var sourceRowID = sourceRow.id;
    var sourceRowOrder = sourceRow.order;

    var planID = sourceRow.plan_id;
    var idSelector = '#' + datagridID;

    $.post('/action/dragRowOfTestPlanCaseView ', {targetRowID:targetRowID, targetRowOrder:targetRowOrder, sourceRowID:sourceRowID, sourceRowOrder:sourceRowOrder, direction:point, datagridID:datagridID, planID:planID}, 
        function(data, status){
            if (data == 'success') {
                $.messager.alert('提示', '保存成功', 'info');
            } else {
                $.messager.alert('错误', '保存失败: ' + data, 'error');
            }
        }
    );
    onLoadSuccess();

    $(idSelector).datagrid('reload');

}


function onDropForTestCaseStep(targetRow, sourceRow, point, datagridID) {
    var targetRowID = targetRow.id;
    var targetRowOrder = targetRow.order;

    var sourceRowID = sourceRow.id;
    var sourceRowOrder = sourceRow.order;
    console.log(sourceRow);

    var caseID = sourceRow.case_id;
    var idSelector = '#' + datagridID;

    $.post('/action/dragRowOfTestCaseStep ', {targetRowID:targetRowID, targetRowOrder:targetRowOrder, sourceRowID:sourceRowID, sourceRowOrder:sourceRowOrder, direction:point, datagridID:datagridID, caseID:caseID}, 
        function(data, status){
            if (data == 'success') {
                $.messager.alert('提示', '保存成功', 'info');
            } else {
                $.messager.alert('错误', '保存失败: ' + data, 'error');
            }
        }
    );
    onLoadSuccess();

    $(idSelector).datagrid('reload');

}

// 启用、禁用测试用例步骤表中的记录
function enableOrDisableCaseStep(datagridID, opType){ 
    if (endEditing()){
        var idSelector = '#' + datagridID;   
        //获取选中行的数据  
        var rowsSelected = $(idSelector).datagrid('getSelections');
        if (rowsSelected.length < 1) {  //如果没有选中行，提示信息  
            $.messager.alert("告警", "请选择要" + opType +"的记录！", 'warn');  
            return;  
        }

        $.messager.confirm("确认消息", "确定要" + opType +"所选记录吗？", function (isConfirm) {  
            if (isConfirm) { //确定删除
                var url = '/action/enableOrDisableCaseStep';
                var rowIDs = '';  // 存放所选记录的ID
                for (var i = 0; i < rowsSelected.length; i++) {  
                    rowIDs += rowsSelected[i].id + ",";  
                }

                data = 'rowIDs=' + rowIDs + '&datagridID=' + datagridID + '&opType=' + opType;              
                $.post(url, data, function(data,status) {
                    if (data == 'success') {        
                        $.messager.alert('提示信息', '操作成功', 'info');
                        $(idSelector).datagrid('reload');  // 重新加载数据，防止执行其它操作时获取索引错误
                    } else {
                        $.messager.alert('错误信息', '操作失败:' + data, 'error');
                    } 
                });                  
            }  
        });
    }
}

// 扩展时间控件
Date.prototype.format = function (format) {  
    var o = {  
        "M+": this.getMonth() + 1, // month  
        "d+": this.getDate(), // day  
        "h+": this.getHours(), // hour  
        "m+": this.getMinutes(), // minute  
        "s+": this.getSeconds(), // second  
        "q+": Math.floor((this.getMonth() + 3) / 3), // quarter  
        "S": this.getMilliseconds()  
        // millisecond  
    }  
    if (/(y+)/.test(format))  
        format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));  
        for (var k in o)  
            if (new RegExp("(" + k + ")").test(format))  
                format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));  
        return format;  
    }  


// 时间格式化函数
function formatDatebox(value) {  
    if (value == null || value == '') {  
        return '';  
    }  
    var dt;  
    if (value instanceof Date) {  
        dt = value;  
    } else {  
            dt = new Date(value);  
    }  
      
    return dt.format("yyyy-MM-dd"); //扩展的Date的format方法(上述插件实现)  
}   

var textChanged = false;    // 用于判断是否combobox选取、输入的内容是否改变

// 收起多选combobox下拉列表时触发事件
function onHidePanelForCombobox(){
    var text = $(this).combobox('getText');
    text = text.split(',');

    var list = [];
    var json = {};
    var res = '';

    // 去除重复数据
	for(var i = 0; i < text.length; i++){
	    if(!json[text[i]]) {
	        list.push(text[i]);
	        res = res + text[i] + ','
	        json[text[i]] = true;
	    }
	}
	res = res.substring(0,res.length-1); // 删除最右侧逗号

    if(textChanged) {
        var mark = false;
        var comboboxData = $(this).combobox('getData');
        outerBlock:{
            for (var i=0; i<list.length; i++) {
                var item = list[i];
                innerBlock:{
                    for (var j=0; j<comboboxData.length; j++) {
                        var dataObj = comboboxData[j];
                        if(dataObj.choice == item) {
                            mark = true; //用户输入项，存在下拉列表选项中,停止查找
                            break innerBlock;
                        }else{ //遍历完内存循环还没找到，标记false
                            mark = false;
                        }    
                    }
                    if(!mark) { 
                        break outerBlock;
                    }
                }
            }
        }         
        if(!mark) {
            $(this).combobox('clear');
            $.messager.alert('告警', '请通过下拉列表择现有项', 'warning');                 
        } else {
            $(this).combobox('clear');
            $(this).combobox('setText', res);
        }             
    } 
    textChanged = false;     
}

// commbox输入框的值改变时触发事件
function onChangeForCombobox(newValue, oldValue) {
    textChanged = true;
} 



// 设置单元格样式，控制英文换行
function setCellStyle(){
    return "white-space:pre-wrap;word-break:break-all;word-wrap:break-word";
}
