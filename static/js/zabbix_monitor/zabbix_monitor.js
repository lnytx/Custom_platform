//根据选中的value也就是itemid值，传到后台，返回结果数据,将选中的itemid定义为全局变量，后面要使用
//var item_id = [];


/**
 * 
 * 获取当前时间
 */
function p(s) {
    return s < 10 ? '0' + s: s;
}
var myDate = new Date();
//获取当前年
var year=myDate.getFullYear();
//获取当前月
var month=myDate.getMonth()+1;
//获取当前日
var date=myDate.getDate(); 
var h=myDate.getHours();       //获取当前小时数(0-23)
var m=myDate.getMinutes();     //获取当前分钟数(0-59)
var s=myDate.getSeconds();  
//默认取前一天
var pre_d=myDate.getDate()-1;

var now=year+'-'+p(month)+"-"+p(date)+" "+p(h)+':'+p(m)+":"+p(s);
var pre_now=year+'-'+p(month)+"-"+p(pre_d)+" "+p(h)+':'+p(m)+":"+p(s);
console.log("当前时间",now)
console.log("当前时间前1小时",pre_now)



$(function(){
var myDate = new Date();
var date=myDate.getDate();
//时间插件初始化
$("#zabbix_minion_starttime").datetimepicker({  
    language : 'zh-CN',  
    weekStart : 1,  
    todayBtn : 1,  
    autoclose : 1,  
    todayHighlight : true,  
    startView : 2,  
    minView: "hour",  
    format: 'yyyy-mm-dd hh:ii:ss',  
    forceParse : true ,//强制解析用户输入内容为正确时间
    minuteStep: 1
}).on('hide', function(event) {  
    event.preventDefault();  
    event.stopPropagation();  
    var startTime = event.date;  
    $("#log_endtime").datetimepicker('setStartDate',startTime);  
    $("#log_endtime").val("");  
}).val(pre_now);  
$("#zabbix_minion_endtime").datetimepicker({  
    language : 'zh-CN',  
    weekStart : 1,  
    todayBtn : 1,  
    autoclose : 1,  
    todayHighlight : true,  
    startView : 2,  
    minView: "hour",  
    format: 'yyyy-mm-dd hh:ii:ss',  
    forceParse : true ,//强制解析用户输入内容为正确时间
    minuteStep: 1
}).on('hide', function(event) {  
    event.preventDefault();  
    event.stopPropagation();  
    var endTime = event.date;  
    $("#log_starttime").datetimepicker('setEndDate',endTime);  
}).val(now);  




 
//多选插件初始化Group       
$('#zabbix_minion_group_multiple').multiselect({  
                buttonWidth: '200px',  
                dropRight: false,  
                maxHeight: 300,  
                maxWidth: '200px',
                onChange: function(option, checked) {  
               	console.log("组",$(option).val());  
                                /*if(条件) { 
                      this.clearSelection();//清除所有选择及显示 
                 }*/  
                 group_name = $(option).val();
                 $.get("zabbix_get_host",{"group_name":group_name}, function(ret){
					//根据ajax结果获取后台对应的host的IP
					for (var i = 0; i < ret.length; i++){
						//$("#zabbix_minion_host_multiple").html(""); 
						//$("#zabbix_minion_host_multiple").empty()
						$("#zabbix_minion_host_multiple").append("<option value=" + i + ">" + ret[i].ip + "</option>");  
						//$("#edit_config_multiple").append("<option value="+i+">" + ret[i].ip + "</option>");
					};
					$('#zabbix_minion_host_multiple').multiselect('rebuild')
                 });
                },  
                nonSelectedText: '选择组',  
                numberDisplayed: 10,  
                single: true,
                enableFiltering: true,  
                //allSelectedText:'全部',  
        });  
        
//多选插件初始化Host
$('#zabbix_minion_host_multiple').multiselect({  
                buttonWidth: '200px',  
                dropRight: false,  
                maxHeight: 300,  
                maxWidth: '200px',
                onChange: function(option, checked) {  
                //联动graph选择器
               	console.log($(option).val());  
                                /*if(条件) { 
                      this.clearSelection();//清除所有选择及显示 
                 }*/  
                 //取IP这种方法不行$(option).val()
                 ip = $("#zabbix_minion_host_multiple").find("option:selected").text()
                 console.log("ip",ip)
                //传入IP，根据IP获取zabbix的监控项
                $.get("zabbix_get_items",{"ip":ip}, function(ret){
                	if (ret.code == -1) 
                	{
				     	swal('警告',ret.msg, ret.status);
				    } 
		        	else
		        	{
		        	//根据ajax结果获取后台对应的host的IP,使用each时更为简洁
		        	// $.each(ret,function(i,item){
//		        	 	console.log("情况提前",i,item)
//		        	 });
						for (var i = 0; i < ret.length; i++)
						{	
							for(var key in ret[i])
							{
								$("#zabbix_minion_graph").append("<option value=" + key + ">" + ret[i][key]+ "</option>");
							}
						};
							$('#zabbix_minion_graph').multiselect('rebuild')
		            }
					});
                },  
                nonSelectedText: '选择host',  
                numberDisplayed: 10,  
                enableFiltering: true,  
                allSelectedText:'全部',  
        });  
//多选插件初始化Graph       
$('#zabbix_minion_graph').multiselect({  
				enableClickableOptGroups: true,  
                enableCollapsibleOptGroups: true,  
                includeSelectAllOption: true,  
                selectAllText: '全选',
                buttonWidth: '200px',  
                dropRight: false,  
                maxHeight: 300,  
                maxWidth: '200px',
                onChange: function(option, checked) {  
               	//var item_id = new Array()
               	//var item_id = [];
//				$("#zabbix_minion_graph").each(function () {
//				console.log("$(option).val()",$(option).text())
//				console.log("$(this).val()",$(this).val())
//				item_id.push($(this).val()) //push([$(this).val()])
				//my_data = JSON.stringify(item_id)
//				});
				//var operatorIDs=JSON.stringify(item_id)//将数组转为JSON字符串
                },  
                nonSelectedText: '选择Graph',  
                numberDisplayed: 10,  
                enableFiltering: true,  
        });    


var selectValueStr = [];  
$("#zabbix_minion_graph option:selected").each(function () {  
    selectValueStr.push($(this).val());  
});  
console.log("选中值",selectValueStr)

//动态添加值
//function deploy_yum_Onchang(obj)
//{
//	$.get("zabbix_minion",{"group_name":group_name}, function(ret){
////					//根据ajax结果获取后台对应的host的IP
//					for (var i = 0; i < ret.length; i++){
//					console.log("情况提前",ret[i].group_name)
//						$("#zabbix_minion_group_multiple").append("<option value='" + i + "'>" + ret[i].group_name + "</option>");  
//						//$("#edit_config_multiple").append("<option value="+i+">" + ret[i].ip + "</option>");
//					};
//}

});


function one_page_num_change(obj)
{
	var check_num = $("#one_page_num").find("option:selected").text();
	if (check_num =='每页数量')
		 {
		 	swal('请选择数量', '您未选择数量', 'warning');
		 	check_num = 5;
		 }
	else
	{
		var form = document.getElementById("myform");
    	form.submit();
		//$.get("/log_view",{"check_num":check_num}, function(ret){
			//动态添加select选项,从后台数据库获取
//			       $("#one_page_num option[value='"+check_num+"']").attr("selected","selected");
//			
//			});
	}
}





