$(function(){

	
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
	
	//添加group时保存菜单的事件
	$("#add_group_save").click(function(){
		//获取前面选择每行的IP，传到后台处理
		var ips=[]
		$(":checkbox[name='td_check']").each(function(){
			if ($(this).attr("checked"))
			{
				var text = $(this).attr('value');
				ips.push(text)
			}
	    })
	    //数组转字符串
	    ip_list= ips.join(",")
	    var group_name = $("#add_new_group option:selected").attr("value")
	    var group_id = $("#add_new_group option:selected").attr("group_id")//取得上面的group_id值
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
		var group_name = $("#create_group_name").val()
		var remark = $("#create_group_remark").val()
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
        var json_ip = $("#host_add_ip").val()
        var json_hostname = $("#host_add_hostname").val()
        var json_username = $("#host_add_username").val()
        var json_application = $("#host_add_application").val()
        var json_port = $("#host_add_port").val()
        var json_group = $("#host_add_group").val()
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
        var minion_id = $(this).parent().parent().attr('minion_id');
//        $('#ip').attr(hostname);  
        
        //$("#hostname").text("World");
        
        //alert($username).text())
        $("#h_ip").text(ip)
        $("#host_info_ip").text(ip)
        $("#host_info_ostype").text(ostype)
        $("#host_info_hostname").text(hostname)
        $("#host_info_username").text(username)
        $("#host_info_application").text(application)
        $("#host_info_port").text(port)
        $("#host_edit_group").text(group_name)
        
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
        
        $("#h_edit_ip").val(ip)
        $("#host_edit_ip").val(ip)
        //select选择的值
        var type=['Linux','Debian','Ubuntu','RedHat','CentOS','Fedora','OpenSuse','Windows','Others']
		//获取ostype在数组中的位置，用来确定前台的select选项显示
        var i=$.inArray(ostype, type);
        if (i > 0 )//i>0则说明在数组中找到了对应的值，否则为-1
        	{
        		$(".host_edit_select option[value='"+i+"']").attr("selected","selected");
        	}
        else
        	{
        		$(".host_edit_select option[value='"+8+"']").attr("selected","selected");
        	}
        
        $("#host_edit_hostname").val(hostname)
        $("#host_edit_username").val(username)
        $("#host_edit_application").val(application)
        $("#host_edit_port").val(port)
        $("#host_edit_group").val(group_name)
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
        var json_group = $("#host_edit_group").val()
        var json_pwd = $("#host_edit_pwd").val()
        var host_edit_minion_id = $("#host_edit_minion_id").val()
        var json_ostype = $("#host_edit_ostype").find("option:selected").text();
        	 //拼接字符串，传入后台更新
        var edit_str = ""
        //ip是指原来的IP，修改input之前的IP
        edit_str=json_ip+','+json_hostname+','+json_username+','+json_application+','
        	+json_port+','+json_group+','+json_ostype+','+json_pwd+','+host_edit_minion_id+','+ip
        	//相当于前面还有个cmdb接着前面的url
        	$.get("edit_host/",{'edit_str':edit_str}, function(ret){
        		
			        })
			        
					
				//提示信息
				swal("成功!", "编辑成功", "success")
					//swal({
//							  title: "保存",
//							  text: "数据保存成功",
//							  type: "success",
//							  timer: 2000,
//							  showConfirmButton: false
//							});

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
    			$.get("update_host/",{'minion_id':minion_id,'ip':ip}, function(ret){
		    				if (ret.code == 1||ret.code==0) {
			                    swal('更新成功', '更新成功', "success");
			                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
			                        location.reload();
			                    });
			                } 
			        	
			        	else {
			                   // swal(ret.msg, "", "error");
			                    swal(
			                    	      '失败',
			                    	     ret.msg,
			                    	      'success'
			                    	 )
			            }
    			})
    		}
    		
    })
    

    $("#loadgif").click(function () {
    			alert("dsafs")
				
		$.ajax({ 
          url:'ajax_test',
          type:'get', 
          data:'name=ZXCVB', 
          timeout:15000, 
          beforeSend:function(XMLHttpRequest){ 
              //alert('远程调用开始...'); 
              $("#loading").html("<img src='/static/image/ajax-loading.gif' />"); 
              sleep
         }, 
         success:function(data,textStatus){ 
             alert('开始回调，状态文本值：'+textStatus+' 返回数据：'+data); 
             // $("#loading").empty(); 
           }, 
          complete:function(XMLHttpRequest,textStatus){ 
              // alert('远程调用成功，状态文本值：'+textStatus); 
             $("#loading").empty(); 
           }, 
           error:function(XMLHttpRequest,textStatus,errorThrown){ 
              alert('error...状态文本值：'+textStatus+" 异常信息："+errorThrown); 
             $("#loading").empty(); 
          } 
       }); 
		});
});
