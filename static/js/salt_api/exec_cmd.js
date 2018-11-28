$(function(){
		active_tab=''//定义全局变量，查看当前是哪个tab,执行对应tab的内容
		$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
		      // 获取已激活选项卡的名称
		      var activeTab = $(e.target).text(); 
		      active_tab=activeTab
		      console.log("当前选择的tab页面是:",active_tab)
		      // 获取先前选项卡的名称
		      var previousTab = $(e.relatedTarget).text(); 
		      //如果是导航是文件修改则将按钮显示出来，否则隐藏
		      if (active_tab==='文件修改')
				{
				$("#show_view").show();
				show_view_btn='show_view_btn'
				$("#show_view").click(function(){
				//显示要修改的文件的预览版本
					//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		var edit_config_linux = $("#edit_config_linux").val()
		var edit_config_win = $("#edit_config_win").val()
		var edit_config_pre = $("#edit_config_pre").val()
		var edit_config_last = $("#edit_config_last").val()
		//ips为表中选择的ip
		item=$("#edit_config_multiple").find("option:selected")
		ips=""
		item.each(function(i,s){
		if (i==item.length-1){
    		ips += s.text; 
    		return false;//中断each
    		}
             ips += s.text+","; 
			});
		if (ips.length == 0 )
			{
				swal('命令执行失败','请选择主机','warning' )
			}
		else if((edit_config_linux=='' && edit_config_win=='')||edit_config_last=='')
			{
				swal('命令执行失败','请输入配置文件路径或要修改的内容','warning' )
			}
		//ajax
		else{
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
					          url:'/exec_cmd/edit_config',
					          type:'get', 
					          data:{'ips':ips,"edit_config_linux":edit_config_linux,"edit_config_win":edit_config_win,"edit_config_pre":edit_config_pre,"edit_config_last":edit_config_last,"preview":'true'}, 
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
					             if (ret.code==-1) {
					                    swal('结果', ret.msg, ret.status);
					                    count_err=0;
					                    count_scuess=0;
					                    //输出结果到页面中
					                    $.each(ret,function(i,item){
					                    	if(i!='msg' && i!='code'&&i!='status') 
					                    	{
					                    		if(String(item).substring(0,5)=='ERROR')
							                    	{
							                    		count_err++;
							                    		$("#failed_exec").css('display','block');
							                    		$("#failed_num").text(count_err+"个服务器执行失败,如下:");
							                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>minion_id为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
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
					             else if (ret.code == 1) {
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
				})
				}
			 else
			 {
			 	$("#show_view").hide();
			 }
		      
		   });
	
	//这里是命令执行中的组
	var select_group = $("#select_group").find("option:selected").text();
	//下面是修改配置文件里的组
	var edit_config_group = $("#edit_config_group").find("option:selected").text();
	//下面是执行分发yum源中的
	var deploy_yum_minion = $("#deploy_yum_minion").find("option:selected").text();
	var ul = $("#ul");
	//ajax获取后台group_list数据
	$.get("/cmdb/group_list/",{"add_str":''}, function(ret){
		//动态添加select选项,从后台数据库获取
		$("#select_group").empty()
		$("#select_group").append("<option>" + '无' + "</option>");
		
		$("#edit_config_group").empty()
		$("#edit_config_group").append("<option>" + '无' + "</option>");
		
		$("#deploy_yum_group").empty()
		$("#deploy_yum_group").append("<option>" + '无' + "</option>");
		
		for (var i = 0; i < ret.length; i++) 
			{
	 			$("#select_group").append("<option group_id="+ret[i].group_id+">" + ret[i].group_name + "</option>");
	 			//给处理配置文件时的多选同样的添加组名
	 			$("#edit_config_group").append("<option group_id="+ret[i].group_id+">" + ret[i].group_name + "</option>");
	 			//给分发并安装指定salt_minion yum源标签中的salt_minion_id组赋值
	 			$("#deploy_yum_group").append("<option group_id="+ret[i].group_id+">" + ret[i].group_name + "</option>");
	 		}
		})
		//默认是不可选的
		$("#select_host").attr("disabled","disabled");
	
	
	//多选插件
$('#edit_config_multiple').multiselect({  
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

$('#deploy_yum_multiple').multiselect({  
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
        //上面的是分发yum源的多选初始化


	})
	




	var  host_list = "";
//二级联动select,onchang方法
function select_group_Onchang(obj)
		{ 
			var group_name = $("#select_group").find("option:selected").text();
			//处理多选的联动
			var ul = $("#ul");
			if (group_name!='无')//如果不是'无'的话，二级菜单可以选择
			{	
				$(ul).empty("");
				$("#select_host").removeAttr("disabled");
				//处理多级联动
				//默认的选择项总是空或无
				$.get("/exec_cmd",{"group_name":group_name}, function(ret){
					//根据ajax结果获取后台对应的host的IP
					$.each(ret,function(i,item){
						$("#select_host").append("<option value="+i+">" + ret[i].ip + "</option>");
						//处理多选的联动
				        ul.append("<li><div class='checkbox'></div><label><input type='checkbox' value=" + i + " onclick='Choose(this)'/>" + item.ip + "</label></li>");
					});
					$("#select_host").append("<option>" + '无' + "</option>");
					$("#select_host").find("option:contains('无')").attr("selected",true);
					
					//判断返回值为空时
					if(null == ret || "" == ret)
						{
							ul.append("<li><label>该主机组没有对应的主机，请先添加。</label></li>");
						}
				});
				
				$("#select_host").empty()
				//清空一个ul下的所有内容，防止一直追加
				$(ul).empty("");
			}
			else
				{
					$("#select_host").empty()
					$("#select_host").append("<option>" + '无' + "</option>");
					$("#select_host").attr("disabled","disabled");
					$('ul li').remove();
					ul.append("<li><label>无</label></li>");
					//处理多选联动
				}
		}



    function show(t) {
        //设置多选框显示的位置，在选择框的中间
        var left = t.offsetLeft + t.clientWidth / 2 - $("#panel")[0].clientWidth / 2
        var top = t.offsetTop + t.clientHeight + document.body.scrollTop;
        $("#panel").css("opacity", "1");
        $("#panel").css("margin-left", left);
        $("#panel").css("margin-top", top + 5);
    }
    //隐藏多选框
    function hide() {
        $("#panel").css("opacity", "0");
    }
    //全选操作
    // $("#ul").find("input[type=checkbox]").each(function(i,element) {
    
   //console.log(element)
    function CheckAll(t) {
        var name = "";
        var ids = "";
        //var popoverContent = $($(t).parent().parent().parent().children()[2]);
        $("#ul").find("input[type=checkbox]").each(function(i,th) {
        	th.checked = t.checked;
            if ($(t).prop("checked")) {
                name += $(th).parent().text() + ",";
                console.log("name",$(th).parent().text())
                ids += $(th).val() + ",";
                console.log("ids",$(th).val())
            }
        });
//		var th = $("#ul").find("input[type=checkbox]").parent().parent().parent();
//		console.log("th"+th)
        name = name.substr(0, name.length - 1);
        ids = ids.substr(0, ids.length - 1);
        $("#txt").val(name);
        $("#ids").val(ids);
        //向后台传IP值并在后台执行命令
        
    }
    
    //勾选某一个操作
    function Choose(t) {
        var oldName = $("#txt").val();
        var name = oldName == "" ? "," + $("#txt").val() : "," + $("#txt").val() + ",";
        var ids = oldName == "" ? "," + $("#ids").val() : "," + $("#ids").val() + ",";
        var newName = $(t).parent().parent().text()
        var newid = $(t).parent().parent().val();
        
        if (t.checked) {//选中的操作
            $("#txt").val(name += newName + ",");
            $("#ids").val(ids += newid + ",");
        } else {//去掉选中的操作
            var index = name.indexOf(","+newName+",");
            var len = newName.length;
            name = name.substring(0, index) + name.substring(index + len + 1, name.length);

            var index = ids.indexOf("," + newid + ",");
            var len = newid.length;
            ids = ids.substring(0, index) + ids.substring(index + len + 1, ids.length);
        }
        name = name.substr(1, name.length - 2);
        ids = ids.substr(1, ids.length - 2);
        $("#txt").val(name);
        $("#ids").val(ids);
        //向后台传IP值并在后台执行命令
    }


//处理配置文件中的多选
function edit_group_Onchang(obj)
{
	$("#edit_config_multiple").empty()
	var group_name = $("#edit_config_group").find("option:selected").text();
		$.get("/exec_cmd",{"group_name":group_name}, function(ret){
					//根据ajax结果获取后台对应的host的IP
					for (var i = 0; i < ret.length; i++){
						$("#edit_config_multiple").append("<option value='" + i + "'>" + ret[i].ip + "</option>");  
						//$("#edit_config_multiple").append("<option value="+i+">" + ret[i].ip + "</option>");
					};
					
						//处理修改配置时的多选
				if ((group_name!='无') && (ret.length>0))
				{
					$("#edit_config_multiple").multiselect("destroy").multiselect({  
                enableClickableOptGroups: true,  
                enableCollapsibleOptGroups: true,  
                includeSelectAllOption: true,  
                buttonWidth: '400px',  
                dropRight: false,  
                maxHeight: 150,  
                onChange: function(option, checked) {  
                ips = $("#edit_config_multiple").find("option:selected").text()
                },  
                nonSelectedText: '--请选择--',  
                numberDisplayed: 10,  
                enableFiltering: true,  
                allSelectedText:'全部',  
        		}); 
			}
				else
				{
					$("#edit_config_multiple").multiselect("destroy").multiselect({  
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
	


//分发yum源中的多选 处理
function deploy_yum_Onchang(obj)
{
	$("#deploy_yum_multiple").empty()
	var group_name = $("#deploy_yum_group").find("option:selected").text();
		$.get("/exec_cmd",{"group_name":group_name}, function(ret){
					//根据ajax结果获取后台对应的host的IP
					for (var i = 0; i < ret.length; i++){
						$("#deploy_yum_multiple").append("<option value='" + i + "'>" + ret[i].ip + "</option>");  
						//$("#edit_config_multiple").append("<option value="+i+">" + ret[i].ip + "</option>");
					};
					
						//处理修改配置时的多选
				if ((group_name!='无') && (ret.length>0))
				{
					$("#deploy_yum_multiple").multiselect("destroy").multiselect({  
                enableClickableOptGroups: true,  
                enableCollapsibleOptGroups: true,  
                includeSelectAllOption: true,  
                buttonWidth: '400px',  
                dropRight: false,  
                maxHeight: 150,  
                onChange: function(option, checked) {  
                ips = $("#deploy_yum_multiple").find("option:selected").text()
                },  
                nonSelectedText: '--请选择--',  
                numberDisplayed: 10,  
                enableFiltering: true,  
                allSelectedText:'全部',  
        		}); 
			}
				else
				{
					$("#deploy_yum_multiple").multiselect("destroy").multiselect({  
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
		host_list = $("#txt").val()
		//host_list为全局变量，记录所有被选中的IP
	if (active_tab=='命令执行')//执行命令执行tab的按钮事件
	{
		
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
				
		
		
		var order = $("#salt_order").val();
		var args_linux = $("#salt_args_linux").val();
		var args_win = $("#salt_args_win").val();
		var common_cmd = $("#common_cmd").find("option:selected").text()
		if (host_list.length == 0 )
			{
				swal('命令执行失败','请选择主机','warning' )
			}
		else if(order == 0)
		{
			swal('命令执行失败','请输入要执行的命令', 'warning' )
		}
		else
		{
			
			swal({
                title: "执行:",
                text: "执行"+host_list,
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "执行",
                closeOnConfirmButtonText:"取消",
                closeOnConfirm: false,
                //allowOutsideClick :false
                
	            }, function () {
	            	$.ajax({ 
				          url:'/exec_cmd',
				          type:'get', 
				          data:{'host_list':host_list,"order":order,"args_linux":args_linux,"args_win":args_win,"common_cmd":common_cmd}, 
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
				             if (ret.code==0) {
				                    swal('成功', ret.msg, "success");
				                    count_err=0;
				                    count_scuess=0;
				                    //输出结果到页面中
						        	 //定义salt返回的一些错误
//						        	 sub_str=['False','error','No minions matched','No command was sent',
//					                        'no jid was assigned','issue any command','is not recognized',
//					                        'Usage:','ERROR: Specified cwd','is not available','salt: error:','Minion did not return',
//					                        'Passed invalid arguments'
//					                        ]
				                    $.each(ret,function(i,item){
				                    	if(i!='msg' && i!='code') 
				                    	{
				                    		if(String(item).substring(0,5)=='ERROR')
						                    	{
						                    		count_err++;
						                    		$("#failed_exec").css('display','block');
						                    		$("#failed_num").text(count_err+"个服务器执行失败,如下:");
						                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>minion_id为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
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
				             else if (ret.code == 1) {
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
	
	if (active_tab=='文件上传')
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		var form_data = new FormData();
            var file_info = $('#file_upload')[0].files[0];
            form_data.append('file',file_info);
            //if(file_info==undefined)暂且不许要判断是否有附件
                //alert('你没有选择任何文件');
                //return false
            //}

            // 提交ajax的请求
            $.ajax({
                url:"/exec_cmd/upload_files/",
                type:'POST',
                data: form_data,
                processData: false,  // tell jquery not to process the data
                contentType: false, // tell jquery not to set contentType
                success: function(ret) {
					$("#scuess_exec").css('display','block');
					$("#scuess_exec").append("<div id='scuess_html'><div  class='alert alert-block alert-success fade in'><p>"+ret.msg+"</br>"+"</p></div></div>")
					swal(
				                    	      '成功',
				                    	     ret.msg,
				                    	      'success'
				                    	 )
                },
                error:function(XMLHttpRequest,textStatus,errorThrown){ 
                				
                		$("#failed_exec").css('display','block');
						$("#failed_exec").append("<div id='failed_exec'><div  class='alert alert-block alert-error fade in'><p>"+ret.msg+"</br>"+"</p></div></div>");		
                				
				              swal(
				                    	      textStatus,
				                    	     errorThrown,
				                    	      'error'
				                    )
				          } 
            }); // end ajax
            
	}
	
	
	
	if (active_tab==='yum源初始化')
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		var yum_init_port = $("#yum_init_port").val()
		var yum_init_src = $("#yum_init_src").val()
		var create_yum_name = $("#create_yum_name").val()
		var edit_config_last = $("#edit_config_last").val()
		swal({
	                title: "初始化:",
	                text: "初始化中",
	                type: "warning",
	                showCancelButton: true,
	                confirmButtonColor: "#DD6B55",
	                confirmButtonText: "执行",
	                closeOnConfirmButtonText:"取消",
	                closeOnConfirm: false,
	                //allowOutsideClick :false
	                
		            }, function () {
						$.ajax({ 
					          url:'/exec_cmd/yum_init',
					          type:'get', 
					          data:{'yum_init_port':yum_init_port,"yum_init_src":yum_init_src}, 
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
					             if (ret.code==1) 
					             {
					             		swal('结果','执行成功' , 'success');
					             		$.each(ret,function(i,item){
					                    count_scuess=1;
					                    //输出结果到页面中
			                    		$("#scuess_exec").css('display','block');
			                    		$("#scuess_num").text(count_scuess+"个服务器执行成功,命令及结果如下:");
			                    		if(i!='code' && i!='status')
			                    		{
			                    			$("#scuess_exec").append("<div id='scuess_html'><div  class='alert alert-block alert-success fade in'><p><b>执行的命令为:"+i+"</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
			                    		}
					                });
					               }
					             else if (ret.code == -1) {
					                    swal('有异常',ret.msg, "warning");
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
		
		
		
	}
	
	
	if (active_tab==='创建指定源')
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		var create_yum_name = $("#create_yum_name").val()
		if (create_yum_name.length == 0 )
			{
				swal('命令执行失败','请输入要创建的源','warning' )
			}
		else{
		swal({
	                title: "初始化:",
	                text: "初始化中",
	                type: "warning",
	                showCancelButton: true,
	                confirmButtonColor: "#DD6B55",
	                confirmButtonText: "执行",
	                closeOnConfirmButtonText:"取消",
	                closeOnConfirm: false,
	                //allowOutsideClick :false
	                
		            }, function () {
						$.ajax({ 
					          url:'/exec_cmd/yum_create',
					          type:'get', 
					          data:{'create_yum_name':create_yum_name}, 
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
					             if (ret.code==1) 
					             {
					             		swal('结果','执行成功' , 'success');
					             		$.each(ret,function(i,item){
					                    count_scuess=1;
					                    //输出结果到页面中
			                    		$("#scuess_exec").css('display','block');
			                    		$("#scuess_num").text(count_scuess+"个服务器执行成功,命令及结果如下:");
			                    		if(i!='code' && i!='status')
			                    		{
			                    			$("#scuess_exec").append("<div id='scuess_html'><div  class='alert alert-block alert-success fade in'><p><b>执行的命令为:"+i+"</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
			                    		}
					                });
					               }
					             else if (ret.code == -1) {
					                    swal('有异常',ret.msg, "warning");
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
	
	
	if(active_tab==='分发并安装rpm包')
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		var yum_salt_rpm = $("#yum_salt_rpm").val()
		//ips为表中选择的ip
		item=$("#deploy_yum_multiple").find("option:selected")
		ips=""
		item.each(function(i,s){
		console.log("item", i,s.text)
		if (i==item.length-1){
    		ips += s.text; 
    		return false;//中断each
    		}
             ips += s.text+","; 
			});
		console.log("ips", ips)
		if (ips.length == 0 )
			{
				swal('命令执行失败','请选择主机','warning' )
			}
		else if(yum_salt_rpm=='')
			{
				swal('命令执行失败','请输入要分发的包名','warning' )
			}
		//ajax
		else{
			swal({
	                title: "分发:",
	                text: "分发"+ips,
	                type: "warning",
	                showCancelButton: true,
	                confirmButtonColor: "#DD6B55",
	                confirmButtonText: "执行",
	                closeOnConfirmButtonText:"取消",
	                closeOnConfirm: false,
	                //allowOutsideClick :false
	                
		            }, function () {
						$.ajax({ 
					          url:'/exec_cmd/yum_deploy',
					          type:'get', 
					          data:{'ips':ips,"yum_salt_rpm":yum_salt_rpm}, 
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
					                    console.log("i",i)
					                    console.log("item",item)
					                    	if(i!='msg' && i!='code'&&i!='status') 
					                    	{
					                    		if(String(item).substring(0,5)=='ERROR')
							                    	{
							                    		count_err++;
							                    		$("#failed_exec").css('display','block');
							                    		$("#failed_num").text(count_err+"个服务器执行失败,如下:");
							                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>minion_id为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
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
	}//分发yum包完
	
	if (active_tab==='文件修改')
	{
		//首先清空所有的执行结果
		$("#scuess_exec").empty();
		$("#scuess_html").empty();
		$("#scuess_num").empty();
		 $("#failed_exec").empty();
		 $("#failed_html").empty();
		 $("#failed_num").empty();
		var edit_config_linux = $("#edit_config_linux").val()
		var edit_config_win = $("#edit_config_win").val()
		var edit_config_pre = $("#edit_config_pre").val()
		var edit_config_last = $("#edit_config_last").val()
		//ips为表中选择的ip
		item=$("#edit_config_multiple").find("option:selected")
		ips=""
		item.each(function(i,s){
		console.log("item", i,s.text)
		if (i==item.length-1){
    		ips += s.text; 
    		return false;//中断each
    		}
             ips += s.text+","; 
			});
		if (ips.length == 0 )
			{
				swal('命令执行失败','请选择主机','warning' )
			}
		else if((edit_config_linux=='' && edit_config_win=='')||edit_config_last=='')
			{
				swal('命令执行失败','请输入配置文件路径或要修改的内容','warning' )
			}
		//ajax
		else{
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
					          url:'/exec_cmd/edit_config',
					          type:'get', 
					          data:{'ips':ips,"edit_config_linux":edit_config_linux,"edit_config_win":edit_config_win,"edit_config_pre":edit_config_pre,"edit_config_last":edit_config_last}, 
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
					             if (ret.code==-1) {
					                    swal('结果', ret.msg, ret.status);
					                    count_err=0;
					                    count_scuess=0;
					                    //输出结果到页面中
					                    $.each(ret,function(i,item){
					                    	if(i!='msg' && i!='code'&&i!='status') 
					                    	{
					                    		if(String(item).substring(0,5)=='ERROR')
							                    	{
							                    		count_err++;
							                    		$("#failed_exec").css('display','block');
							                    		$("#failed_num").text(count_err+"个服务器执行失败,如下:");
							                    		$html = $("<div id='failed_html'><div  class='alert alert-block alert-error fade in'><p><b>minion_id为:"+i+":</b></br>"+JSON.stringify(item, null, '\nt')+"</br>"+"</p></div></div>")
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
					             else if (ret.code == 1) {
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
	
	if (null==active_tab||""==active_tab||active_tab=='home')
	{
		//salert("这是hometab")
		
	}
		
		//$.ajax({ 
//					          url:'exec_cmd',
//					          type:'get', 
//					          data:{'host_list':host_list.pop()}, 
//					          //timeout:15000, 
//					          beforeSend:function(XMLHttpRequest){ 
//					              //执行前提示 
//					              alert(123)
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
//					             $("#loading").empty(); 
//					           }, 
//					           error:function(XMLHttpRequest,textStatus,errorThrown){ 
//					              swal(
//					                    	      textStatus,
//					                    	     errorThrown,
//					                    	      'error'
//					                    )
//					             $("#loading").empty(); 
//					          } 
//						}); 
		//ajax完
	}






//
//function selectOnchang(obj){ 
////获取被选中的option标签选项 
//alert(123)
//var select_group = $("#select_group").find("option:selected").text();
////ajax获取后台数据
//$.get("/getdata/sss/",{'select_group':select_group}, function(ret){
////将后台数据显示在前台的textarea中
//						
//                             var res = [];   
//                             var num=1;  
//                             //动态生成表头
////                             res.push("<tr>")
////                             res.push("<th>IP</th>")
////                             res.push("<th>IP</th>")
////                             res.push("<th>IP</th>")
////                             res.push("<th>IP</th>")
////                             res.push("</tr>")
//                             jQuery.each(ret, function(i,item){  
//                                 res.push(item.ip);  
//                                 res.push( item.Createtime);  
//                                 res.push( item.username);  
//                                 res.push( item.hostname);
//                                 res.push("\n")
//                                 num++;
//								
//								//动态生成表格写入tdata中
////								res.push('<tr>');  
////                                 res.push('<td align="center" >' + num + '</td>');  
////                                 res.push('<td align="center" >' + item.ip + '</td>');  
////                                 res.push('<td align="center" >' + item.Createtime + '</td>');  
////                                 res.push('<td align="center" >' + item.username + '</td>');
////                                 res.push('</tr>');  
////                                 num++;  
//
//  
//                              });  
//                              //$("#largetextarea").empty().val(res.join(""));  
//                              //将结果写入隐藏的表格中
//                              //$("#tdata").html(res);
//                              $("#exescuess").empty().val(res.join(""));  
//                              //页面未执行的textarea是先隐藏的，如果有未执行的结果则，在这里将隐藏改为显示出来
//                              //$("#exefaild").empty().val(res.join(""));  
//                              document.getElementById("weizhixing").style.display="block";
//                              $("#exefaild").empty().val(res.join(""));  
//			    	 //将表的第一行数据alex修改为ret.result123
//			    	 //$("#largetextarea").val("adasfsd")
//			        })
//}
//
////给重启，停止等添加事件
//$('#instance ul').on('click','li',function(){
//    alert($(this).text());
//})
