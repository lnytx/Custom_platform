$(function(){

			//动态改变span的class
			$("#sample_2 > tbody tr").each(function(){ 
  			//获取tr 的Id 
  			var status = $(this).find("td").eq(4).find("span").text()
  			if (status=='Accepted')//Accepted
  			 {
  			 	$(this).find("td").eq(4).find("span").addClass('label label-success')
  			 	//如果已添加的就隐藏key_accept按钮
  			 	//只有在Unaccepted中的salt_id才能接受与拒绝操作
  			 	$(this).find("td").eq(5).find("#key_accept").hide();
  			 	$(this).find("td").eq(5).find("#key_reject").hide();
  			 }
  			 if (status=='Unaccepted')//Unaccepted
  			 {
  			 	$(this).find("td").eq(4).find("span").addClass('label label-danger')
  			 }
  			 if (status=='Rejected')//Denied
  			 {
  			 	$(this).find("td").eq(4).find("span").addClass('label label-warning')
  			 	$(this).find("td").eq(5).find("#key_accept").hide();
  			 	$(this).find("td").eq(5).find("#key_reject").hide();
  			 }
  			 if (status=='Denied')//Denied
  			 {
  			 	$(this).find("td").eq(4).find("span").addClass('label label-info')
  			 	$(this).find("td").eq(5).find("#key_accept").hide();
  			 	$(this).find("td").eq(5).find("#key_reject").hide();
  			 }
			  //获取tr 这一行的text 
			  //alert(" text="+trId); 
  			 });
			
			//$('#key_status').attr("'class", "label label-danger")
			//class="label label-danger"
//			class="label label-warning"
//			class="label label-success"
	
	//accept minion_key
	$(".key_accept").click(function(){
		var ip = $(this).parent().parent().attr('ip');
		var minion_key = $(this).parent().parent().attr('minion_id');
		swal({
                title: "添加minion_key:",
                text: "添加"+minion_key,
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "执行",
                closeOnConfirmButtonText:"取消",
                closeOnConfirm: false,
                //allowOutsideClick :false
                
	            }, function () {
	            	$.ajax({ 
				          url:'/minion_key/accept_minionkey',
				          type:'get', 
				          data:{'ip':ip,"minion_key":minion_key}, 
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
				            if (ret.code == 1) {
			                    swal(ret.msg, '', "success");
			                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
			                        location.reload();
			                    });
			               	 } 
				             else if (ret.code == 0) {
				                    swal('有异常',ret.msg, "warning");
				                } 
				        	else if(ret.code == -1){
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
	})
	
	
	
	$(".key_reject").click(function(){
		var ip = $(this).parent().parent().attr('ip');
		var minion_key = $(this).parent().parent().attr('minion_id');
		swal({
                title: "添加minion_key:",
                text: "添加"+minion_key,
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "执行",
                closeOnConfirmButtonText:"取消",
                closeOnConfirm: false,
                //allowOutsideClick :false
                
	            }, function () {
	            	$.ajax({ 
				          url:'/minion_key/reject_mminionkey',
				          type:'get', 
				          data:{'ip':ip,"minion_key":minion_key}, 
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
				            if (ret.code == 1) {
			                    swal(ret.msg, '', "success");
			                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
			                        location.reload();
			                    });
			               	 } 
				             else if (ret.code == 0) {
				                    swal('有异常',ret.msg, "warning");
				                } 
				        	else if(ret.code == -1){
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
	})
	
	
	//删除key
	$(".key_delete").click(function(){
		var ip = $(this).parent().parent().attr('ip');
		var minion_key = $(this).parent().parent().attr('minion_id');
		swal({
                title: "添加minion_key:",
                text: "添加"+minion_key,
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "执行",
                closeOnConfirmButtonText:"取消",
                closeOnConfirm: false,
                //allowOutsideClick :false
                
	            }, function () {
	            	$.ajax({ 
				          url:'/minion_key/delete_minionkey',
				          type:'get', 
				          data:{'ip':ip,"minion_key":minion_key}, 
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
				            if (ret.code == 1) {
			                    swal(ret.msg, '', "success");
			                    $('.confirm').click(function () {   //额外绑定一个事件，当确定执行之后返回成功的页面的确定按钮，点击之后刷新当前页面或者跳转其他页面
			                        location.reload();
			                    });
			               	 } 
				             else if (ret.code == 0) {
				                    swal('有异常',ret.msg, "warning");
				                } 
				        	else if(ret.code == -1){
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
	})
	
});
