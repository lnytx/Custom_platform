$(function(){
	//查看详情
	$('.host_info').click(function () {
		alert(123)
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
//        $('#ip').attr(hostname);  
        
        //alert($username).text())
        $("#h_edit_ip").val(ip)
        $("#host_edit_ip").val(ip)
        //select选择的值
        var type=['Linux','Debian','Ubuntu','RedHat','CentOS','Fedora','OpenSuse','Windows','Others']
//        获取ostype在数组中的位置，用来确定前台的select选项显示
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
        
        
        //2、获取模态框中修改的值，并写入数据库中
        $("#host_edit_save").click(function(){
        //获取前台数据
        	var os = $("#host_edit_ostype").find("option:selected").text();
        	alert(os)
        	$.get("/host_edit/",{'jsonStr':jsonStr}, function(ret){
			    //接收来自后台返回的数据
			    	 //将表的第一行数据alex修改为ret.result123
			    	 oTable.fnUpdate(ret.result, nRow, 0, false);
			        })
        	alert($("#host_edit_ip").val())
        	
        })
        
        
//		$('#edit').on('hidden.bs.modal', function () {
//				alert("当模态框完全对用户隐藏时触发。")
//			})
	});
});


