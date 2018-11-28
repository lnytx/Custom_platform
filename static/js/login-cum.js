$(function(){
        //main function to initiate the module
        
        	
           $('.login-form').validate({
	            errorElement: 'label', //default input error message container
	            errorClass: 'help-inline', // default input error message class
	            focusInvalid: false, // do not focus the last invalid input
	            rules: {
	                username: {
	                    required: true
	                },
	                password: {
	                    required: true
	                },
	                remember: {
	                    required: false
	                }
	            },

	            messages: {
	                username: {
	                    required: "Username is required."
	                },
	                password: {
	                    required: "Password is required."
	                }
	            },

	            invalidHandler: function (event, validator) { //display error alert on form submit   
	                $('.alert-error', $('.login-form')).show();
	            },

	            highlight: function (element) { // hightlight error inputs
	                $(element)
	                    .closest('.control-group').addClass('error'); // set error class to the control group
	            },

	            success: function (label) {
	                label.closest('.control-group').removeClass('error');
	                label.remove();
	            },

	            errorPlacement: function (error, element) {
	                error.addClass('help-small no-left-padding').insertAfter(element.closest('.input-icon'));
	            },

	        });
	        $("#login_sub").on('click',function(){
	        	$("#msg_notice").empty()
	        })
	        
//	        $("#login_sub").on('click',function(){
//	        var login_username = $("#login_username").val();
//	        var login_password = $("#login_password").val();
//	        console.log("#login_username",login_username,login_password)
//	        //登录按钮事件
//	        	$.ajax({
//            type:'POST',
//            url:"/login/",
//            async:false,
//            data:{'login_username':login_username,"login_password":login_password},
//            success: function(data){
//            console.log("data",data)
//                if (data){
//                    $("#msg_notice").html("登录成功！");
//                    window.location.href = "index.html";
//                    return true;
//                }
//                else {
//                    $("#msg_notice").html("用户名或密码错误，请重新输入！");
//                    return false;
//                }
//                },
//		        error:function(XMLHttpRequest,textStatus,errorThrown){ 
//				              swal(
//				                    	      textStatus,
//				                    	     errorThrown,
//				                    	      'error'
//				                    )
//				          } 
//		        })
//	        
//	      	  })
	        });

	      //  $('.login-form input').keypress(function (e) {
//	            if (e.which == 13) {
//	                if ($('.login-form').validate().form()) {
//	                    window.location.href = "index.html";
//	                }
//	                return false;
//	            }
//	        });
//
//	        $('.forget-form').validate({
//	            errorElement: 'label', //default input error message container
//	            errorClass: 'help-inline', // default input error message class
//	            focusInvalid: false, // do not focus the last invalid input
//	            ignore: "",
//	            rules: {
//	                email: {
//	                    required: true,
//	                    email: true
//	                }
//	            },
//
//	            messages: {
//	                email: {
//	                    required: "Email is required."
//	                }
//	            },
//
//	            invalidHandler: function (event, validator) { //display error alert on form submit   
//
//	            },
//
//	            highlight: function (element) { // hightlight error inputs
//	                $(element)
//	                    .closest('.control-group').addClass('error'); // set error class to the control group
//	            },
//
//	            success: function (label) {
//	                label.closest('.control-group').removeClass('error');
//	                label.remove();
//	            },
//
//	            errorPlacement: function (error, element) {
//	                error.addClass('help-small no-left-padding').insertAfter(element.closest('.input-icon'));
//	            },
//
//	            submitHandler: function (form) {
//	                window.location.href = "index.html";
//	            }
//	        });
//
//	        $('.forget-form input').keypress(function (e) {
//	            if (e.which == 13) {
//	                if ($('.forget-form').validate().form()) {
//	                    window.location.href = "index.html";
//	                }
//	                return false;
//	            }
//	        });
//
//	        jQuery('#forget-password').click(function () {
//	            jQuery('.login-form').hide();
//	            jQuery('.forget-form').show();
//	        });
//
//	        jQuery('#back-btn').click(function () {
//	            jQuery('.login-form').show();
//	            jQuery('.forget-form').hide();
//	        });
//
//	        $('.register-form').validate({
//	            errorElement: 'label', //default input error message container
//	            errorClass: 'help-inline', // default input error message class
//	            focusInvalid: false, // do not focus the last invalid input
//	            ignore: "",
//	            rules: {
//	                username: {
//	                    required: true
//	                },
//	                password: {
//	                    required: true
//	                },
//	                rpassword: {
//	                    equalTo: "#register_password"
//	                },
//	                email: {
//	                    required: true,
//	                    email: true
//	                },
//	                tnc: {
//	                    required: true
//	                }
//	            },
//
//	            messages: { // custom messages for radio buttons and checkboxes
//	                tnc: {
//	                    required: "Please accept TNC first."
//	                }
//	            },
//
//	            invalidHandler: function (event, validator) { //display error alert on form submit   
//
//	            },
//
//	            highlight: function (element) { // hightlight error inputs
//	                $(element)
//	                    .closest('.control-group').addClass('error'); // set error class to the control group
//	            },
//
//	            success: function (label) {
//	                label.closest('.control-group').removeClass('error');
//	                label.remove();
//	            },
//
//	            errorPlacement: function (error, element) {
//	                if (element.attr("name") == "tnc") { // insert checkbox errors after the container                  
//	                    error.addClass('help-small no-left-padding').insertAfter($('#register_tnc_error'));
//	                } else {
//	                    error.addClass('help-small no-left-padding').insertAfter(element.closest('.input-icon'));
//	                }
//	            },
//
//	            submitHandler: function (form) {
//	                window.location.href = "index.html";
//	            }
//	        });
//
//	        jQuery('#register-btn').click(function () {
//	            jQuery('.login-form').hide();
//	            jQuery('.register-form').show();
//	        });
//
//	        jQuery('#register-back-btn').click(function () {
//	            jQuery('.login-form').show();
//	            jQuery('.register-form').hide();
//	        });
//        }
//
//    };
//
//}();