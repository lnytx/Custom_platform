$(function(){
	
		$("#sample_2 > tbody tr").each(function(){ 
  			//获取tr 的Id 
  			var status = $(this).find("td").eq(8).find("span").text()
  			console.log("status",status)
  			if (status=='Up')//Accepted
  			 {
  			 	$(this).find("td").eq(8).find("span").addClass('label label-success')
  			 }
  			 if (status=='Down')//Unaccepted
  			 {
  			 	$(this).find("td").eq(8).find("span").addClass('label label-danger')
  			 }
  			 if (status=='Other')//Denied
  			 {
  			 	$(this).find("td").eq(8).find("span").addClass('label label-warning')
  			 }
  			 });
	
	$("#check_host_all").click(function(){
		//$("input[type='checkbox']").attr("checked",true);
		if(this.checked)
			{
				$("tbody :checkbox").attr("checked",true)
			}
		else
			{
				$("tbody :checkbox").attr("checked",false)
			}
	})
	
//	//选中行的值
//	$(":checkbox[name='td_check']").click(function() {
//            var ip_list = new Array();
//            var i = 0;
//            var ip = $(this).attr('value');
//            ip_list +=ip+','
//           });
//	
	
	$("#tbody :checkbox").click(function(){
		all_check()
	});
			//设置全选复选框 
			function all_check()
			{
				//全选时的总数
				var check_num = $("#tbody :checkbox").size();
				var chk = 0;
				var ip_list=[];
				$("#tbody :checkbox").each(function(){
					if ($(this).attr("checked"))
					{
						chk++;
					}
					
				});
				if(check_num==chk)
					{
						$("#check_host_all").attr("checked",true);
					}
				else
					{
						$("#check_host_all").attr("checked",false);
					}
			}
//			all_check()
//	$("input:checkbox").bind("click",function(){  
//			
//			if ($("input[name='td_check']").attr("checked",false))
//				{alert('取消')}
//            });   
	
//	$check_host_all.on('click', function () {
//        $('tbody input[type="checkbox"]').each(function () {
//            this.checked = $checkall[0].checked;
//            alert(123)
//        })
//    });
	
	$(".group_add").click(function(){
		//这里是处理前台组的下拉列表的
		$("#add_new_group").empty();//首先清空，否则每点一次都会有重复数据（也可以使用拼接html的方式）
		add_str='add_group'
		$.get("group_list/",{"add_str":add_str}, function(ret){
			//动态添加select选项,从后台数据库获取
			for (var i = 0; i < ret.length; i++) 
				{
		 			$("#add_new_group").append("<option group_id="+ret[i].group_id+">" + ret[i].group_name + "</option>");
		 		}
			})
	})
	
	
	//动态添加组名
	$(".host_add").click(function(){
		$.get("group_list/",{"add_str":''}, function(ret){
			//动态添加select选项,从后台数据库获取
			console.log(ret)
			for (var i = 0; i < ret.length; i++) 
				{
		 			$("#host_add_group").append("<option group_id="+ret[i].group_id+">" + ret[i].group_name + "</option>");
		 		}
			})
	})
	
	//添加group时保存菜单的事件
	$("#add_group_save").click(function(){
		//获取前面选择每行的IP，传到后台处理
		var ips=[]
		$(":checkbox[name='td_check']").each(function(){
			if ($(this).attr("checked"))
			{
				var text = $.trim($(this).attr('value'));
				ips.push(text)
			}
	    })
	    //数组转字符串
	    ip_list= ips.join(",")
	    var group_name = $.trim($("#add_new_group option:selected").attr("value"))
	    var group_id = $.trim($("#add_new_group option:selected").attr("group_id"))//取得上面的group_id值
		//传到后台，更新,并将group_name一起传过去
		$.get("group_add/",{'ip_list':ip_list,'group_name':group_name,'group_id':group_id}, function(ret){
			//前台提示信息
						if (ret.code == 1) {
			                swal(ret.msg, '', "success");
			                $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
			                    location.reload();
			                });
			            } 
			    	
			    	else {
			               // swal(ret.msg, "", "error");
			                swal(
			                	      '错误',
			                	     ret.msg,
			                	      'warning'
			                	 )
			        }
			
			});
		
	})
	
	//创建新group时保存菜单的事件
	$("#create_group_save").click(function(){
		var group_name = $.trim($("#create_group_name").val())
		var remark = $.trim($("#create_group_remark").val())
		var cretat_group_str=group_name+','+remark
		$.get("group_create/",{'cretat_group_str':cretat_group_str}, function(ret){
			    		//后台返回ret的格式为{code:'code'},code=1为sql执行成功，-1为失败
			        	if (ret.code == 1) {
			                    swal(ret.msg, '', "success");
			                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
			                        location.reload();
			                    });
			                } 
			        	
			        	else {
			                   // swal(ret.msg, "", "error");
			                    swal(
			                    	      '错误',
			                    	     ret.msg,
			                    	      'warning'
			                    	 )
			            }
			   		 });
	})
	
	
	$("#host_add_save").click(function(){
        //获取前台数据
        var json_ip = $.trim($("#host_add_ip").val());
        
        var json_hostname = $.trim($("#host_add_hostname").val())
        var json_username = $.trim($("#host_add_username").val())
        var json_application = $.trim($("#host_add_application").val())
        var json_port = $.trim($("#host_add_port").val())
        //获取组名
        
        var json_group =  $("#host_add_group").find("option:selected").text();
        var json_pwd = $("#host_add_pwd").val()
        var json_minion_id = $("#host_add_minion_id").val()
        var json_ostype = $("#host_add_ostype").find("option:selected").text();
        	 //拼接字符串，传入后台更新
        var add_str = ""
        var	arr_str = ""
        arr_str=json_ip+','+json_username+','+json_port+','+json_pwd
    	//转成数组，查看数组中是否有空值
        sub_str = arr_str.split(',')
        result = $.inArray("", sub_str);//为-1时表示没有空值，大于0则表示有匹配到了空值
        //ip是指原来的IP，修改input之前的IP
        add_str=json_ip+','+json_hostname+','+json_username+','+json_application+','
        	+json_port+','+json_group+','+json_ostype+','+json_pwd+','+json_minion_id
        	//alert(add_str)
        	//相当于前面还有个cmdb接着前面的url
				//提示信息
        	if (result >=0)
        	{
                // swal(ret.msg, "", "error");
                 swal(
                 	      '错误',
                 	      '有必填项未写值',
                 	      'error'
                 	 )
        	}
        	else{
			        $.get("add_host/",{'add_str':add_str}, function(ret){
			    		//后台返回ret的格式为{code:'code'},code=1为sql执行成功，-1为失败
			        	if (ret.code == 1) {
			                    swal(ret.msg, '', "success");
			                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
			                        location.reload();
			                    });
			                } 
			        	
			        	else {
			                   // swal(ret.msg, "", "error");
			                    swal(
			                    	      '错误',
			                    	     ret.msg,
			                    	      'warning'
			                    	 )
			            }
			   		 });
        	}
							//提示信息
        	
        //最后关闭模态框后的动作
//		$('#edit').on('hide.bs.modal', function () {
//				alert("修改完成")
//			})
	});

	//查看详情,如果使用id取值的话有时会有问题，只能使用类名来取值了
	$('.host_info').click(function () {
		
		//获取当前行中的某一列数据
		//alert($(this).parent().parent().children("td").get(1).innerHTML);
		//alert($(this).parent().parent().attr('nid'));
		
        var ip = $.trim($(this).parent().parent().attr('ip'));
        var minion_id = $.trim($(this).parent().parent().attr('minion_id'));
//        $("#h_info_ip").text(ip)
        
        $.get("host_info/",{'ip':ip,'minion_id':minion_id}, function(ret){
        
				if (ret.code==2) 
				{
					$("#info").modal('hide');
					$("#host_info_ip").empty()
			        $("#host_info_minion_id").empty()
			        $("#host_info_kernel").empty()
			        $("#host_info_osversion").empty()
			        $("#host_info_cpu_model").empty()
			        $("#host_info_num_cpus").empty()
			        $("#host_edit_manufacturer").empty()
			        $("#host_info_osfullname").empty()
			        $("#host_info_mem_total").empty()
			        $("#host_info_cpuarch").empty()
			        $("#host_info_roles").empty()
			        $("#host_info_kernelrelease").empty()
			        $("#host_info_saltversion").empty()
			        $("#host_info_shell").empty()
			        $("#host_info_username").empty()
			        $("#host_info_disk_total").empty()
		          	swal('失败', ret.msg, 'error');
		        }
		    	else
		    	{
        			$("#host_info_ip").val(ret.ip)
			        $("#host_info_minion_id").val(ret.minion_id)
			        $("#host_info_kernel").val(ret.kernel)
			        $("#host_info_osversion").val(ret.osversion)
			        $("#host_info_cpu_model").val(ret.cpu_model)
			        $("#host_info_num_cpus").val(ret.num_cpus)
			        $("#host_edit_manufacturer").val(ret.manufacturer)
			        $("#host_info_osfullname").val(ret.osfullname)
			        $("#host_info_mem_total").val(ret.mem_total)
			        $("#host_info_cpuarch").val(ret.cpuarch)
			        $("#host_info_roles").val(ret.roles)
			        $("#host_info_kernelrelease").val(ret.kernelrelease)
			        $("#host_info_saltversion").val(ret.saltversion)
			        $("#host_info_shell").val(ret.shell)
			        $("#host_info_username").val(ret.username)
			        $("#host_info_disk_total").val(ret.total)
			      }
			      })
//        $('#ip').attr(hostname);  
        
        //$("#hostname").text("World");
        
        //alert($('#host_see').find("label[name='username']").text())
        //$('#host_see').find('label[id="hostname"]').text('122');
    });
	
	//编辑主机
	$(".host_edit").click(function(){
	
		var nid = $(this).parent().parent().attr('nid');
        var ip = $(this).parent().parent().attr('ip');
        var hostname = $(this).parent().parent().attr('hostname');
        var application = $(this).parent().parent().attr('application');
        var username = $(this).parent().parent().attr('username');
        var ostype = $(this).parent().parent().attr('ostype');
        var port = $(this).parent().parent().attr('port');
        var status = $(this).parent().parent().attr('status');
        var group_name = $(this).parent().parent().attr('group_name');
        var pwd = $(this).parent().parent().attr('pwd');
        var host_edit_minion_id = $(this).parent().parent().attr('minion_id');
        var host_edit_minion_old_id = host_edit_minion_id
        //记录下之前的值，然后与修改后的值比较，得到修改前后的值
        var edit_before = [];
        edit_before.push(ip);
        edit_before.push(hostname);
        edit_before.push(ostype);
        edit_before.push(application);
        edit_before.push(username);
        edit_before.push(port);
        edit_before.push(group_name);
        edit_before.push(pwd);
        edit_before.push(host_edit_minion_id);
        console.log("edit_before",edit_before)
        
        $("#h_edit_ip").text(ip)
        $("#host_edit_ip").val(ip)
        
        
        
        
        $("#host_edit_group").empty();//首先清空，否则每点一次都会有重复数据（也可以使用拼接html的方式）
        $("#host_edit_group").append("<option>" + group_name + "</option>");
        $.get("group_list/",{"add_str":''}, function(ret){
			//动态添加select选项,从后台数据库获取
			for (var i = 0; i < ret.length; i++) 
				{
					if(ret[i].group_name == group_name)
						{continue;}
		 			$("#host_edit_group").append("<option value="+ret[i].group_id+">" + ret[i].group_name + "</option>");
		 		}
			})
        
        
        //select选择的值
        var type=['Linux','Debian','Ubuntu','RedHat','CentOS','Fedora','OpenSuse','Windows','Aix','Others']
		//获取ostype在数组中的位置，用来确定前台的select选项显示
        var i=$.inArray(ostype, type);
        if (i > 0 )//i>0则说明在数组中找到了对应的值，否则为-1
        	{
        		$(".host_edit_select option[value='"+i+"']").attr("selected","selected");
        	}
        else //选择others
        	{
        		$(".host_edit_select option[value='"+9+"']").attr("selected","selected");
        	}
        
        
        
        $("#host_edit_hostname").val(hostname)
        $("#host_edit_username").val(username)
        $("#host_edit_application").val(application)
        $("#host_edit_port").val(port)
        //$("#host_edit_group").val(group_name)
        $("#host_edit_pwd").val(pwd)
        $("#host_edit_minion_id").val(host_edit_minion_id)
        
       // 获取form元素的值
        
        
        //2、获取模态框中修改的值，并写入数据库中
        $("#host_edit_save").click(function(){
        //获取前台数据
        var json_ip = $("#host_edit_ip").val()
        var json_hostname = $("#host_edit_hostname").val()
        var json_username = $("#host_edit_username").val()
        var json_application = $("#host_edit_application").val()
        var json_port = $("#host_edit_port").val()
        var json_group = $("#host_edit_group").find("option:selected").text();
        var json_pwd = $("#host_edit_pwd").val()
        var host_edit_minion_id = $("#host_edit_minion_id").val()
        var json_ostype = $("#host_edit_ostype").find("option:selected").text();
        	 //拼接字符串，传入后台更新
        var edit_str = ""
        //ip是指原来的IP，修改input之前的IP
        edit_str=json_ip+','+json_hostname+','+json_username+','+json_application+','
        	+json_port+','+json_group+','+json_ostype+','+json_pwd+','+host_edit_minion_id+','+ip+','+host_edit_minion_old_id
        	
        	
        //记录下修改之后的值，然后与修改后的值比较，得到修改前后的值
        var edit_after = [];
        edit_after.push(json_ip);
        edit_after.push(json_hostname);
        edit_after.push(json_ostype);
        edit_after.push(json_application);
        edit_after.push(json_username);
        edit_after.push(json_port);
        edit_after.push(json_group);
        edit_after.push(json_pwd);
        edit_after.push(host_edit_minion_id);
        console.log("edit_after",edit_after)
        //比较修改前后的值，将修改的提取出来
        var edit_result={}//记录被修改元素修改前的值,修改前的为key，修改后的为value
        for(var j= 0; j < edit_before.length; j++)
        {  
        	var before = edit_before[j];  
            var after = edit_after[j];  
            if(before != after) 
            {  //相同则表明未修改
            	edit_result[before]=after
            }  
         }
         var edit_str
         for(var j= 0; j < edit_result.length; j++)
         {
         	
         }
          console.log("修改前后的值",edit_result)
		//edit_result['edit_str']=edit_str
        	//相当于前面还有个cmdb接着前面的url
        	$.get("edit_host/",{'edit_str':edit_str,'edit_result':JSON.stringify(edit_result)}, function(ret){
        		console.log("ret",ret)
        		 if (ret.code==-1)
        		 {
        			 swal("失败!", ret.msg, "error");
 					$('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
 	                                location.reload();
 	                            });
        		 }
        		 if(ret.code==1)
        		 {
        			 swal("成功！", ret.msg, "success");
  						$('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
  	                                location.reload();
  	                            });
        		 }
			   });
			        
					
				//提示信息
				
        	
        })
        
        //最后关闭模态框后的动作
//		$('#edit').on('hide.bs.modal', function () {
//				alert("修改完成")
//			})
	});
	
	
	
	//删除操作
	
	$('.host_delete').click(function () {
	
		//获取IP，根据IP删除对应的记录（级联删除host_info表）
		var ip = $(this).parent().parent().attr('ip');
		var del_str = ip
		//提示信息
				 swal({
	                title: "删除:"+ip,
	                text: "删除后将无法恢复，请谨慎操作！",
	                type: "warning",
	                showCancelButton: true,
	                confirmButtonColor: "#DD6B55",
	                confirmButtonText: "确定",
	                closeOnConfirmButtonText:"123",
	                closeOnConfirm: false
	            }, function () {
	            		$.get("del_host/",{'del_str':del_str}, function(ret){
	            		//后台返回ret的格式为{code:'code'},code=1为sql执行成功，-1为失败
	            		if (ret.code === 1) {
	                            swal("删除成功！", "", "success");
	                            $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
	                                location.reload();
	                            });
	
	                        } else {
	                            swal("删除失败！", "", "error");
	                            $('.confirm').click(function () {   //
	                                location.reload();
	                            });
	                    }
               		 });
       			 });
    });
    
    
    
    $(".host_update").click(function(){
    	var ip = $(this).parent().parent().attr('ip');
    	var minion_id = $(this).parent().parent().attr('minion_id');
    	if (minion_id=='None' || minion_id=='undefined')
    		{
    			swal("更新失败,请安装salt-minion,并填写minin_id", "", "error");
    		}
    	else
    		{
    			//$.get("update_host/",{'minion_id':minion_id,'ip':ip}, function(ret){
//		    				if (ret.code == 1||ret.code==0) {
//			                    swal('更新成功', '更新成功', "success");
//			                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
//			                        location.reload();
//			                    });
//			                } 
//			        	
//			        	else {
//			                   // swal(ret.msg, "", "error");
//			                    swal(
//			                    	      '失败',
//			                    	     ret.msg,
//			                    	      'success'
//			                    	 )
//			            }
//    			})


				
				$.ajax({ 
					          url:'update_host',
					          type:'get', 
					          data:{'minion_id':minion_id,'ip':ip}, 
					          //timeout:15000, 
					          beforeSend:function(XMLHttpRequest){ 
					              //alert('远程调用开始...'); 
//					              $("#loading").html("<img src='/static/image/ajax-loading.gif' />"); 
					        	  swal({
				        	            title:'loading...',
				        	            text:'正在加载数据',
				        	            imageUrl:'/static/image/ajax-loading.gif',
				        	            showConfirmButton: false//去掉确认的按钮
				        	        });
					         }, 
					         success:function(ret,textStatus){ 
					             //alert('开始回调，状态文本值：'+textStatus+' 返回数据：'+data.msg); 
					             // $("#loading").empty(); 
					        	   
					             if (ret.code == 0) {
					                    swal('更新成功', ret.msg, "success");
					                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
					                        location.reload();
					                    });
					                } 
					             else if (ret.code == 1) {
					                    swal('更新成功', ret.msg, "success");
					                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
					                        location.reload();
					                    });
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
//					             $("#loading").empty(); 
					           }, 
					           error:function(XMLHttpRequest,textStatus,errorThrown){ 
					              swal(
					                    	      textStatus,
					                    	     errorThrown,
					                    	      'error'
					                    )
				                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
				                        location.reload();
				                    });
//					             $("#loading").empty(); 
					          } 
						}); 

    		}
    		
    })
    

   // $("#loadgif").click(function () {
//    			alert("dsafs")
//				
//		$.ajax({ 
//          url:'ajax_test',
//          type:'get', 
//          data:'name=ZXCVB', 
//          timeout:15000, 
//          beforeSend:function(XMLHttpRequest){ 
//              //alert('远程调用开始...'); 
//              $("#loading").html("<img src='/static/image/ajax-loading.gif' />"); 
//              sleep
//         }, 
//         success:function(data,textStatus){ 
//             alert('开始回调，状态文本值：'+textStatus+' 返回数据：'+data); 
//             // $("#loading").empty(); 
//           }, 
//          complete:function(XMLHttpRequest,textStatus){ 
//              // alert('远程调用成功，状态文本值：'+textStatus); 
//             $("#loading").empty(); 
//           }, 
//           error:function(XMLHttpRequest,textStatus,errorThrown){ 
//              alert('error...状态文本值：'+textStatus+" 异常信息："+errorThrown); 
//             $("#loading").empty(); 
//          } 
//       }); 
//		});
    
    
});
