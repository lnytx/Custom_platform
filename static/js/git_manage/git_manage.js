$(function(){
		active_tab=''//定义全局变量，查看当前是哪个tab,执行对应tab的内容
		$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
		      // 获取已激活选项卡的名称
		      var activeTab = $(e.target).text(); 
		      active_tab=activeTab
		      console.log("当前选择的tab页面是:",active_tab)
		      if (active_tab=='查看项目')
		      {
		$("#show_project_num").show();
		      	//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		 //需要动态生成boostrap表格，未完成
		 //var $table=$('<table class="table table-striped table-bordered table-hover" id="myDataTable"></table>')
		 //$("#view_project").append($table);
		$.get('/git_manage/git_project_group_view/',{'add_str':'12'}, function(ret){
							//赋值给条数,页面显示有多少条
							project_num = []
							new_arr = []
							var res = [];   
							var num=1;  
                             //动态生成表头
                             res.push("<tr>")
                             res.push("<th>ID</th>")
                             res.push("<th>IP</th>")
                             res.push("<th>project_name</th>")
                             res.push("<th>center_path</th>")
                             res.push("<th>dest_path</th>")
                             res.push("</tr>")
                             $.each(ret, function(i,item){  
                             var row_num=0
                             console.log("item_project_name",item.project_name)
                             $.each(ret,function(j,t){
                             	if (item.project_name==t.project_name)
                             	{
                             		row_num++;
                             		console.log("row_num",row_num);
                             	}
                             	
                             })
                             var p_name=item.project_name
                         //    res.push(it.ip);  
//                                 res.push( it.id);  
//                                 res.push( it.project_name);  
//                                 res.push( it.dest);
//                                 res.push("\n")
//                                 num++;
                             
								//将所有的project_name添加到project_num中去重计算数量
								project_num.push(item.project_name)
								//动态生成表格写入tdata中
								 res.push('<tr>');  
                                 res.push('<td align="center" class="hidden-480" >' + num + '</td>');  
                                 res.push('<td align="center" >' + item.ip + '</td>');  
                                 res.push('<td align="center" >' + item.project_name + '</td>');  
                                 res.push('<td align="center" >' + item.center_path + '</td>');
                                 res.push('<td align="center" >' + item.dest_path + '</td>');
                                 res.push('</tr>');  
                                 num++;  
                              });  
                              //res.push("</table>")
                              //$("#myDataTable").html(res)
                              	//去重
                              	for(var i=0;i<project_num.length;i++) {
								　　var items=project_num[i];
								　　//判断元素是否存在于new_arr中，如果不存在则插入到new_arr的最后
								　　if($.inArray(items,new_arr)==-1) {
								　　　　new_arr.push(items);
								　　}
								}
							
                              $.unique(project_num); 
                              console.log("new_arr",new_arr.length,new_arr);
                              $("#show_project_num").text("一共有"+new_arr.length+"个项目")
                              $("#myDataTable").append(res)
                              //document.getElementById("view_project").appendChild(res);
                              
                              //view_project
                              //$("#largetextarea").empty().val(res.join(""));  
                              //将结果写入隐藏的表格中
                              //$("#tdata").html(res);
                              //$("#exescuess").empty().val(res.join(""));  
                              //页面未执行的textarea是先隐藏的，如果有未执行的结果则，在这里将隐藏改为显示出来
                              //$("#exefaild").empty().val(res.join(""));  
                              //document.getElementById("weizhixing").style.display="block";
//                              $("#exefaild").empty().val(res.join(""));  
			    	 //将表的第一行数据alex修改为ret.result123
			    	 //$("#largetextarea").val("adasfsd")
			})
		      }//if
		      if (active_tab=='项目git初始化')
				{
					//清空第一页动态生成的表身体
					
						$("#myDataTable").empty();
						$("#view_git_project_name").empty();
				}
			if (active_tab=='项目版本')
				{
					//清空第一页动态生成的表身体
					$("#scuess_exec").empty();
					$("#scuess_html").empty();
					$("#scuess_num").empty();
					 $("#failed_exec").empty();
					 $("#failed_html").empty();
					 $("#failed_num").empty();
					
						$("#myDataTable").empty();
						$("#view_git_multiple").empty()
					$("#view_git_project_name").append("<option value='无'>" + '请选择' + "</option>"); 
					$("#view_git_project_name").attr("checked",true)
					//初始化项目版本中的多选表
					$.get("/git_manage/view_project_version",{"view_project":'None'}, function(ret){
					//根据ajax结果获取后台对应的host的IP
					for (var i = 0; i < ret.length; i++){
						console.log("输出",i,ret[i].project_name)
						$("#view_git_project_name").append("<option value='" + i + "'>" + ret[i].project_name + "</option>");  
						//$("#edit_config_multiple").append("<option value="+i+">" + ret[i].ip + "</option>");
					};
					
					});
				}
				if (active_tab=='git命令')
				{
					//清空第一页动态生成的表身体
					$("#scuess_exec").empty();
					$("#scuess_html").empty();
					$("#scuess_num").empty();
					 $("#failed_exec").empty();
					 $("#failed_html").empty();
					 $("#failed_num").empty();
					
						$("#myDataTable").empty();
						$("#view_git_multiple").empty()
						$("#view_git_deploy_name").empty()
					$("#view_git_deploy_name").append("<option value='无'>" + '请选择' + "</option>"); 
					$("#view_git_deploy_name").attr("checked",true)
					//初始化项目版本中的多选表
					$.get("/git_manage/view_project_version",{"view_project":'None'}, function(ret){
					//根据ajax结果获取后台对应的host的IP
					for (var i = 0; i < ret.length; i++){
						console.log("输出",i,ret[i].project_name)
						$("#view_git_deploy_name").append("<option value='" + i + "'>" + ret[i].project_name + "</option>");  
						//$("#edit_config_multiple").append("<option value="+i+">" + ret[i].ip + "</option>");
					};
					
					});
					
				}
		      // 获取先前选项卡的名称
		      var previousTab = $(e.relatedTarget).text(); 
		   });
		   
	var git_manage_group = $("#git_manage_group").find("option:selected").text();
	var ul = $("#ul");
	//ajax获取后台group_list数据
	$.get("/cmdb/group_list/",{"add_str":''}, function(ret){
		//动态添加select选项,从后台数据库获取
		$("#git_manage_group").empty()
		$("#git_manage_group").append("<option>" + '无' + "</option>");
		
		for (var i = 0; i < ret.length; i++) 
			{
	 			$("#git_manage_group").append("<option group_id="+ret[i].group_id+">" + ret[i].group_name + "</option>");
	 		}
		})
	
	

	//多选插件
$('#git_manage_multiple').multiselect({  
                enableClickableOptGroups: true,  
                enableCollapsibleOptGroups: true,  
                includeSelectAllOption: true,  
                buttonWidth: '400px',  
                dropRight: false,  
                maxHeight: 150,  
                onChange: function(option, checked) {  
               	console.log($(option).val());  
                                /*if(条件) { 
                      this.clearSelection();//清除所有选择及显示 
                 }*/  
                },  
                nonSelectedText: '--无--',  
                numberDisplayed: 10,  
                enableFiltering: true,  
                allSelectedText:'全部',  
        });  
	//上面是多选
	
	

$('#view_git_multiple').multiselect({  
                enableClickableOptGroups: true,  
                enableCollapsibleOptGroups: true,  
                includeSelectAllOption: true,  
                buttonWidth: '400px',  
                dropRight: false,  
                maxHeight: 150,  
                onChange: function(option, checked) {  
               	console.log($(option).val());  
                                /*if(条件) { 
                      this.clearSelection();//清除所有选择及显示 
                 }*/  
                },  
                nonSelectedText: '--无--',  
                numberDisplayed: 10,  
                enableFiltering: true,  
                allSelectedText:'全部',  
        });  





	})
	



//view_git_project_name的onchange事件,查看选择项目对应的中心库的版本
function view_center_version(obj)
{
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		 if (active_tab=='项目版本')
		 {
		 	var project_name = $("#view_git_project_name").find("option:selected").text(); 
		 }
		 
		
		if (active_tab=='git命令')
		{
			var project_name = $("#view_git_deploy_name").find("option:selected").text();
		}
		$.get('/git_manage/view_center_version/',{"project_name":project_name}, function(ret){
				$.each(ret,function(i,item){
				                    	if(i!='msg' && i!='code') 
				                    	{
				                    		if(String(item).substring(0,5)=='ERROR')
						                    	{
						                    		$("#failed_exec").css('display','block');
						                    		$("#failed_num").text(project_name+"中心服务器版本查看失败");
						                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>命令为:"+i+"执行失败:</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    		$("#failed_exec").append($html)
						                    	}
						                    	else
						                    	{
						                    		$("#scuess_exec").css('display','block');
						                    		$("#scuess_num").text(project_name+"中心服务器版本取最近5次提交:");
						                    		$("#scuess_exec").append("<div id='scuess_html'><div  class='alert alert-block alert-success fade in'><p><b>命令为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    	}
						                 }
				                    	
				                    	
				                    })
		
		 			});
}



//处理配置文件中的多选
function git_manage_Onchang(obj)
{
	$("#git_manage_multiple").empty()
	var group_name = $("#git_manage_group").find("option:selected").text();
		$.get("/exec_cmd",{"group_name":group_name}, function(ret){
					//根据ajax结果获取后台对应的host的IP
					for (var i = 0; i < ret.length; i++){
						$("#git_manage_multiple").append("<option value='" + i + "'>" + ret[i].ip + "</option>");  
						//$("#edit_config_multiple").append("<option value="+i+">" + ret[i].ip + "</option>");
					};
					
						//处理修改配置时的多选
				if ((group_name!='无') && (ret.length>0))
				{
					$("#git_manage_multiple").multiselect("destroy").multiselect({  
                enableClickableOptGroups: true,  
                enableCollapsibleOptGroups: true,  
                includeSelectAllOption: true,  
                buttonWidth: '400px',  
                dropRight: false,  
                maxHeight: 150,  
                onChange: function(option, checked) {  
                ips = $("#git_manage_multiple").find("option:selected").text()
                },  
                nonSelectedText: '--请选择--',  
                numberDisplayed: 10,  
                enableFiltering: true,  
                allSelectedText:'全部',  
        		}); 
			}
				else
				{
					$("#git_manage_multiple").multiselect("destroy").multiselect({  
	                enableClickableOptGroups: true,  
	                enableCollapsibleOptGroups: true,  
	                includeSelectAllOption: true,  
	                buttonWidth: '400px',  
	                dropRight: false,  
	                maxHeight: 150,  
	                onChange: function(option, checked) {  
	               	console.log($(option).val());  
	                },  
	                nonSelectedText: '--这个组无值--',  
	                numberDisplayed: 10,  
	                enableFiltering: true,  
	                allSelectedText:'全部',  
	       			 }); 
				}
				});
				
				
}

//定义一个方法，获取IP传到后台，后台根据IP找到minion_id并执行命令，并将结果返回
//提交按钮
function saltFunc()
	{
	if (active_tab=='查看项目')//执行命令执行tab的按钮事件
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		 //需要动态生成boostrap表格，未完成
		 //var $table=$('<table class="table table-striped table-bordered table-hover" id="myDataTable"></table>')
		 //$("#view_project").append($table);
		$.get('/git_manage/git_project_group_view/',{'add_str':'12'}, function(ret){
							var res = [];   
                             var num=1;  
                             //动态生成表头
                             res.push("<tr>")
                             res.push("<th>ID</th>")
                             res.push("<th>IP</th>")
                             res.push("<th>project_name</th>")
                             res.push("<th>dest</th>")
                             res.push("</tr>")
                             $.each(ret, function(i,item){  
                         //    res.push(it.ip);  
//                                 res.push( it.id);  
//                                 res.push( it.project_name);  
//                                 res.push( it.dest);
//                                 res.push("\n")
//                                 num++;
                             	 console.log("res1",res)
                             
								
								//动态生成表格写入tdata中
								 res.push('<tr>');  
                                 res.push('<td align="center" class="hidden-480" >' + num + '</td>');  
                                 res.push('<td align="center" >' + item.ip + '</td>');  
                                 res.push('<td align="center" >' + item.project_name + '</td>');  
                                 res.push('<td align="center" >' + item.dest + '</td>');
                                 res.push('</tr>');  
                                 num++;  
                              });  
                              //res.push("</table>")
                              console.log("res2",res)
                              //$("#myDataTable").html(res)
                              $("#myDataTable").append(res)
                              //document.getElementById("view_project").appendChild(res);
                              
                              //view_project
                              //$("#largetextarea").empty().val(res.join(""));  
                              //将结果写入隐藏的表格中
                              //$("#tdata").html(res);
                              //$("#exescuess").empty().val(res.join(""));  
                              //页面未执行的textarea是先隐藏的，如果有未执行的结果则，在这里将隐藏改为显示出来
                              //$("#exefaild").empty().val(res.join(""));  
                              //document.getElementById("weizhixing").style.display="block";
//                              $("#exefaild").empty().val(res.join(""));  
			    	 //将表的第一行数据alex修改为ret.result123
			    	 //$("#largetextarea").val("adasfsd")
		})
			
		}
		
	if (active_tab=='项目git初始化')//执行命令执行tab的按钮事件
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		
		//获取组名
		var group_name = $("#git_manage_group").find("option:selected").text();
		var git_project_dest=$("#git_project_dest").val()
		var git_project_name = $("#git_project_name").val()
		var git_project_center = $("#git_project_center").val()
		
		//ips为表中选择的ip
		item=$("#git_manage_multiple").find("option:selected")
		ips=""
		item.each(function(i,s){
		console.log("item", i,s.text)
		if (i==item.length-1){
    		ips += s.text; 
    		return false;//中断each
    		}
            ips += s.text+","; 
			});
		if (group_name == '无'||ips.length==0)
			{
				swal('执行失败','请选择主机','warning' )
			}
		else if(git_project_dest.length==0)
		{
			swal('执行失败','请输入项目所在路径','warning' )
		}
		else//执行命令
		{
			
			swal({
                title: "执行:",
                text: "执行"+ips,
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "执行",
                closeOnConfirmButtonText:"取消",
                closeOnConfirm: false,
                //allowOutsideClick :false
                
	            }, function () {
	            	$.ajax({ 
				          url:'/git_manage/git_init',
				          type:'get', 
				          data:{'ips':ips,"git_project_name":git_project_name,"group_name":group_name,"git_project_dest":git_project_dest,"git_project_center":git_project_center}, 
				          //timeout:15000, 
				          beforeSend:function(XMLHttpRequest){ 
				              //添加动画，显示正在处理中..
				            	swal({
		        	            title:'loading...',
		        	            text:'正在加载数据',
		        	            imageUrl:'/static/image/ajax-loading.gif',
		        	            showConfirmButton: false//去掉确认的按钮
		        	        });
				         }, 
				         success:function(ret,textStatus){ 
				             //alert('开始回调，状态文本值：'+textStatus+' 返回数据：'+data.msg); 
				             if (ret.code==1) {
				                    swal('成功', ret.msg, ret.status);
				                    count_err=0;
				                    count_scuess=0;
				                    //输出结果到页面中
				                    $.each(ret,function(i,item){
				                    	if(i!='msg' && i!='code') 
				                    	{
				                    		if(String(item).substring(0,5)=='ERROR')
						                    	{
						                    		count_err++;
						                    		$("#failed_exec").css('display','block');
						                    		$("#failed_num").text(count_err+"个服务器执行失败,如下:");
						                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>IP为:"+i+"执行失败:</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    		$("#failed_exec").append($html)
						                    	}
						                    	else
						                    	{
						                    		count_scuess++;
						                    		$("#scuess_exec").css('display','block');
						                    		$("#scuess_num").text(count_scuess+"个服务器执行成功,如下:");
						                    		$("#scuess_exec").append("<div id='scuess_html'><div  class='alert alert-block alert-success fade in'><p><b>minion_id为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    	}
						                 }
				                    	
				                    	
				                    })
//			            			$("#scuess_html").html(msg)
//			            			$("#scuess_exec").css('display','block');
//			            			$("#failed_html").html(msg)
//				                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
//				                        location.reload();
//				                    });
				                } 
				             else if (ret.code == 0) {
				                    swal('有异常',ret.msg, "warning");
				                    $.each(ret,function(i,item){
				                    if(i!='code' && i!='msg')
					                    {
						                    $("#failed_exec").css('display','block');
						                    $("#failed_exec").append("<div id='failed_exec'><div  class='alert alert-block alert-error fade in'><p><b>服务器"+i+"有问题:</b></br>"+JSON.stringify(item, null, '\nt')+ret.msg+"</br>"+"</p></div></div>");
					                    }
				                    })
				                    
				                } 
				        	else if(ret.code == -1){
				                   // swal(ret.msg, "", "error");
				                    swal(
				                    	      '失败',
				                    	     ret.msg,
				                    	      'error'
				                    	 )
				            }
				        	else if(ret.code == -2){
				                   // swal(ret.msg, "", "error");
				                    swal(
				                    	      '失败',
				                    	     ret.msg,
				                    	      'error'
				                    	 )
				            }
				           }, 
				          complete:function(XMLHttpRequest,textStatus){ 
				              // alert('远程调用成功，状态文本值：'+textStatus); 
				             $("#loading").empty(); 
				           }, 
				           error:function(XMLHttpRequest,textStatus,errorThrown){ 
				              swal(
				                    	      textStatus,
				                    	     errorThrown,
				                    	      'error'
				                    )
				          } 
					}); 
	            	
       			 });
			
		}
		
	}
	
	if (active_tab=='项目版本')//执行命令执行tab的按钮事件
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		
		//获取组名
		var project_name =  $("#view_git_project_name").find("option:selected").text();
		var log_num = $("#view_git_project_num").val()
		if (project_name == '无'||project_name.length==0)
			{
				swal('执行失败','请选择项目名称','warning' )
			}
		if(!(/^(\+|-)?\d+$/.test( log_num ))|| log_num<0)
			{
				swal('执行失败','请输入正整数','warning' )
			}
		else//执行命令
		{
			
			swal({
                title: "执行:",
                text: "执行"+project_name,
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "执行",
                closeOnConfirmButtonText:"取消",
                closeOnConfirm: false,
                //allowOutsideClick :false
                
	            }, function () {
	            	$.ajax({ 
				          url:'/git_manage/view_project_version',
				          type:'get', 
				          data:{'project_name':project_name,"log_num":log_num}, 
				          //timeout:15000, 
				          beforeSend:function(XMLHttpRequest){ 
				              //添加动画，显示正在处理中..
				            	swal({
		        	            title:'loading...',
		        	            text:'正在加载数据',
		        	            imageUrl:'/static/image/ajax-loading.gif',
		        	            showConfirmButton: false//去掉确认的按钮
		        	        });
				         }, 
				         success:function(ret,textStatus){ 
				             //alert('开始回调，状态文本值：'+textStatus+' 返回数据：'+data.msg); 
				             if (ret.code==1) {
				                    swal('成功', ret.msg, ret.status);
				                    count_err=0;
				                    count_scuess=0;
				                    //输出结果到页面中
				                    $.each(ret,function(i,item){
				                    	if(i!='msg' && i!='code') 
				                    	{
				                    		if(String(item).substring(0,5)=='ERROR')
						                    	{
						                    		count_err++;
						                    		$("#failed_exec").css('display','block');
						                    		$("#failed_num").text(count_err+"个服务器执行失败,如下:");
						                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>IP为:"+i+"执行失败:</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    		$("#failed_exec").append($html)
						                    	}
						                    	else
						                    	{
						                    		count_scuess++;
						                    		$("#scuess_exec").css('display','block');
						                    		$("#scuess_num").text(count_scuess+"个服务器执行成功,如下:");
						                    		$("#scuess_exec").append("<div id='scuess_html'><div  class='alert alert-block alert-success fade in'><p><b>minion_id为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    	}
						                 }
				                    	
				                    	
				                    })
//			            			$("#scuess_html").html(msg)
//			            			$("#scuess_exec").css('display','block');
//			            			$("#failed_html").html(msg)
//				                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
//				                        location.reload();
//				                    });
				                } 
				             else if (ret.code == 0) {
				                    swal('有异常',ret.msg, "warning");
				                    $.each(ret,function(i,item){
				                    if(i!='code' && i!='msg')
					                    {
						                    $("#failed_exec").css('display','block');
						                    $("#failed_exec").append("<div id='failed_exec'><div  class='alert alert-block alert-error fade in'><p><b>服务器"+i+"有问题:</b></br>"+JSON.stringify(item, null, '\nt')+ret.msg+"</br>"+"</p></div></div>");
					                    }
				                    })
				                    
				                } 
				        	else if(ret.code == -1){
				                   // swal(ret.msg, "", "error");
				                    swal(
				                    	      '失败',
				                    	     ret.msg,
				                    	      'error'
				                    	 )
				            }
				        	else if(ret.code == -2){
				                   // swal(ret.msg, "", "error");
				                    swal(
				                    	      '失败',
				                    	     ret.msg,
				                    	      'error'
				                    	 )
				            }
				           }, 
				          complete:function(XMLHttpRequest,textStatus){ 
				              // alert('远程调用成功，状态文本值：'+textStatus); 
				             $("#loading").empty(); 
				           }, 
				           error:function(XMLHttpRequest,textStatus,errorThrown){ 
				              swal(
				                    	      textStatus,
				                    	     errorThrown,
				                    	      'error'
				                    )
				          } 
					}); 
	            	
       			 });
			
		}
		
	}
	
	
	if (active_tab=='git命令')//执行命令执行tab的按钮事件
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		var project_name = $("#view_git_deploy_name").find("option:selected").text();
		//var version_num = $("#view_deploy_project_num").val()
		var git_pull_project = $("#git_pull_project").val()
		if (project_name == '请选择' )
			{
				swal('命令执行失败','请选择项目名称','warning' )
			}
		//ajax
		else{
			swal({
	                title: "执行:",
	                text: "分发到项目集群:"+project_name,
	                type: "warning",
	                showCancelButton: true,
	                confirmButtonColor: "#DD6B55",
	                confirmButtonText: "执行",
	                closeOnConfirmButtonText:"取消",
	                closeOnConfirm: false,
	                //allowOutsideClick :false
	                
		            }, function () {
						$.ajax({ 
					          url:'/git_manage/git_deploy_version',
					          type:'get', 
					          data:{'project_name':project_name,"git_pull_project":git_pull_project,"pre_view":true}, 
					          //timeout:15000, 
					          beforeSend:function(XMLHttpRequest){ 
					              //添加动画，显示正在处理中..
					            	swal({
			        	            title:'loading...',
			        	            text:'正在加载数据',
			        	            imageUrl:'/static/image/ajax-loading.gif',
			        	            showConfirmButton: false//去掉确认的按钮
			        	        });
					         }, 
					         success:function(ret,textStatus){ 
					             //alert('开始回调，状态文本值：'+textStatus+' 返回数据：'+data.msg); 
					             if (ret.code==1) {
					                    swal('结果', ret.msg, ret.status);
					                    count_err=0;
					                    count_scuess=0;
					                    //输出结果到页面中
					                    $.each(ret,function(i,item){
					                    	if(i!='msg' && i!='code') 
				                    	{
				                    		if(String(item).substring(0,5)=='ERROR')
						                    	{
						                    		count_err++;
						                    		$("#failed_exec").css('display','block');
						                    		$("#failed_num").text(count_err+"个服务器执行失败,如下:");
						                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>IP为:"+i+"执行失败:</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    		$("#failed_exec").append($html)
						                    	}
						                    	else
						                    	{
						                    		count_scuess++;
						                    		$("#scuess_exec").css('display','block');
						                    		$("#scuess_num").text(count_scuess+"个服务器执行成功,如下:");
						                    		$("#scuess_exec").append("<div id='scuess_html'><div  class='alert alert-block alert-success fade in'><p><b>minion_id为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
						                    	}
						                 }
					                    	
					                    	
					                    })
					                } 
					             else if (ret.code == -1) {
					                    swal('有异常',ret.msg, "warning");
					                    $.each(ret,function(i,item){
					                    if(i!='code' && i!='msg')
						                    {
							                    $("#failed_exec").css('display','block');
							                    $("#failed_exec").append("<div id='failed_exec'><div  class='alert alert-block alert-error fade in'><p><b>服务器"+i+"有问题:</b></br>"+JSON.stringify(item, null, '\nt')+ret.msg+"</br>"+"</p></div></div>");
						                    }
					                    })
					                    
					                } 
					        	else if(ret.code == 0){
					                   // swal(ret.msg, "", "error");
					                    swal(
					                    	      '失败',
					                    	     ret.msg,
					                    	      'error'
					                    	 )
					            }
					        	else if(ret.code == -2){
					                   // swal(ret.msg, "", "error");
					                    swal(
					                    	      '失败',
					                    	     ret.msg,
					                    	      'error'
					                    	 )
					            }
					           }, 
					          complete:function(XMLHttpRequest,textStatus){ 
					              // alert('远程调用成功，状态文本值：'+textStatus); 
					             $("#loading").empty(); 
					           }, 
					           error:function(XMLHttpRequest,textStatus,errorThrown){ 
					              swal(
					                    	      textStatus,
					                    	     errorThrown,
					                    	      'error'
					                    )
					          } 
						}); 
			//ajax 完
		});
		}//else
				
	}
	
	}






