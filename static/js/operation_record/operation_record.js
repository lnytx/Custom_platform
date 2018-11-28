$(function(){

//时间插件初始化
$("#log_starttime").datetimepicker({  
    language : 'zh-CN',  
    weekStart : 1,  
    todayBtn : 1,  
    autoclose : 1,  
    todayHighlight : 1,  
    startView : 2,  
    minView: "month",  
    format: 'yyyy-mm-dd',  
    forceParse : 0  
}).on('hide', function(event) {  
    event.preventDefault();  
    event.stopPropagation();  
    var startTime = event.date;  
    $("#log_endtime").datetimepicker('setStartDate',startTime);  
    $("#log_endtime").val("");  
});  
$("#log_endtime").datetimepicker({  
    language : 'zh-CN',  
    weekStart : 1,  
    todayBtn : 1,  
    autoclose : 1,  
    todayHighlight : 1,  
    startView : 2,  
    minView: "month",  
    format: 'yyyy-mm-dd',  
    forceParse : 0  
}).on('hide', function(event) {  
    event.preventDefault();  
    event.stopPropagation();  
    var endTime = event.date;  
    $("#log_starttime").datetimepicker('setEndDate',endTime);  
});  

	//查看日志详情
	//$('#log_search').click(function () {
//	
//	var log_operation_name = $.trim($("#log_operation_name").val());
//	var log_starttime = $.trim($("#log_starttime").val());
//	var log_endtime = $.trim($("#log_endtime").val());
//	console.log("log_operation_name",log_operation_name,log_starttime,log_endtime)
//	
//	$.get("search_log/",{"log_operation_name":log_operation_name,"log_starttime":log_starttime,"log_endtime":log_endtime}, function(ret){
//			//动态添加html
//			html = ''
//			//动态添加select选项,从后台数据库获取
//			       //$("#one_page_num option[value='"+check_num+"']").attr("selected","selected");
//			       $.each(ret,function(){
//			    //   	html += "<td>"+ret['user_log'].user_name+"</td>"
////					html += "<td><a href='/log_view/details/?target_ids={{row.target_ids}}' class='log_details' id='log_details1'>{{row.action}}</a></td>"
////					html += "<td><span >{{row.result}}</span></td>"
////					html += "<td><span >{{row.exec_time|date:'Y-m-d H:i:s'}}</span></td>"
////					html += "<td><span >{{row.last_login|date:'Y-m-d H:i:s'}}</span></td>"
//					//$("#user_log_row").append(html)
//			       console.log("输出结果1",ret.last_login)
//			       console.log("输出结果2222",ret.result)
//			       })
//			       
//			
//			});
//        
//    });
	
        
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



//查看日志详情
//$('#log_search').click(function () {
//	var log_operation_name = $.trim($("#log_operation_name").val());
//	var log_starttime = $.trim($("#log_starttime").val());
//	var log_endtime = $.trim($("#log_endtime").val());
//	console.log("log_operation_name",log_operation_name,log_starttime,log_endtime)
//	
//						$.ajax({ 
//					          url:'search_log/',
//					          type:'get', 
//					          data:{'log_operation_name':log_operation_name,'log_starttime':log_starttime,'log_endtime':log_endtime}, 
//					          //timeout:15000, 
//					          beforeSend:function(XMLHttpRequest){ 
//					        	  swal({
//				        	            title:'loading...',
//				        	            text:'正在加载数据',
//				        	            imageUrl:'/static/image/ajax-loading.gif',
//				        	            showConfirmButton: false//去掉确认的按钮
//				        	        });
//					         }, 
//					         success:function(ret,textStatus){ 
//					             //alert('开始回调，状态文本值：'+textStatus+' 返回数据：'+data.msg); 
//					             // $("#loading").empty(); 
//					        	   
//					             if (ret.code == 0) {
//					                    swal('更新成功', ret.msg, "success");
//					                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
//					                        location.reload();
//					                    });
//					                } 
//					             else if (ret.code == 1) {
//					                    swal('更新成功', ret.msg, "success");
//					                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
//					                        location.reload();
//					                    });
//					                } 
//					        	else if(ret.code == -1){
//					                   // swal(ret.msg, "", "error");
//					                    swal(
//					                    	      '失败',
//					                    	     ret.msg,
//					                    	      'error'
//					                    	 )
//					            }
//					        	else if(ret.code == -2){
//					                   // swal(ret.msg, "", "error");
//					                    swal(
//					                    	      '失败',
//					                    	     ret.msg,
//					                    	      'error'
//					                    	 )
//					            }
//					            
//					            
//					            
//					           }, 
//					          complete:function(XMLHttpRequest,textStatus){ 
//					              // alert('远程调用成功，状态文本值：'+textStatus); 
////					             $("#loading").empty(); 
//					           }, 
//					           error:function(XMLHttpRequest,textStatus,errorThrown){ 
//					              swal(
//					                    	      textStatus,
//					                    	     errorThrown,
//					                    	      'error'
//					                    )
//				                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
//				                        location.reload();
//				                    });
////					             $("#loading").empty(); 
//					          } 
//						}); 
//					});